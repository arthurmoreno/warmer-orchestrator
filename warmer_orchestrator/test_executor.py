from executor import Executor


CONCURRENT_WARMERS = 10

class StepMock:
    index = 0
    step_objective = 2100
    lambdas_load = [
        {'function_name': 'login', 'load': 750},
        {'function_name': 'singup', 'load': 750},
        {'function_name': 'list-posts', 'load': 600}
    ]


def test_execute_step():

    step = StepMock()

    executor = Executor("my-warmer")
    warmer_payload = executor.distribute_step_load(
        step, CONCURRENT_WARMERS
    )

    lambdas = warmer_payload["body"]["lambdas"]

    assert lambdas[0]["concurrency"] == 75
    assert lambdas[2]["concurrency"] == 60
