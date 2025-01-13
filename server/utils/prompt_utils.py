import requests
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
from .log_utils import LogUtils
import asyncio

logger = LogUtils.get_logger()

class PromptUtils:
    @staticmethod
    def load_prompt_template(keyword):
        template_path = "prompt_templates"
        if keyword:
            template_file = os.path.join(template_path, "keyword_prompt.txt")
        else:
            template_file = os.path.join(template_path, "no_keyword_prompt.txt")
        
        with open(template_file, "r", encoding="utf-8") as file:
            template = file.read()
        
        return template

    @staticmethod
    def call_large_model_api(prompt):
        response = requests.post(
            url="http://10.30.1.3:8900/v1/chat/completions",
            data=json.dumps({
                "model": "TuringYitian-32b",
                "messages": [
                    {"role": "system", "content": "你是出色的AI 助手，帮我处理事务。"},
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
        return response.json()['choices'][0]['message']['content']

    @staticmethod
    def summarize_markdown_sync(keyword, md_content, index):
        start_time = time.time()
        prompt_template = PromptUtils.load_prompt_template(keyword)
        prompt = prompt_template.format(keyword=keyword, content=md_content)
        summary = PromptUtils.call_large_model_api(prompt)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"总结耗时 (序号 {index}): {elapsed_time:.2f} 秒")
        return summary

    @staticmethod
    async def summarize_markdown(keyword, md_content, index):
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            return await loop.run_in_executor(pool, PromptUtils.summarize_markdown_sync, keyword, md_content, index)
