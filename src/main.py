from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt

app = FastAPI(title="Enterprise IAM Auth (Python)")

SECRET_KEY = "super-secret-enterprise-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Mock User DB
MOCK_USERS = {
    "admin": {"password": "password123", "role": "admin"},
    "user": {"password": "password123", "role": "user"}
}

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "role": payload.get("role")}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_admin(user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = MOCK_USERS.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    token_data = {"sub": form_data.username, "role": user["role"]}
    access_token = create_access_token(token_data)
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user

@app.get("/admin/dashboard")
async def admin_only_route(current_user: dict = Depends(require_admin)):
    return {"message": "Welcome to the admin dashboard"}
