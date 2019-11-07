from step import StepGenerator


CONCURRENT_EXECUTIONS = {
    'start': 3000,
    'step': 500,
    'end': 6000,
}


LAMBDAS_PROPORTION = [
    {
        "function_name": "login",
        "load_proportion": 0.50
    },
    {
        "function_name": "signup",
        "load_proportion": 0.30
    },
    {
        "function_name": "list-posts",
        "load_proportion": 0.20
    }
]


def test_number_of_steps():
    step_generator = StepGenerator()
    numbers_of_steps = step_generator.number_of_steps(
        CONCURRENT_EXECUTIONS
    )

    assert numbers_of_steps == 7


def test_step_generator():
    step_generator = StepGenerator()
    steps = step_generator.generate(LAMBDAS_PROPORTION, CONCURRENT_EXECUTIONS)

    step = steps[0]
    lambdas_load = step.lambdas_load

    assert step.index == 0
    assert step.step_objective == 3000
    assert lambdas_load[0]["function_name"] == "login"
    assert lambdas_load[0]["load"] == 1500

    step = steps[2]
    lambdas_load = step.lambdas_load

    assert step.index == 2
    assert step.step_objective == 4000
    assert lambdas_load[1]["function_name"] == "signup"
    assert lambdas_load[0]["load"] == 2000
