import aiohttp

from .debug.debug_dataclass import Level
from app.settings import settings


class DispatcherAsync:
    def __init__(
        self,
        dispatcher_url: str,
        app_name: str,
        dispatcher_code: str,
        loggers_paths: list[str] | None = None,
        max_logs_to_send: int = 10,
    ):
        self.__dispatcher_url = dispatcher_url
        self.__code = dispatcher_code
        self.__app_name = app_name
        if loggers_paths is None:
            loggers_paths = []
        self.__loggers = loggers_paths
        self.__max_logs_to_send = max_logs_to_send

    async def send(
        self,
        title: str,
        message: str,
        level: Level,
        logs: str | list[str] | tuple[str] | None = None,
    ) -> bool:
        if type(logs) in (list, tuple):
            logs='\n'.join(logs)
        else:
            logs = ''
            try:
                for i in self.__loggers:
                    with open(i, 'r') as f:
                        if logs != '':
                            logs += '\n'
                        logs += f'Logfile: {i}\n'
                        logs = '\n'.join(f.readlines()[-self.__max_logs_to_send:])
            except FileNotFoundError:
                logs = 'Logs not found'
        async with aiohttp.ClientSession() as session:
            res = await session.post(
                self.__dispatcher_url,
                json={
                    'incident': {
                        'title': title,
                        'message': message,
                        'logs': logs,
                        'level': level,
                    },
                    'app_name': self.__app_name,
                    'code': self.__code,
                }
            )
            return True if res is not None and (await res.json())['ok'] == True else False


dispatcher = DispatcherAsync(
    dispatcher_url=settings.DISPATCHER_URL,
    app_name=settings.DISPATCHER_APP,
    dispatcher_code=settings.DISPATCHER_CODE,
    loggers_paths=['logs/app.log', 'logs/error.log'],
    max_logs_to_send=10
)
