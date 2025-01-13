import asyncio
from playwright.async_api import async_playwright
import requests
from requests.utils import dict_from_cookiejar
from .user_agent_utils import UserAgentUtils
from .log_utils import LogUtils

logger = LogUtils.get_logger()

class SearchEngineUtils:
    @staticmethod
    async def search_baidu(keyword, max_results=5):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=UserAgentUtils.random_user_agent())
            page = await context.new_page()

            await page.goto("https://www.baidu.com", wait_until="load")
            await page.wait_for_selector("input[name='wd']", timeout=60000)  # 增加超时时间到 60000ms
            await page.fill("input[name='wd']", keyword)
            await page.press("input[name='wd']", "Enter")
            await page.wait_for_selector("#content_left")

            results = await page.query_selector_all("#content_left .t a")
            search_results = []
            for result in results[:max_results]:
                title = await result.inner_text()
                link = await result.get_attribute("href")
                search_results.append({"title": title, "link": link})

            await browser.close()
            return search_results

    @staticmethod
    async def search_bing(keyword, max_results=5):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=UserAgentUtils.random_user_agent())
            page = await context.new_page()

            await page.goto("https://cn.bing.com", wait_until="load")
            await page.fill("input[name='q']", keyword)
            await page.press("input[name='q']", "Enter")
            await page.wait_for_selector("#b_results", timeout=60000)

            results = await page.query_selector_all("#b_results .b_algo h2 a")
            search_results = []
            for result in results[:max_results]:
                title = await result.inner_text()
                link = await result.get_attribute("href")
                search_results.append({"title": title, "link": link})

            await browser.close()
            return search_results

    @staticmethod
    async def search_sogou(keyword, max_results=5):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=UserAgentUtils.random_user_agent())
            page = await context.new_page()

            await page.goto(f"https://www.sogou.com/web?query={keyword}", wait_until="load")
            await asyncio.sleep(5)  # 添加延迟以模拟真实用户行为
            await page.wait_for_selector(".results", timeout=60000)

            results = await page.query_selector_all(".results .vrwrap h3.vr-title a")
            search_results = []
            for result in results[:max_results]:
                title = await result.inner_text()
                link = await result.get_attribute("href")
                search_results.append({"title": title, "link": link})

            await browser.close()
            return search_results

    @staticmethod
    async def search_sogou_wechat(keyword, max_results=5):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=UserAgentUtils.random_user_agent())
            page = await context.new_page()

            # 获取 cookies
            response = requests.get('https://pb.sogou.com/cl.gif?')
            cookies = dict_from_cookiejar(response.cookies)
            print(f"获取到的 cookies: {cookies}")

            # 设置 cookies
            await context.add_cookies([
                {'name': name, 'value': value, 'domain': '.sogou.com', 'path': '/', 'httpOnly': False, 'secure': False, 'sameSite': 'Lax'}
                for name, value in cookies.items()
            ])

            await page.goto(f"https://weixin.sogou.com/weixin?p=01030402&query={keyword}&type=2", wait_until="load")
            await asyncio.sleep(5)  # 添加延迟以模拟真实用户行为

            await page.wait_for_selector(".news-list", timeout=60000)

            results = await page.query_selector_all(".news-list li .txt-box h3 a")
            search_results = []
            for result in results[:max_results]:
                title = await result.inner_text()
                link = await result.get_attribute("href")
                if not link.startswith("http") and not link.startswith("https"):
                    link = 'https://weixin.sogou.com' + link
                search_results.append({"title": title, "link": link})

            # 获取 header 和 cookie
            headers = await page.evaluate("() => { return Object.fromEntries(new Headers([...document.cookie.split('; ').map(c => c.split('='))])) }")
            cookies = await context.cookies()

            await browser.close()
            return search_results, headers, cookies
