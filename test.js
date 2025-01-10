async function bingSearch(query) {
  try {
    //https://serpapi.com/bing-search-api
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(
      `https://www.bing.com/search?form=QBRE&q=${encodeURIComponent(
        query
      )}&cc=US`
    );
    const summaries = await page.evaluate(() => {
      const liElements = Array.from(
        document.querySelectorAll("#b_results > .b_algo")
      );
      const firstFiveLiElements = liElements.slice(0, 5);
      return firstFiveLiElements.map((li) => {
        const abstractElement = li.querySelector(".b_caption > p");
        const linkElement = li.querySelector("a");
        const href = linkElement.getAttribute("href");
        const title = linkElement.textContent;

        const abstract = abstractElement ? abstractElement.textContent : "";
        return { href, title, abstract };
      });
    });
    await browser.close();
    console.log(summaries);
    return summaries;
  } catch (error) {
    console.error("An error occurred:", error);
  }
}

bingSearch("百度")