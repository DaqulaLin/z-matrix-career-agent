# 文件名: main.py
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from compass_api.agent import run_compass_engine

# 初始化干净的 FastAPI 引擎
app = FastAPI(title="Compass Oracle API")

# 定义严格的输入参数校验
class CompassRequest(BaseModel):
    target_job: str
    mode: str = "mixed"  # 默认使用综合模式

# 核心罗盘推演接口 (处理 POST 请求)
@app.post("/compass")
def generate_compass(req: CompassRequest):
    try:
        print(f"🚀 接收到推演请求: 职位={req.target_job}, 模式={req.mode}")
        # 调用 agent.py 里的核心计算函数
        result = run_compass_engine(req.target_job, req.mode)
        return {"status": "success", "data": result}
    except Exception as e:
        print(f"❌ 推演失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 健康探针接口 (处理 GET 请求，防止 307 重定向)
@app.get("/")
def health_check():
    return {"status": "Compass API is running and ready for deduction!"}

if __name__ == "__main__":
    # 使用 Uvicorn 启动
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)