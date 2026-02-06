class RedisClientMock:
    def __init__(self, *args, **kwargs):
        pass

    async def get(self, *args, **kwargs):
        return None

    async def set(self, *args, **kwargs):
        pass

    async def get_dict(self, *args, **kwargs):
        return {}

    async def set_dict(self, *args, **kwargs):
        pass

    async def delete(self, *args, **kwargs):
        return True

    async def set_json(self, *args, **kwargs):
        return True

    async def get_json(self, *args, **kwargs):
        return {}


class BlockListMock:
    def __init__(self, *args, **kwargs):
        pass

    async def in_ban(self, *args, **kwargs):
        return False

    async def ban(self, *args, **kwargs):
        return True
