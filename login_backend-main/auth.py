#FastAPIでJWTトークンを使ってユーザー（ここでは社員）の認証を行うための処理

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
#configのディレクトリからインポートしている。

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # token取得URL

def get_current_employee(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        emp_id = payload.get("sub")
        if emp_id is None:
            raise HTTPException(status_code=401, detail="認証情報が不正です")
        return emp_id
    except JWTError:
        raise HTTPException(status_code=401, detail="トークンが無効です")