from pydantic import BaseModel



class UserName(BaseModel):
    name: str


class UserLogin(UserName):
    password: str


class UserRegister(UserLogin):
    key: str


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class TokenFull(BaseModel):
    access_token: str
    refresh_token: str
