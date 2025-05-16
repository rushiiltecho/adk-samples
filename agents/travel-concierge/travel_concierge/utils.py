from datetime import datetime
import logging
from typing import Union
from types import FunctionType
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.invocation_context import InvocationContext
import requests

def setup_logger():
    class CustomFormatter(logging.Formatter):
        def format(self, record):
            prefix = '\n' + '=' * 50 + '\n'
            suffix = '\n' + '=' * 50 + '\n'
            
            if record.levelno == logging.INFO:
                prefix = '\n' + '-' * 50 + '\n'
                suffix = '\n' + '-' * 50 + '\n'
            elif record.levelno == logging.DEBUG:
                prefix = '\n' + '*' * 50 + '\n'
                suffix = '\n' + '*' * 50 + '\n'
            elif record.levelno == logging.ERROR:
                prefix = '\n' + '#' * 50 + '\n'
                suffix = '\n' + '#' * 50 + '\n'
                
            return prefix + super().format(record) + suffix

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter('%(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger

logger = setup_logger()

def _get_agent_log(agent_data):
    def get_tool_name(tool):
        if callable(tool):  # For function type instances
            return tool.__name__
        else:  # For object type instances
            return getattr(tool, 'name', str(tool))  # Try to get 'name' attribute, fallback to string representation

    return {
        "model": agent_data.get("model",""),
        "agent_name": agent_data.get("name","unknown"),
        "tools": [get_tool_name(i) for i in agent_data.get("tools",[])],
        "global_instruction": agent_data.get("global_instruction",""),
        "instruction": agent_data.get("instruction",""),
        "agent_description": agent_data.get("description",""),
        "sub_agents": agent_data.get("sub_agents",""),
    }

# utility function
def make_json_serializable(obj):
    """Recursively convert non-serializable types to serializable ones."""
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [make_json_serializable(i) for i in obj]
    elif isinstance(obj, set):
        return list(obj)
    elif callable(obj):
        return obj.__name__ if hasattr(obj, '__name__') else str(obj)
    elif hasattr(obj, '__dict__'):
        return make_json_serializable(obj.__dict__)
    else:
        return obj

def _get_log_data(callback_context:InvocationContext, event_type="before_agent") -> dict:
    callback_dict = callback_context.__dict__
    logger.info(f"CALLBACK DICT: {callback_dict}")
    invocation_context = callback_context.__dict__.get("_invocation_context").model_dump(exclude=["agent"])
    logger.info(f"Invocation DICT: {invocation_context}")
    agent_information = callback_context.__dict__.get("_invocation_context").agent.model_dump(exclude=["sub_agents","parent_agent"])
    logger.info(f"AGENT INFO: {agent_information}")
    sub_agents = [i.model_dump(exclude=["parent_agent","sub_agents"]) for i in callback_context.__dict__.get("_invocation_context").agent.sub_agents] or []
    logger.info(f"SUB AGENTS: {sub_agents}")
    agent_log= {}
    # if "agent" in event_type:
    agent_data = agent_information #callback_dict.get("_invocation_context").agent.model_dump(exclude="sub_agents")
    agent_data["sub_agents"] = sub_agents
    # logger.info(f"TOOL CONTEXT PRINTING:{agent_data.__dict__.keys()} \n\n {agent_data}")
    agent_log = _get_agent_log(agent_data)
    session_data = invocation_context.get("session",{})#callback_dict.get("_invocation_context").model_dump(exclude=["agent"]).get("session",{})
    log_entry = {
        "invocation_id": invocation_context.get("invocation_id",""),
        "event_type": f"{event_type}",
        "log_timestamp": datetime.now().isoformat(),
        "user_input": {
            "text": [p.text for p in callback_context.user_content.parts],
            "role": callback_context.user_content.role
        },
        "session_type":session_data
    }
    if "agent" in event_type:
        log_entry["agent_details"] = agent_log or {},

    return make_json_serializable(log_entry)

def log_data(callback_context:InvocationContext, event_type:str):
    log_data = _get_log_data(callback_context=callback_context,event_type=event_type)
    try:
        requests.post("http://127.0.0.1:3000/log/", json=log_data)
    except Exception as e:
        print(f"Logging failed: {e}")


def get_dictionary_from_context(callback_context:InvocationContext):
    callback_dict = callback_context.__dict__
    logger.info(f"CALLBACK DICT: {callback_dict}")
    invocation_context = callback_context.__dict__.get("_invocation_context").model_dump(exclude=["agent"])
    logger.info(f"Invocation DICT: {invocation_context}")
    agent_information = callback_context.__dict__.get("_invocation_context").agent.model_dump(exclude=["sub_agents","parent_agent"])
    logger.info(f"AGENT INFO: {agent_information}")
    sub_agents = [i.model_dump(exclude=["parent_agent","sub_agents"]) for i in callback_context.__dict__.get("_invocation_context").agent.sub_agents] or []
    logger.info(f"SUB AGENTS: {sub_agents}")
    return {
        "agent": {
            **agent_information,
            "sub_agents": sub_agents
        },
        "invocation_context": invocation_context
    }

def log_agent(callback_context:InvocationContext, type_of_callback=""):
    context = get_dictionary_from_context(callback_context)
    agent_name = context["agent"].get("name","").split("_agent")[0]
    precedence , callback_type = type_of_callback.split("_")[:2]
    log_data(callback_context,f"{precedence}_{agent_name}_{callback_type}")

