# Author: Savindi Wijenayaka
# Date: 13.07.2021

import json
import logging

import azure.durable_functions as df
import azure.durable_functions.models.utils.entity_utils as utils
import azure.functions as func


async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)
    entity_name, entity_key = (
        req.route_params["entityName"],
        req.route_params["entityKey"],
    )
    entity_identifier = utils.EntityId(entity_name, entity_key)

    entity_state_response = await client.read_entity_state(entity_identifier)

    if not entity_state_response.entity_exists:
        return func.HttpResponse("Entity not found", status_code=404)

    return func.HttpResponse(
        json.dumps(
            {
                "entity": entity_name,
                "key": entity_key,
                "state": entity_state_response.entity_state,
            }
        )
    )
