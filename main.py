from fastapi import FastAPI, HTTPException, Depends
import jwt
import datetime
from fastapi.security import OAuth2PasswordBearer
import uvicorn

app = FastAPI()

# JWT için gizli anahtar
SECRET_KEY = "supersecretkey"  # Gerçek projelerde çevresel değişkenlerde sakla
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Ana sayfa (public endpoint)
@app.get("/")
def home():
    return {"message": "Welcome to the API"}

# JWT Token oluşturma fonksiyonu
def create_token(data: dict):
    """ Kullanıcıya JWT token oluşturur """
    data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

# Token oluşturma endpoint'i
@app.post("/token")
def generate_token():
    """ Token oluşturur ve döner """
    return {"access_token": create_token({"user": "test_user"}), "token_type": "bearer"}

# Güvenli veri isteyen endpoint (JWT Token zorunlu)
@app.get("/secure-data")
def secure_data(token: str = Depends(oauth2_scheme)):
    """ Güvenli endpoint: Token gerektirir """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"message": f"Hello, {payload['user']}!"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Uvicorn sunucusunu başlat
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
