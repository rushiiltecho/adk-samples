# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Callback functions for FOMC Research Agent."""

from datetime import datetime
import logging
import time

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest
from typing import Any, Dict
from google.adk.tools import BaseTool
from google.adk.agents.invocation_context import InvocationContext
import httpx
from customer_service.entities.customer import Customer
import requests
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

RATE_LIMIT_SECS = 60
RPM_QUOTA = 10


def rate_limit_callback(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> None:
    """Callback function that implements a query rate limit.

    Args:
      callback_context: A CallbackContext obj representing the active callback
        context.
      llm_request: A LlmRequest obj representing the active LLM request.
    """
    
    logging.info(f"\n\n{'-'*50}\n Model Before Callback:\n{callback_context.__dict__} \n{'-'*50}")
    log_entry = _get_log_data(callback_context, "before_model")
    logging.info(f"\n\n{'-'*50}\n Model Before LLM Requests :\n{llm_request.__dict__} \n{'-'*50}")

    try:
        requests.post("http://localhost:3000/log/", json=log_entry)
    except Exception as e:
        print(f"Logging failed: {e}")
    
    for content in llm_request.contents:
        for part in content.parts:
            if part.text=="":
                part.text=" "

    
    

    now = time.time()
    if "timer_start" not in callback_context.state:

        callback_context.state["timer_start"] = now
        callback_context.state["request_count"] = 1
        logger.debug(
            "rate_limit_callback [timestamp: %i, "
            "req_count: 1, elapsed_secs: 0]",
            now,
        )
        return

    request_count = callback_context.state["request_count"] + 1
    elapsed_secs = now - callback_context.state["timer_start"]
    logger.debug(
        "rate_limit_callback [timestamp: %i, request_count: %i,"
        " elapsed_secs: %i]",
        now,
        request_count,
        elapsed_secs,
    )

    if request_count > RPM_QUOTA:
        delay = RATE_LIMIT_SECS - elapsed_secs + 1
        if delay > 0:
            logger.debug("Sleeping for %i seconds", delay)
            time.sleep(delay)
        callback_context.state["timer_start"] = now
        callback_context.state["request_count"] = 1
    else:
        callback_context.state["request_count"] = request_count

    return


def lowercase_value(value):
    """Make dictionary lowercase"""
    if isinstance(value, dict):
        return (dict(k, lowercase_value(v)) for k, v in value.items())
    elif isinstance(value, str):
        return value.lower()
    elif isinstance(value, (list, set, tuple)):
        tp = type(value)
        return tp(lowercase_value(i) for i in value)
    else:
        return value


# Callback Methods
def before_tool(
    tool: BaseTool, args: Dict[str, Any], tool_context: CallbackContext
):

    logging.info(f"TOOL CONTEXT PRINTING:{tool_context.__dict__.keys()} \n\n {tool_context.__dict__}")
    # with open('temp.json', 'w') as f:
    #     json.dump(tool_context.__dict__, f, indent=4, default=str)
    log_entry = _get_log_data(tool_context, "before_tool")
    # i make sure all values that the agent is sending to tools are lowercase
    lowercase_value(args)
    logging.info(f"{'_'*200}\nLOG ENTRY: {log_entry}{'_'*200}")
    try:
        requests.post("http://localhost:3000/log/", json=log_entry)
    except Exception as e:
        print(f"Logging failed: {e}")

    # Check for the next tool call and then act accordingly.
    # Example logic based on the tool being called.
    if tool.name == "sync_ask_for_approval":
        amount = args.get("value", None)
        if amount <= 10:  # Example business rule
            return {
                "result": "You can approve this discount; no manager needed."
            }
        # Add more logic checks here as needed for your tools.

    if tool.name == "modify_cart":
        if (
            args.get("items_added") is True
            and args.get("items_removed") is True
        ):
            return {"result": "I have added and removed the requested items."}
    return None


def _get_agent_log(agent_data):
    return {
        "model": agent_data.model, #agent_data.get("model",""),
        "agent_name": agent_data.name,#agent_data.get("name","unknown"),
        "tools": [i.__name__ for i in agent_data.tools], #.get("tools",[])],
        "global_instruction": agent_data.global_instruction or "", #agent_data.get("global_instruction",""),
        "instruction": agent_data.instruction or "",
        "agent_description":agent_data.description or "" #agent_data.get("description","")
    }

def _get_tool_log(tool_data):
    return {

    }

# utility function
def make_json_serializable(obj):
    """Recursively convert sets to lists in a nested structure."""
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(i) for i in obj]
    elif isinstance(obj, set):
        return list(obj)
    else:
        return obj

def _get_log_data(callback_context:InvocationContext, event_type="before_agent") -> dict:
    callback_dict = callback_context.__dict__
    agent_log= {}
    # if "agent" in event_type:
    agent_data = callback_dict.get("_invocation_context").agent
    logging.info(f"TOOL CONTEXT PRINTING:{agent_data.__dict__.keys()} \n\n {agent_data}")
    agent_log = _get_agent_log(agent_data)
    session_data = callback_dict.get("_invocation_context").model_dump().get("session",{})
    session_log = session_data
    log_entry = {
        "event_type": f"{event_type}",
        "log_timestamp": datetime.now().isoformat(),
        "agent_details":agent_log or {},
        "user_input": {
            "text": [p.text for p in callback_context.user_content.parts],
            "role": callback_context.user_content.role
        },
        "session_type":session_log
    }
    return make_json_serializable(log_entry)

# checking that the customer profile is loaded as state.
def before_agent(callback_context: InvocationContext):
    logging.info(f"Agent Context: {callback_context.__dict__}")
    callback_dict = callback_context.__dict__
    logging.info(f"TYPEOF CALLBACK DICT{type(callback_dict)}\n\nCALLBACK DICT:{callback_dict}")
    if "customer_profile" not in callback_context.state:
        callback_context.state["customer_profile"] = Customer.get_customer(
            "123"
        ).to_json()
    
    # if callback_context.user_content.parts[0].text == "how are you today":
    #     callback_context.user_content.parts[0].text = "hi"
    # if callback_context.user_content.parts[0].text == "hi":
    #     callback_context.user_content.parts[0].text = "how are you today"
    # print(f"OUTPUT: {[i.__dict__ for i in callback_context.user_content.parts]}\n\n {callback_context.user_content.role}\n\n {callback_dict.get("_invocation_context").model_dump().get("agent")}")
    
    logger.info(callback_context.state["customer_profile"])
    
    log_entry=_get_log_data(callback_context,"before_agent")
    logging.info(f"LOG ENTRY: {log_entry}")
    try:
        requests.post("http://localhost:3000/log/", json=log_entry)
    except Exception as e:
        print(f"Logging failed: {e}")

async def after_agent_callback(callback_context: InvocationContext) -> None:
    log_entry = {
        "event_type": "after_agent",
        "timestamp": datetime.now().isoformat(),
        "agent_name": callback_context.agent.name,
        "agent_output": callback_context.agent.__dict__,
        "session_id": callback_context.session,
    }
    try:
        async with httpx.AsyncClient() as client:
            await client.post("http://localhost:3000/log/", json=log_entry)
    except Exception as e:
        print(f"Logging failed: {e}")