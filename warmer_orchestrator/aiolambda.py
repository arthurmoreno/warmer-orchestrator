import asyncio

import aiobotocore


class AioLambda:

    session = None
    lambda_instance = None

    access_key = None
    secret_key = None
    region_name = None

    def __init__(self):
        self.set_lambda_instance()

    def set_lambda_instance(self):
        loop = asyncio.get_event_loop()
        self.session = aiobotocore.get_session(loop=loop)

        self.lambda_instance = self.session.create_client('lambda')

    async def close_instance(self):
        await self.lambda_instance.close()

    async def invoke(self, *args, **kwargs):
        return await self.lambda_instance.invoke(*args, **kwargs)
