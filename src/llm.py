"""
Module: llm.py

Provides factory functions to initialize the Groq Language Model instance
and construct the LangChain processing pipeline.
"""

import logging
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from config import GROQ_API_KEY, GROQ_FALLBACK_KEYS, MODEL_NAME, MODEL_TEMPERATURE
from src.prompts import SYSTEM_PROMPT


def build_llm(model: str = None, temperature: float = None, api_key: str = None) -> ChatGroq:
    """
    Instantiates a single ChatGroq model using the provided credentials.
    """
    model = model or MODEL_NAME
    temperature = temperature if temperature is not None else MODEL_TEMPERATURE
    api_key = api_key or GROQ_API_KEY

    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY is not set. "
            "Add it to your .env file or as an environment variable."
        )
    return ChatGroq(model=model, temperature=temperature, api_key=api_key)


def build_chain(primary_llm: ChatGroq):
    """
    Constructs the LangChain pipeline by binding the system prompt, message history,
    user input, and any defined fallback LLMs to ensure continuous operation.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])
    
    # Generate fallback LLMs if backup keys are provided in .env
    fallback_llms = []
    for key in GROQ_FALLBACK_KEYS:
        try:
            backup_llm = build_llm(api_key=key)
            fallback_llms.append(prompt | backup_llm)
        except Exception as e:
            logging.warning(f"Failed to initialize fallback LLM: {e}")

    primary_chain = prompt | primary_llm
    
    # If backups exist, bind them so LangChain automatically fails over on error
    if fallback_llms:
        primary_chain = primary_chain.with_fallbacks(fallback_llms)
        
    return primary_chain
