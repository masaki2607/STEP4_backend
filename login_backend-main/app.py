from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# FastAPIインスタンス作成
app = FastAPI()

# CORS（クロスオリジン）設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルートエンドポイント（テスト用）
@app.get("/")
def read_root():
    return {"message": "OneView API is running!", "status": "healthy", "version": "minimal"}

# ヘルスチェックエンドポイント
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "OneView Backend"}

# Azure App Service用の起動設定
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
