from trafilatura import fetch_url, extract, extract_metadata, html2txt

downloaded = fetch_url('https://modelscope.cn/models?page=1&tasks=hotTask%3Atext-to-image-synthesis&type=tasks')

result = extract(downloaded, output_format="markdown", with_metadata=True)
# result = html2txt(downloaded)

print(result)