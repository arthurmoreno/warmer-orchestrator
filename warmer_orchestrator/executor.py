import asyncio

from aiolambda import AioLambda
from logger import logger
from json_encoder import json_dumps


BASE_WARMER_PAYLOAD = {
    "body": {
        "lambdas": []
    }
}


class Executor:

    function_name = ""

    def __init__(self, warmer_function_name):
        self.function_name = warmer_function_name

    async def invoke_lambda(self, aio_lambda, warmer_payload):
        try:
            response = await aio_lambda.invoke(
                FunctionName=self.function_name,
                InvocationType='Event',
                Payload=json_dumps(warmer_payload)
            )

            if response.get('message', None) == 'Lambda was warmed.':
                return True

        except Exception as e:
            logger.error(
                'invoker_err function=%s reason=%s', self.function_name, e, exc_info=True
            )

            return False

    async def execute_warm_functions(self, warmer_payload, concurrent_warmers):
        logger.info(
            f"""
            execute_warm_functions
            function_name={self.function_name}
            warmer_payload={warmer_payload}
            concurrent_warmers={concurrent_warmers}
            """
        )
        aio_lambda = AioLambda()

        tasks = [
            self.invoke_lambda(aio_lambda, warmer_payload)
            for _ in range(1, concurrent_warmers)
        ]

        # Check result of the tasks
        _, _ = await asyncio.wait(
            tasks, return_when=asyncio.ALL_COMPLETED
        )

        await aio_lambda.close_instance()

        logger.info(f'Successfuly warmed Lambdas using {self.function_name}')
        return 'Lambda has warmed'

    def execute_step(self, step, concurrent_warmers):
        logger.info(f'Executing step index: {step.index}')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        warmer_payload = self.distribute_step_load(step, concurrent_warmers)

        # Check result of the tasks
        _ = loop.run_until_complete(
            self.execute_warm_functions(warmer_payload, concurrent_warmers)
        )

        loop.close()

    def distribute_step_load(self, step, concurrent_warmers):
        warmer_payload = BASE_WARMER_PAYLOAD

        lambdas = []
        for lambda_ in step.lambdas_load:
            lambdas.append({
                "function_name": lambda_["function_name"],
                "concurrency": int(lambda_["load"] / concurrent_warmers)
            })

        warmer_payload["body"]["lambdas"] = lambdas

        return warmer_payload
