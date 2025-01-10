import asyncio
from playwright.async_api import async_playwright
import trafilatura


# Step 1: 搜索关键词并提取链接
async def search_baidu(keyword, max_results=5):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # headless=False 可观察浏览器操作
        context = await browser.new_context()
        page = await context.new_page()

        # 打开百度主页
        await page.goto("https://www.baidu.com", wait_until="load")

        # 输入关键词并提交搜索
        await page.fill("input[name='wd']", keyword)
        await page.press("input[name='wd']", "Enter")

        # 等待搜索结果加载完成
        await page.wait_for_selector("#content_left")

        # 获取搜索结果链接
        results = await page.query_selector_all("#content_left .t a")
        search_results = []
        for result in results[:max_results]:  # 限制最多抓取 max_results 条链接
            title = await result.inner_text()
            link = await result.get_attribute("href")
            search_results.append({"title": title, "link": link})

        await browser.close()
        return search_results


# Step 2: 递归访问链接，提取 HTML 并转换为 Markdown
async def fetch_and_convert_to_md(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # 打开目标链接
            await page.goto(url, wait_until="load")
            # 提取页面 HTML 内容
            html_content = await page.content()

            # 转换 HTML 为 Markdown
            markdown_content = trafilatura.extract(html_content, output_format="markdown", include_formatting=True)
            return markdown_content
        except Exception as e:
            print(f"访问 {url} 时出错：{e}")
            return None
        finally:
            await browser.close()


# Step 3: 主函数
async def main():
    keyword = "AGI"  # 搜索关键词
    max_results = 5  # 设置最多抓取搜索结果条数

    # 获取百度搜索结果
    search_results = await search_baidu(keyword, max_results=max_results)

    print("搜索结果：")
    for index, result in enumerate(search_results, start=1):
        print(f"{index}. {result['title']}\n   {result['link']}")

    # 递归获取每个链接的 Markdown 内容
    for index, result in enumerate(search_results, start=1):
        print(f"\n正在处理第 {index} 个链接：{result['link']}")
        markdown = await fetch_and_convert_to_md(result["link"])

        if markdown:
            print(f"\nMarkdown 内容（{result['title']}）：\n")
            print(markdown[:500])  # 仅输出前 500 字符以简化展示
        else:
            print(f"无法提取 {result['link']} 的 Markdown 内容。")


if __name__ == "__main__":
    asyncio.run(main())