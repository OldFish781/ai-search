import asyncio
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from playwright.async_api import async_playwright
import trafilatura
import random
import requests
import json
from fastapi.middleware.cors import CORSMiddleware
import os
from utils import search_baidu, search_bing, search_sogou

# 配置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - [%(levelname)s] - [%(threadName)s]:  %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[
                        logging.FileHandler("app.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)

# 生成随机 User-Agent 的函数
def random_user_agent():
    user_agent_list = [
        # Chrome on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.100 Safari/537.36",
        # Firefox on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0",
        # Chrome on Mac
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.100 Safari/537.36",
        # Safari on iPhone
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Mobile/15E148 Safari/604.1",
        # Edge on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.100 Safari/537.36 Edg/110.0.1587.46",
    ]
    return random.choice(user_agent_list)


# 请求数据的 Pydantic 模型
class SearchRequest(BaseModel):
    engine: str  # 搜索引擎，如 baidu, bing, sogou
    keyword: str  # 搜索关键词
    max_results: int = 5  # 默认返回最多 5 个结果


# 获取页面并转换为 Markdown 格式
def fetch_and_convert_to_md_sync(url, index):
    async def fetch(url):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=random_user_agent())
            context.set_default_navigation_timeout(60000)  # 设置请求超时
            page = await context.new_page()

            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://www.baidu.com" + url  # 请替换为主网站 URL

            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=120000)  # 设置更长的超时
                await page.wait_for_timeout(2000)

                html_content = await page.content()
                markdown_content = trafilatura.extract(html_content, output_format="markdown", include_formatting=True)
                return markdown_content
            except Exception as e:
                logger.error(f"访问 {url} 时出错：{e}")
                return None
            finally:
                await browser.close()

    return asyncio.run(fetch(url))

async def fetch_and_convert_to_md(url, index):
    start_time = time.time()
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, fetch_and_convert_to_md_sync, url, index)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"转换为 MD 耗时 (序号 {index}): {elapsed_time:.2f} 秒")
    return result


def load_prompt_template(keyword):
    template_path = "prompt_templates"
    if keyword:
        template_file = os.path.join(template_path, "keyword_prompt.txt")
    else:
        template_file = os.path.join(template_path, "no_keyword_prompt.txt")
    
    with open(template_file, "r", encoding="utf-8") as file:
        template = file.read()
    
    return template

# 使用大模型接口进行总结
def summarize_markdown_sync(keyword, md_content, index):
    start_time = time.time()
    prompt_template = load_prompt_template(keyword)
    prompt = prompt_template.format(keyword=keyword, content=md_content)
    response = requests.post(
        url="http://10.30.1.3:8900/v1/chat/completions",
        data=json.dumps({
            "model": "TuringYitian-32b",
            "messages": [
                {"role": "system", "content": "你是出色的概要助手，帮我处理内容。"},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 4000,
            "top_p": 1,
            "temperature": 0.1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "repetition_penalty": 1,
            "top_k": -1,
        })
    )
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"总结耗时 (序号 {index}): {elapsed_time:.2f} 秒")
    return response.json()['choices'][0]['message']['content']

async def summarize_markdown(keyword, md_content, index):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, summarize_markdown_sync, keyword, md_content, index)


# FastAPI 接口
@app.post("/search_and_summarize/")
async def search_and_summarize(request: SearchRequest):
    try:
        start_time = time.time()
        # 获取搜索结果
        if request.engine == "baidu":
            search_results = await search_baidu(request.keyword, request.max_results)
        elif request.engine == "bing":
            search_results = await search_bing(request.keyword, request.max_results)
        elif request.engine == "sogou":
            search_results = await search_sogou(request.keyword, request.max_results)
        else:
            raise ValueError(f"未知的搜索引擎: {request.engine}")

        logger.info(f"关键字：{request.keyword}\n从 {request.engine} 获取的搜索结果：")
        for index, result in enumerate(search_results, start=1):
            logger.info(f"{index}. {result['title']}")

        mark_downs = []
        # 递归获取每个链接的 Markdown 内容并总结
        tasks = [fetch_and_convert_to_md(result["link"], index) for index, result in enumerate(search_results, start=1)]
        markdowns = await asyncio.gather(*tasks)

        # 对每个 Markdown 进行总结
        summarized_markdowns = await asyncio.gather(*[summarize_markdown(request.keyword, md, index) for index, md in enumerate(markdowns, start=1) if md])
        mark_downs.extend(summarized_markdown for summarized_markdown in summarized_markdowns if summarized_markdown)

        # 使用大模型接口进行总结
        summary = await summarize_markdown(request.keyword, str.join("\n", mark_downs)[:20000], "最终")
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"总耗时: {elapsed_time:.2f} 秒")
        return {"summary": summary}

    except Exception as e:
        logger.error(f"处理请求时出错：{e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)