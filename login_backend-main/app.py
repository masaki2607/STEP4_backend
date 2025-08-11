# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt
import bcrypt
from fastapi import APIRouter, Depends
from auth import get_current_employee

from database import SessionLocal
from models import Employee
from datetime import datetime, timedelta



# FastAPIインスタンス作成
app = FastAPI()

# CORS（クロスオリジン）設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて制限してください
    allow_credentials=False,  # "*" origins との組み合わせのため False に変更
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT設定
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# DBセッション取得関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# パスワードの照合
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

# ルートエンドポイント（テスト用）
@app.get("/")
def read_root():
    return {"message": "OneView API is running!", "status": "healthy"}

# ログインエンドポイント
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Employee).filter(Employee.emp_id == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="社員番号またはパスワードが正しくありません")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": user.emp_id, "exp": expire}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}

#保護されたエンドポイントを定義
router = APIRouter()

@router.get("/protected")
def protected_route(emp_id: str = Depends(get_current_employee)):
    return {"message": f"{emp_id} さん、ようこそ！"}

# ルーターをアプリに登録
app.include_router(router)

#パスワード再設定のエンドポイントを定義
from reset_password import router as reset_router
app.include_router(reset_router)

# Azure App Service用の起動設定
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
