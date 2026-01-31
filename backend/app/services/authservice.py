from dataclasses import dataclass

from fastapi import HTTPException

from core.requests_makers import HttpMakerAsync

from app.settings import settings


@dataclass(frozen=True, slots=True)
class AuthToken:
    access_token: str
    refresh_token: str


class AuthService(HttpMakerAsync):
    def __init__(self):
        super().__init__(
            base_url=settings.AUTH_URL,
            base_headers={
                'X-Access-Code': settings.AUTH_ACCESS_CODE
            }
        )

    async def login(self, name: str, password: str) -> AuthToken:
        ans = await self._make('/v1/auth/login', method='POST', json={'name': name, 'password': password})
        if ans.status != 200:
            raise HTTPException(
                status_code=ans.status,
                detail=ans.json.get('detail', 'Unknown error')
            )
        return AuthToken(ans.json['access_token'], ans.json['refresh_token'])

    async def logout(self, name: str) -> bool:
        ans = await self._make('/v1/auth/logout', method='POST', json={'name': name})
        if ans.status != 200:
            raise HTTPException(
                status_code=ans.status,
                detail=ans.json.get('detail', 'Unknown error')
            )
        return ans.json['ok']

    async def refresh(self, refresh_token: str) -> AuthToken:
        ans = await self._make('/v1/auth/refresh', method='POST', json={'refresh_token': refresh_token})
        if ans.status != 200:
            raise HTTPException(
                status_code=ans.status,
                detail=ans.json.get('detail', 'Unknown error')
            )
        return AuthToken(ans.json['access_token'], ans.json['refresh_token'])

    async def register(self, name: str, password: str, key: str) -> bool:
        return (await self._make('/v1/auth/register', method='POST', json={
            'name': name,
            'password': password,
            'key': key
        })).json['ok']


auth_service = AuthService()
