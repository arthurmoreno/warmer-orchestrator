import time

from executor import Executor
from step import StepGenerator
from settings import (
    LAMBDAS_PROPORTION,
    CONCURRENT_EXECUTIONS,
    WARMER_FUNCTION_NAME,
    CONCURRENT_WARMERS,
    WAITING_TIME
)


def routine():
    step_generator = StepGenerator()
    steps = step_generator.generate(LAMBDAS_PROPORTION, CONCURRENT_EXECUTIONS)

    executor = Executor(WARMER_FUNCTION_NAME)
    last_step = None

    for step in steps:
        executor.execute_step(step, CONCURRENT_WARMERS)

        time.sleep(WAITING_TIME)
        last_step = step

    while True:
        executor.execute_step(last_step, CONCURRENT_WARMERS)

        time.sleep(WAITING_TIME)


if __name__ == '__main__':
    routine()
