import asyncio
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from utils.log_utils import LogUtils
from utils.prompt_utils import PromptUtils

logger = LogUtils.get_logger()

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
    message: str  # 搜索关键词

# FastAPI 接口
@app.post("/search_and_summarize/")
async def search_and_summarize(request: SearchRequest):
    try:
        start_time = time.time()
        search_results = await PromptUtils.dispatcher(prompt=request.message)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"总耗时: {elapsed_time:.2f} 秒")
        return {"summary": search_results}

    except Exception as e:
        logger.error(f"处理请求时出错：{e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)