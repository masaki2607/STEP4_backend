# reset_password.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from models import Employee
import bcrypt

router = APIRouter()

# 照合API
@router.post("/api/verify-user")
def verify_user(payload: dict, db: Session = Depends(get_db)):
    emp_id = payload.get("emp_id")
    name = payload.get("name")

    user = db.query(Employee).filter(
        Employee.emp_id == emp_id,
        Employee.name == name
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="社員情報が見つかりません。")

    return {"message": "本人確認に成功しました。"}

# パスワード再設定用スキーマ
class PasswordResetRequest(BaseModel):
    empId: str
    newPassword: str

# パスワード再設定API
@router.post("/reset-password")
def reset_password(data: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(Employee).filter(Employee.emp_id == data.empId).first()
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    hashed_pw = bcrypt.hashpw(data.newPassword.encode(), bcrypt.gensalt()).decode()
    user.password = hashed_pw
    db.commit()

    return {"message": "パスワードが更新されました"}