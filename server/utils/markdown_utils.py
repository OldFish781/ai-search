import asyncio
from playwright.async_api import async_playwright
import trafilatura
import time
from concurrent.futures import ThreadPoolExecutor
from .user_agent_utils import UserAgentUtils
from .log_utils import LogUtils

logger = LogUtils.get_logger()

class MarkdownUtils:
    @staticmethod
    def fetch_and_convert_to_md_sync(url, index, headers=None, cookies=None):
        async def fetch(url, headers, cookies):
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent=UserAgentUtils.random_user_agent())
                if headers:
                    await context.set_extra_http_headers(headers)
                if cookies:
                    await context.add_cookies(cookies)
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

        return asyncio.run(fetch(url, headers, cookies))

    @staticmethod
    async def fetch_and_convert_to_md(url, index, headers=None, cookies=None):
        start_time = time.time()
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            result = await loop.run_in_executor(pool, MarkdownUtils.fetch_and_convert_to_md_sync, url, index, headers, cookies)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"转换为 MD 耗时 (序号 {index}): {elapsed_time:.2f} 秒")
        return result
