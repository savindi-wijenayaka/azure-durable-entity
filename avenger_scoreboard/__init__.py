# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import azure.durable_functions as df


def entity_function(context: df.DurableEntityContext):
    current_value = context.get_state(lambda: {"total_combos": 0, "total_wins": 0})
    operation = context.operation_name
    logging.info(f"current value is: {current_value}")
    if operation == "add":
        data = context.get_input()
        current_value["total_combos"] += data["combos_executed"]
        current_value["total_wins"] += data["win"]
        context.set_state(current_value)
    elif operation == "reset":
        current_value = None
        context.set_state(current_value)
    elif operation == "get":
        context.set_result(current_value)
    elif operation == "delete":
        context.destruct_on_exit()


main = df.Entity.create(entity_function)
