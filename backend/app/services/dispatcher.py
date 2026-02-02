from core.requests_makers import HttpMakerAsync

from app.settings import settings


class DispatcherService(HttpMakerAsync):
    def __init__(self):
        super().__init__(
            base_url=settings.BLOCKER_URL,
            base_headers={
                'X-Access-Code': settings.BLOCKER_ACCESS_CODE
            }
        )


dispatcher_service = DispatcherService()
