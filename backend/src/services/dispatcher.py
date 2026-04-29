from core.requests_makers import HttpMakerAsync

from src.settings import settings


class DispatcherService(HttpMakerAsync):
    """
    Сервис подключения к NCT-Dispatcher
    """
    def __init__(self):
        super().__init__(
            base_url=settings.DISPATCHER_URL,
        )


dispatcher_service = DispatcherService()
