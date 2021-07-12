# Author: Savindi Wijenayaka
# Date: 13.07.2021
 
import logging

import azure.functions as func
import azure.durable_functions as df


async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)
    opperation = req.params["op"]
    data = req.get_json() # Type: dict
    data["opperation"] = opperation
    instance_id = await client.start_new(req.route_params["functionName"], None, data)
    logging.info(f"Started orchestration with ID = '{instance_id}'.")
    return client.create_check_status_response(req, instance_id)
