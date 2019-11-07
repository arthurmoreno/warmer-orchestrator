import math


class StepGenerator:

    def number_of_steps(self, concurrent_executions):
        start = concurrent_executions['start']
        step = concurrent_executions['step']
        end = concurrent_executions['end']

        return math.ceil((end - start) / step) + 1

    def generate(self, lambdas_proportion, concurrent_executions):
        step_objective = concurrent_executions['start']
        steps = []

        for i in range(self.number_of_steps(concurrent_executions)):
            step = Step(i, step_objective, lambdas_proportion)
            steps.append(step)
            step_objective += concurrent_executions['step']

        return steps


class Step:
    index = None
    step_objective = None
    lambdas_load = []

    def __init__(self, i, step_objective, lambdas_proportion):
        self.index = i
        self.step_objective = step_objective

        self.generate_lambda_load(
            lambdas_proportion
        )

    def generate_lambda_load(self, lambdas_proportion):
        self.lambdas_load = []
        for lambda_proportion in lambdas_proportion:
            self.lambdas_load.append({
                "function_name": lambda_proportion["function_name"],
                "load": int(
                    self.step_objective * lambda_proportion["load_proportion"]
                )
            })
