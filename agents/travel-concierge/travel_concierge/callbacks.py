from .utils import log_data, setup_logger, logger, log_agent
from datetime import datetime
import json
import logging
import os
from typing import Awaitable, Dict, Any, Optional, Union

from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.llm_agent import LlmResponse, LlmRequest
from google.adk.sessions.state import State
from google.adk.tools import ToolContext
from google.adk.tools import BaseTool


def before_agent(callback_context: CallbackContext):
    log_agent(callback_context,"before_agent")

def after_agent(callback_context:CallbackContext):
    log_agent(callback_context, "after_agent")

def before_tool(tool:BaseTool, args: Dict[str, Any], tool_context: CallbackContext):
    # tool_dict = {key: value for key, value in tool.__dict__.items()} #if not key.startswith('_')}
    # logger.info(f"\n\n{'-'*60}\nTOOL DICT: {tool_dict}\n{'-'*60}\n\n")
    log_agent(tool_context, "before_tool")

def after_tool(tool:BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response:Union[Awaitable[Optional[dict]], Optional[dict]]):
    log_agent(tool_context, "after_tool")
    # tool_dict = {key: value for key, value in tool.__dict__.items()} #if not key.startswith('_')}
    # logger.info(f"\n\n{'-'*60}\nTOOL DICT: {tool_dict}\n{'-'*60}\n\n")

def before_model(callback_context: CallbackContext, llm_request: LlmRequest):
    # d = {key: value for key, value in llm_request.__dict__.items()} #if not key.startswith('_')}
    # logger.info(f"\n\n{'-'*60}\nLLM REQUEST DICT: {d}\n{'-'*60}\n\n")
    # # Save LLM request to file
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # with open(f"llm_request_{timestamp}.txt", "w") as f:
    #     f.write(str(d))
    log_agent(callback_context,"before_model")

def after_model(callback_context: CallbackContext, llm_response: LlmResponse):
    # d = {key: value for key, value in llm_response.__dict__.items()} #if not key.startswith('_')}
    # logger.info(f"\n\n{'-'*60}\nLLM RESPONSE DICT: {d}\n{'-'*60}\n\n")
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # with open(f"llm_response_{timestamp}.txt", "w") as f:
    #     f.write(str(d))
    log_agent(callback_context,"after_model")