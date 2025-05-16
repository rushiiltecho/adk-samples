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


# ---------- Inspiration Agent ----------
# def before_inspiration(callback_context:CallbackContext):
#     log_data(callback_context,"before_inspiration_agent")
#     # pass

# def before_poi_agent(callback_context:CallbackContext):
#     log_data(callback_context,"before_poi_agent")
#     # pass

# def before_place_agent(callback_context:CallbackContext):
#     log_data(callback_context, "before_place_agent")
#     # pass

# def after_inspiration(callback_context:CallbackContext):
#     log_data(callback_context,"after_inspiration_agent")
#     # pass

# def after_poi_agent(callback_context:CallbackContext):
#     log_data(callback_context,"after_poi_agent")
#     # pass

# def after_place_agent(callback_context:CallbackContext):
#     log_data(callback_context, "after_place_agent")
#     # pass

# # logger= setup_logger()

# def before_inspiration_tool(tool:BaseTool, args: Dict[str, Any], tool_context: CallbackContext):
#     tool_dict = {key: value for key, value in tool.__dict__.items()} #if not key.startswith('_')}
#     logger.info(f"\n\n{'-'*60}\nTOOL DICT: {tool_dict}\n{'-'*60}\n\n")
#     log_data(tool_context, "before_inspiration_tool")
#     # pass

# def after_inspiration_tool(tool:BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response:Union[Awaitable[Optional[dict]], Optional[dict]]):
#     log_data(tool_context, "after_inspiration_tool")
#     tool_dict = {key: value for key, value in tool.__dict__.items()} #if not key.startswith('_')}
#     logger.info(f"\n\n{'-'*60}\nTOOL DICT: {tool_dict}\n{'-'*60}\n\n")

# def before_inspiration_model(callback_context: CallbackContext, llm_request: LlmRequest):
#     d = {key: value for key, value in llm_request.__dict__.items()} #if not key.startswith('_')}
#     logger.info(f"\n\n{'-'*60}\nLLM REQUEST DICT: {d}\n{'-'*60}\n\n")
#     # Save LLM request to file
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     with open(f"llm_request_{timestamp}.txt", "w") as f:
#         f.write(str(d))
#     log_data(callback_context,"before_inspiration_model")

# def after_inspiration_model(callback_context: CallbackContext, llm_response: LlmResponse):
#     d = {key: value for key, value in llm_response.__dict__.items()} #if not key.startswith('_')}
#     logger.info(f"\n\n{'-'*60}\nLLM RESPONSE DICT: {d}\n{'-'*60}\n\n")
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     with open(f"llm_response_{timestamp}.txt", "w") as f:
#         f.write(str(d))
#     log_data(callback_context,"after_inspiration_model")

# def before_place_model(callback_context: CallbackContext, llm_request: LlmRequest):
#     log_data(callback_context,"before_place_model")

# def after_place_model(callback_context: CallbackContext, llm_response: LlmResponse):
#     log_data(callback_context,"after_place_model")

# def before_poi_model(callback_context: CallbackContext, llm_request: LlmRequest):
#     log_data(callback_context,"before_poi_model")

# def after_poi_model(callback_context: CallbackContext, llm_response: LlmResponse):
#     log_data(callback_context,"after_poi_model")

# # ---------------------------------------------------------------

# def before_planning_agent(callback_context:CallbackContext):
#     log_data(callback_context, "before_planning_agent")


# def after_planning_agent(callback_context:CallbackContext):
#     log_data(callback_context, "after_planning_agent")

    
# def before_booking_agent(callback_context:CallbackContext):
#     log_data(callback_context, "before_booking_agent")


# def after_booking_agent(callback_context:CallbackContext):
#     log_data(callback_context, "after_booking_agent")


# def before_pre_trip_agent(callback_context:CallbackContext):
#     log_data(callback_context, "before_pre_trip_agent")


# def after_pre_trip_agent(callback_context:CallbackContext):
#     log_data(callback_context, "after_pre_trip_agent")


# def before_in_trip_agent(callback_context:CallbackContext):
#     log_data(callback_context, "before_in_trip_agent")


# def after_in_trip_agent(callback_context:CallbackContext):
#     log_data(callback_context, "after_in_trip_agent")


# def before_post_trip_agent(callback_context:CallbackContext):
#     log_data(callback_context, "before_post_trip_agent")


# def after_post_trip_agent(callback_context:CallbackContext):
#     log_data(callback_context, "after_post_trip_agent")


# def before_flight_search_agent(callback_context:CallbackContext):
#     log_data(callback_context, "before_flight_search_agent")


# def after_flight_search_agent(callback_context:CallbackContext):
#     log_data(callback_context, "after_flight_search_agent")


# def before_flight_seat_selection_agent(callback_context:CallbackContext):
#     log_data(callback_context, "before_flight_seat_selection_agent")


# def after_flight_seat_selection_agent(callback_context:CallbackContext):
#     log_data(callback_context, "after_flight_seat_selection_agent")


# def before_hotel_search_agent(callback_context:CallbackContext):
#     log_data(callback_context, "before_hotel_search_agent")


# def after_hotel_search_agent(callback_context:CallbackContext):
#     log_data(callback_context, "after_hotel_search_agent")


# def before_itenerary_agent(callback_context:CallbackContext):
#     log_data(callback_context, "before_itenerary_agent")


# def after_itenerary_agent(callback_context:CallbackContext):
#     log_data(callback_context, "after_itenerary_agent")


# def before_create_reservation_agent(callback_context:CallbackContext):
#     log_data(callback_context, "before_create_reservation_agent")


# def after_create_reservation_agent(callback_context:CallbackContext):
#     log_data(callback_context, "after_create_reservation_agent")


# def before_payment_choice_agent(callback_context:CallbackContext):
#     log_data(callback_context, "before_payment_choice_agent")


# def after_payment_choice_agent(callback_context:CallbackContext):
#     log_data(callback_context, "after_payment_choice_agent")


# def before_process_payment_agent(callback_context:CallbackContext):
#     log_data(callback_context, "before_process_payment_agent")


# def after_process_payment_agent(callback_context:CallbackContext):
#     log_data(callback_context, "after_process_payment_agent")
    

# def before_hotel_room_selection_agent(callback_context:CallbackContext):
#     log_data(callback_context, "before_hotel_room_selection_agent")


# def after_hotel_room_selection_agent(callback_context:CallbackContext):
#     log_data(callback_context, "after_hotel_room_selection_agent")


# def before_what_to_pack_agent(callback_context:CallbackContext):
#     log_data(callback_context, "before_what_to_pack_agent")


# def after_what_to_pack_agent(callback_context:CallbackContext):
#     log_data(callback_context, "after_what_to_pack_agent")



# def before_<xyz>_agent(callback_context:CallbackContext):
#     log_data(callback_context, "before_<xyz>_agent")


# def after_<xyz>_agent(callback_context:CallbackContext):
#     log_data(callback_context, "after_<xyz>_agent")


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