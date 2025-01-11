import asyncio
from playwright.async_api import async_playwright

# 获取搜索引擎的结果
async def search_baidu(keyword, max_results=5):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.baidu.com", wait_until="load")
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


async def search_bing(keyword, max_results=5):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://cn.bing.com", wait_until="load")
        await page.fill("input[name='q']", keyword)
        await page.press("input[name='q']", "Enter")
        await page.wait_for_selector("#b_results")

        results = await page.query_selector_all("#b_results .b_algo h2 a")
        search_results = []
        for result in results[:max_results]:
            title = await result.inner_text()
            link = await result.get_attribute("href")
            search_results.append({"title": title, "link": link})

        await browser.close()
        return search_results


async def search_sogou(keyword, max_results=5):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.sogou.com", wait_until="load")
        await page.fill("input[name='query']", keyword)
        await page.press("input[name='query']", "Enter")
        await page.wait_for_selector(".results", timeout=60000)

        results = await page.query_selector_all(".results .vrwrap h3.vr-title a")
        search_results = []
        for result in results[:max_results]:
            title = await result.inner_text()
            link = await result.get_attribute("href")
            search_results.append({"title": title, "link": link})

        await browser.close()
        return search_results
