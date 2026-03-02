import asyncio
import logging

import aiohttp

from .exceptions import OutOfTries, UnableToAccess, RequestMethodNotFoundException
from .response import ResponseData, Method


class HttpMakerAsync:
    """
    Асинхронный класс для выполнения HTTP-запросов.

    Параметры:
        base_url (str): Базовый URL для всех запросов.
        base_headers (dict | None): Базовые заголовки для всех запросов.
        base_params (dict | None): Базовые параметры для всех запросов.
        tries_to_reconnect (int): Количество попыток переподключения при ошибке.
        timeout_in_sec (int): Таймаут для запросов в секундах.

    Методы:
        full_path(path: str) -> str: Получает полный путь для запроса.
        make(
            url: str = '' - относительный (если указан base_url) или полный путь
            method: Method = 'GET', - метод запроса
            data: dict | str | None = None, - данные запроса data
            json: dict | None = None,
            params: dict | None = None, - заголовки для запоса + base_params
            headers: dict | None = None, - заголовки для запоса + base_headers
            try_wait_if_error: bool = True, - если будет вызвана ошибка, выполнить ожидание
        ) -> ResponseData

    Так же добавлены методы (то же что и make но method заранее задан):
        - get
        - post
        - put
        - patch
        - delete
    """

    def __init__(
        self,
        base_url: str = '',
        base_headers: None | dict = None,
        base_params: None | dict = None,
        tries_to_reconnect: int = 3,
        timeout_in_sec: int = 10,
    ):
        self.__base_url = base_url

        if base_headers is None:
            base_headers = {}
        self.__headers = base_headers   # это должен быть словарь

        if base_params is None:
            base_params = {}
        self.__params = base_params    # это должен быть словарь

        self.__tries_to_reconnect = tries_to_reconnect
        self.__timeout = timeout_in_sec

    def full_path(self, path: str) -> str:
        if path == '':
            return self.__base_url
        return f'{self.__base_url}/{path if not path.startswith('/') else path[1:]}'

    async def __execute(
        self,
        path: str,
        method: Method,
        data: dict | str | None = None,
        json: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
        try_wait_if_error: bool = True,
    ) -> ResponseData:
        logging.debug(f'{self.__class__.__name__} {method} -> {path} ? {params}')
        for _ in range(self.__tries_to_reconnect):
            try:
                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=self.__timeout)
                ) as session:
                    # Получаем метод HTTP
                    http_method = getattr(session, method.lower())

                    # Совмещаем заголовки
                    if headers is not None:
                        headers = {**self.__headers, **headers}
                    else:
                        headers = self.__headers

                    # Совмещаем параметры
                    if params is not None:
                        params = {**self.__params, **params}
                    else:
                        params = self.__params

                    async with http_method(
                        url=self.full_path(path) if not path.startswith('http') else path,
                        headers=headers,
                        params=params,
                        data=data,
                        json=json,
                    ) as res:
                        return await self.__get_response_data(res)
            except aiohttp.ClientConnectorError as e:
                logging.error(f'{self.__class__.__name__} > Client connection error {e}')
                if try_wait_if_error:
                    await asyncio.sleep(10)
                    continue
                break
            except aiohttp.ConnectionTimeoutError as e:
                logging.error(f'{self.__class__.__name__} > Connection error: {e}')
                if try_wait_if_error:
                    await asyncio.sleep(20)
                    continue
                break
            except aiohttp.ClientError as e:
                logging.critical(f'{self.__class__.__name__} > Client error: {e}')
                if try_wait_if_error:
                    await asyncio.sleep(60)
                    continue
                break
            except AttributeError as e:
                logging.critical(f'{self.__class__.__name__} > Uncaught error: {e}')
                raise RequestMethodNotFoundException(method)
        logging.critical(f'{self.__class__.__name__} > Tries out but no return')
        raise OutOfTries(path)

    async def _make(
        self,
        url: str = '',
        method: Method = 'GET',
        data: dict | str | None = None,
        json: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
        try_wait_if_error: bool = True,
    ) -> ResponseData:
        logging.debug(f'{self.__class__.__name__} > make -> {self.full_path(url)}')

        # В стандартном HttpMaker тут работа с кэшем
        # Для упращения кода и тк эта логика в проекте не используется она была удалена

        return await self.__execute(
            path=url,
            method=method,
            data=data,
            json=json,
            params=params,
            headers=headers,
            try_wait_if_error=try_wait_if_error,
        )
        # Тут должна быть логика с сохранением в кэш

    async def __get_response_data(
        self,
        response: aiohttp.ClientResponse,
    ) -> ResponseData:
        # Получаем тип контента (проверяем оба варианта регистра)
        try:
            content_type = (
                response.headers.get('Content-Type') or
                {name.lower(): val for name, val in response.headers}.get('content-type')
            )
        except ValueError:
            logging.warning(f'{self.__class__.__name__} > no content-type header, set empty')
            content_type = 'empty'

        try:
            match content_type.split(';')[0].strip().lower():
                case 'application/json' | 'text/html':
                    data = await response.json(content_type=None if 'html' in content_type else 'json')
                    if type(data) is not dict:
                        data = {'data': data}
                case 'empty':
                    data = await response.json(content_type='json')
                case _:
                    logging.warning(f'{self.__class__.__name__} > unreadable content type: {content_type}')
                    raise UnableToAccess(response.url)
            return ResponseData(
                url=str(response.url),
                status=response.status,
                headers=dict(response.headers),
                json=data,
            )
        except aiohttp.ContentTypeError as e:
            logging.error(e)
            raise UnableToAccess(response.url)
