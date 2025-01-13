import requests
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
from .log_utils import LogUtils
import asyncio
from .function_define_utils import get_function_defines, functions
from .functions_utils import *


logger = LogUtils.get_logger()

class PromptUtils:
    @staticmethod
    def load_prompt_template(tag):
        template_path = "prompt_templates"
        if tag == "keyword":
            template_file = os.path.join(template_path, "keyword_prompt.txt")
        elif tag == "no_keyword":
            template_file = os.path.join(template_path, "no_keyword_prompt.txt")
        elif tag == "common":
            template_file = os.path.join(template_path, "common_prompt.txt")   
        else:
            raise ValueError(f"Unknown tag: {tag}")
        with open(template_file, "r", encoding="utf-8") as file:
            template = file.read()
        
        return template

    @staticmethod
    def call_model_api(url, model, messages, max_tokens=4000, top_p=1, temperature=0.1, frequency_penalty=0, presence_penalty=0, repetition_penalty=1, top_k=-1, tools=[]):
        response = requests.post(
            url=url,
            data=json.dumps({
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "tools": tools,
                "temperature": temperature,
                "frequency_penalty": frequency_penalty,
                "presence_penalty": presence_penalty,
                "repetition_penalty": repetition_penalty,
                "top_k": top_k,
            })
        )
        return response.json()

    @staticmethod
    def call_large_model_api(prompt):
        response = PromptUtils.call_model_api(
            url="http://10.30.1.3:8900/v1/chat/completions",
            model="TuringYitian-32b",
            messages=[
                {"role": "system", "content": "你是出色的 AI 助手，帮我处理事务。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            top_p=1,
            temperature=0.1,
            frequency_penalty=0,
            presence_penalty=0,
            repetition_penalty=1,
            top_k=-1,
        )
        return response['choices'][0]['message']['content']

    @staticmethod
    async def dispatcher(prompt):
        function_definitions = get_function_defines()
        response = PromptUtils.call_model_api(
            url="http://10.30.1.3:8900/v1/chat/completions",
            model="TuringYitian-32b",
            messages=[
                {"role": "system", "content": "你是出色的 AI 助手，帮我处理事务。"},
                {"role": "user", "content": prompt}
            ],
            tools=function_definitions,
            max_tokens=4000,
            top_p=1,
            temperature=0.1,
            frequency_penalty=0,
            presence_penalty=0,
            repetition_penalty=1,
            top_k=-1,
        )
        choices = response.get('choices', [])
        if choices:
            message = choices[0].get('message', {})
            tool_calls = message.get('tool_calls', [])
            if tool_calls:
                tool_call = tool_calls[0]
                function_name = tool_call['function']['name']
                arguments = json.loads(tool_call['function']['arguments'])
                func = globals().get(function_name)
                if func:
                    try:
                        return await func(**arguments)
                    except Exception as e:
                        logger.error('Error calling function %s: %s', function_name, e)
                        return Exception(f"Error calling function {function_name}: {e}")
                else:
                    logger.error('Function %s not found', function_name)
                    return f"Error: Function {function_name} not found"
            else:
                return message.get('content', "Error: No content found in message")
        else:
            return "Error: No choices found in response"

    @staticmethod
    def summarize_markdown_sync(keyword, md_content, index):
        start_time = time.time()
        prompt_template = PromptUtils.load_prompt_template('keyword')
        prompt = prompt_template.format(keyword=keyword, content=md_content)
        summary = PromptUtils.call_large_model_api(prompt)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"总结耗时 (序号 {index}): {elapsed_time:.2f} 秒")
        return summary
    
    @staticmethod
    async def summarize_sync(content):
        start_time = time.time()
        prompt_template = PromptUtils.load_prompt_template('common')
        prompt = prompt_template.format(content=content)
        summary = PromptUtils.call_large_model_api(prompt)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"总结耗时: {elapsed_time:.2f} 秒")
        return summary

    @staticmethod
    async def summarize_markdown(keyword, md_content, index):
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            return await loop.run_in_executor(pool, PromptUtils.summarize_markdown_sync, keyword, md_content, index)
