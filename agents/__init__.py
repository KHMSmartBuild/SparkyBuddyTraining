# Original
from excel_gpt_update import analyze_text
from excel_gpt_update import check_info
from function_explanations import generate_function_explanations
from function_explanations import store_function_explanations
from main_train import main
from agents.Template_scripts.app import is_valid_int
from agents.Template_scripts.app import get_command
from agents.Template_scripts.app import map_command_synonyms
from agents.Template_scripts.app import execute_command
from agents.Template_scripts.app import get_text_summary
from agents.Template_scripts.app import get_hyperlinks
from agents.Template_scripts.app import shutdown
from agents.Template_scripts.app import start_agent
from agents.Template_scripts.app import message_agent
from agents.Template_scripts.app import list_agents
from agents.Template_scripts.app import delete_agent
from agents.Template_scripts.args import parse_arguments
from agents.Template_scripts.audio_text import read_audio_from_file
from agents.Template_scripts.audio_text import read_audio
from agents.Template_scripts.chat import create_chat_message
from agents.Template_scripts.chat import generate_context
from agents.Template_scripts.chat import chat_with_ai
from agents.Template_scripts.data_ingestion import configure_logging
from agents.Template_scripts.data_ingestion import ingest_directory
from agents.Template_scripts.data_ingestion import main
from agents.Template_scripts.evaluate_code import evaluate_code
from agents.Template_scripts.execute_code import execute_python_file
from agents.Template_scripts.execute_code import execute_shell
from agents.Template_scripts.execute_code import we_are_running_in_a_docker_container
from agents.Template_scripts.file_operations import check_duplicate_operation
from agents.Template_scripts.file_operations import log_operation
from agents.Template_scripts.file_operations import split_file
from agents.Template_scripts.file_operations import read_file
from agents.Template_scripts.file_operations import ingest_file
from agents.Template_scripts.file_operations import write_to_file
from agents.Template_scripts.file_operations import append_to_file
from agents.Template_scripts.file_operations import delete_file
from agents.Template_scripts.file_operations import search_files
from agents.Template_scripts.google_search import google_search
from agents.Template_scripts.google_search import google_official_search
from agents.Template_scripts.image_gen import generate_image
from agents.Template_scripts.image_gen import generate_image_with_hf
from agents.Template_scripts.image_gen import generate_image_with_dalle
from agents.Template_scripts.improve_code import improve_code
from agents.Template_scripts.llm_utils import call_ai_function
from agents.Template_scripts.llm_utils import create_chat_completion
from agents.Template_scripts.llm_utils import create_embedding_with_ada
from agents.Template_scripts.logs import Logger
from agents.Template_scripts.logs import TypingConsoleHandler
from agents.Template_scripts.logs import ConsoleHandler
from agents.Template_scripts.logs import AutoGptFormatter
from agents.Template_scripts.logs import remove_color_codes
from agents.Template_scripts.logs import print_assistant_thoughts
from agents.Template_scripts.machine_learning import ConstructionMLModel
from agents.Template_scripts.natural_language_generator import NaturalLanguageGenerator
from agents.Template_scripts.prompt import get_prompt
from agents.Template_scripts.prompt import construct_prompt
from agents.Template_scripts.question_answerer import QuestionAnswerer
from agents.Template_scripts.setup import prompt_user
from agents.Template_scripts.spinner import Spinner
from agents.Template_scripts.text_processor import TextProcessor
from agents.Template_scripts.times import get_datetime
from agents.Template_scripts.token_counter import count_message_tokens
from agents.Template_scripts.token_counter import count_string_tokens
from agents.Template_scripts.utils import clean_input
from agents.Template_scripts.utils import validate_yaml_file
from agents.Template_scripts.web_playwright import scrape_text
from agents.Template_scripts.web_playwright import scrape_links
from agents.Template_scripts.web_requests import is_valid_url
from agents.Template_scripts.web_requests import sanitize_url
from agents.Template_scripts.web_requests import check_local_file_access
from agents.Template_scripts.web_requests import get_response



# excel_gpt_update module
from excel_gpt_update import analyze_text, check_info

# function_explanations module
from function_explanations import generate_function_explanations, store_function_explanations

# main_train module
from main_train import main

# agents.Template_scripts.app module
from agents.Template_scripts.app import (
    is_valid_int,
    get_command,
    map_command_synonyms,
    execute_command,
    get_text_summary,
    get_hyperlinks,
    shutdown,
    start_agent,
    message_agent,
    list_agents,
    delete_agent,
)

# agents.Template_scripts.args module
from agents.Template_scripts.args import parse_arguments

# agents.Template_scripts.audio_text module
from agents.Template_scripts.audio_text import read_audio_from_file, read_audio

# agents.Template_scripts.chat module
from agents.Template_scripts.chat import create_chat_message, generate_context, chat_with_ai

# agents.Template_scripts.data_ingestion module
from agents.Template_scripts.data_ingestion import configure_logging, ingest_directory, main

# agents.Template_scripts.evaluate_code module
from agents.Template_scripts.evaluate_code import evaluate_code

# agents.Template_scripts.execute_code module
from agents.Template_scripts.execute_code import (
    execute_python_file,
    execute_shell,
    we_are_running_in_a_docker_container,
)

# agents.Template_scripts.file_operations module
from agents.Template_scripts.file_operations import (
    check_duplicate_operation,
    log_operation,
    split_file,
    read_file,
    ingest_file,
    write_to_file,
    append_to_file,
    delete_file,
    search_files,
)

# agents.Template_scripts.google_search module
from agents.Template_scripts.google_search import google_search, google_official_search

# agents.Template_scripts.image_gen module
from agents.Template_scripts.image_gen import generate_image, generate_image_with_hf, generate_image_with_dalle

# agents.Template_scripts.improve_code module
from agents.Template_scripts.improve_code import improve_code

# agents.Template_scripts.llm_utils module
from agents.Template_scripts.llm_utils import call_ai_function, create_chat_completion, create_embedding_with_ada

# agents.Template_scripts.logs module
from agents.Template_scripts.logs import (
    Logger,
    TypingConsoleHandler,
    ConsoleHandler,
    AutoGptFormatter,
    remove_color_codes,
    print_assistant_thoughts,
)

# agents.Template_scripts.machine_learning module
from agents.Template_scripts.machine_learning import ConstructionMLModel

# agents.Template_scripts.natural_language_generator module
from agents.Template_scripts.natural_language_generator import NaturalLanguageGenerator

# agents.Template_scripts.prompt module
from agents.Template_scripts.prompt import get_prompt, construct_prompt

# agents.Template_scripts.question_answerer module
from agents.Template_scripts.question_answerer import QuestionAnswerer

# agents.Template_scripts.setup module
from agents.Template_scripts.setup import prompt_user

# agents.Template_scripts.spinner module
from agents.Template_scripts.spinner import Spinner

# agents.Template_scripts.text_processor module
from agents.Template_scripts.text_processor import TextProcessor

# agents.Template_scripts.times module
from agents.Template_scripts.times import get_datetime

# agents.Template_scripts.token_counter module
from agents.Template_scripts.token_counter import count_message_tokens, count_string_tokens

# agents.Template_scripts.utils module
from agents.Template_scripts.utils import clean_input, validate_yaml_file

# agents.Template_scripts.web_playwright module
from agents.Template_scripts.web_playwright import scrape_text, scrape_links

# agents.Template_scripts.web_requests module
from agents.Template_scripts.web_requests import (
    is_valid_url,
    sanitize_url,
    check_local_file_access,
    get,
)
