from .search_engine_utils import SearchEngineUtils
from .markdown_utils import MarkdownUtils
from .log_utils import LogUtils
import asyncio
from datetime import datetime
import pytz

logger = LogUtils.get_logger()

async def perform_search(engine, keyword, max_results):
    """
    执行搜索操作。

    参数:
    engine (str): 搜索引擎名称，如 'baidu', 'bing', 'sogou', 'wechat'， 默认百度搜索。
    keyword (str): 搜索关键词。
    max_results (int): 返回的最大结果数。

    返回:
    tuple: 搜索结果列表，headers 和 cookies。
    """
    from .prompt_utils import PromptUtils  # 移动导入到函数内部
    headers = None
    cookies = None
    # 获取搜索结果
    if engine == "baidu":
        search_results = await SearchEngineUtils.search_baidu(keyword, max_results)
    elif engine == "bing":
        search_results = await SearchEngineUtils.search_bing(keyword, max_results)
    elif engine == "sogou":
        search_results = await SearchEngineUtils.search_sogou(keyword, max_results)
    elif engine == "wechat":
        search_results, headers, cookies = await SearchEngineUtils.search_sogou_wechat(keyword, max_results)
    else:
        raise ValueError(f"未知的搜索引擎: {engine}")
    
    logger.info(f"关键字：{keyword}\n从 {engine} 获取的搜索结果：")
    for index, result in enumerate(search_results, start=1):
        logger.info(f"{index}. {result['title']}")

    mark_downs = []
    # 递归获取每个链接的 Markdown 内容并总结
    tasks = [MarkdownUtils.fetch_and_convert_to_md(result["link"], index, headers, cookies) for index, result in enumerate(search_results, start=1)]
    markdowns = await asyncio.gather(*tasks)

    # 对每个 Markdown 进行总结
    summarized_markdowns = await asyncio.gather(*[PromptUtils.summarize_markdown(keyword, md, index) for index, md in enumerate(markdowns, start=1) if md])
    mark_downs.extend(summarized_markdown for summarized_markdown in summarized_markdowns if summarized_markdown)

    # 使用大模型接口进行总结
    summary = await PromptUtils.summarize_markdown(keyword, str.join("\n", mark_downs)[:20000], "最终")
    
    return summary

def get_current_time(content):
    """
    获取当前时间的字符串表示形式。

    参数:
    content (str): 提问内容。

    返回:
    str: 当前时间的字符串表示形式，格式为 'YYYY-MM-DD HH:MM:SS'。
    """
    from .prompt_utils import PromptUtils  # 移动导入到函数内部
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = content + current_datetime
    summary = PromptUtils.summarize_sync(content)
    return summary

