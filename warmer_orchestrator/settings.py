
CONCURRENT_WARMERS = 20
WARMER_FUNCTION_NAME = "warmer"
WAITING_TIME = 60 # 5 minutes
CONCURRENT_EXECUTIONS = {
    'start': 500,
    'step': 500,
    'end': 3000,
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
