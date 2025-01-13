import asyncio
import logging
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from utils.search_engine_utils import SearchEngineUtils
from utils.markdown_utils import MarkdownUtils
from utils.prompt_utils import PromptUtils
from utils.log_utils import LogUtils

app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)

# 请求数据的 Pydantic 模型
class SearchRequest(BaseModel):
    engine: str  # 搜索引擎，如 baidu, bing, sogou
    keyword: str  # 搜索关键词
    max_results: int = 5  # 默认返回最多 5 个结果

# FastAPI 接口
@app.post("/search_and_summarize/")
async def search_and_summarize(request: SearchRequest):
    try:
        start_time = time.time()
        headers = None
        cookies = None
        # 获取搜索结果
        if request.engine == "baidu":
            search_results = await SearchEngineUtils.search_baidu(request.keyword, request.max_results)
        elif request.engine == "bing":
            search_results = await SearchEngineUtils.search_bing(request.keyword, request.max_results)
        elif request.engine == "sogou":
            search_results = await SearchEngineUtils.search_sogou(request.keyword, request.max_results)
        elif request.engine == "wechat":
            search_results, headers, cookies = await SearchEngineUtils.search_sogou_wechat(request.keyword, request.max_results)
        else:
            raise ValueError(f"未知的搜索引擎: {request.engine}")

        LogUtils.logger.info(f"关键字：{request.keyword}\n从 {request.engine} 获取的搜索结果：")
        for index, result in enumerate(search_results, start=1):
            LogUtils.logger.info(f"{index}. {result['title']}")

        mark_downs = []
        # 递归获取每个链接的 Markdown 内容并总结
        tasks = [MarkdownUtils.fetch_and_convert_to_md(result["link"], index, headers, cookies) for index, result in enumerate(search_results, start=1)]
        markdowns = await asyncio.gather(*tasks)

        # 对每个 Markdown 进行总结
        summarized_markdowns = await asyncio.gather(*[PromptUtils.summarize_markdown(request.keyword, md, index) for index, md in enumerate(markdowns, start=1) if md])
        mark_downs.extend(summarized_markdown for summarized_markdown in summarized_markdowns if summarized_markdown)

        # 使用大模型接口进行总结
        summary = await PromptUtils.summarize_markdown(request.keyword, str.join("\n", mark_downs)[:20000], "最终")
        end_time = time.time()
        elapsed_time = end_time - start_time
        LogUtils.logger.info(f"总耗时: {elapsed_time:.2f} 秒")
        return {"summary": summary}

    except Exception as e:
        LogUtils.logger.error(f"处理请求时出错：{e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)