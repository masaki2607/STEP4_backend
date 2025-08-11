from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# FastAPIインスタンス作成
app = FastAPI()

# ログインリクエスト用のモデル
class LoginRequest(BaseModel):
    username: str
    password: str

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

# テスト用ログインエンドポイント
@app.post("/login")
def login(request: LoginRequest):
    # テスト用の簡単な認証
    if request.username == "test" and request.password == "password":
        return {
            "access_token": "test_token_123",
            "token_type": "bearer",
            "message": "ログイン成功"
        }
    else:
        raise HTTPException(
            status_code=401,
            detail="社員番号またはパスワードが正しくありません"
        )

# Azure App Service用の起動設定
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
