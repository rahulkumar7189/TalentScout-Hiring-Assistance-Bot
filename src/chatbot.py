"""
Module: chatbot.py

Contains the main orchestrator class `TalentScoutBot`, which handles interactions
between the user input, the LangChain language model, and utility functions for
extracting underlying JSON data.
"""

from src.llm import build_llm, build_chain
from src.utils import extract_json, clean_response


class TalentScoutBot:
    """
    The main chatbot driver that encapsulates the LLM instance and conversational chain.
    It exposes a single method to process user inputs and return responses.
    """

    def __init__(self, model: str = None, temperature: float = None):
        """
        Initializes the Groq LLM and the LangChain pipeline.

        Args:
            model (str, optional): The name of the Groq model to use. Defaults to None (loads from config).
            temperature (float, optional): Model creativity setting. Defaults to None (loads from config).
        """
        try:
            self._llm = build_llm(model=model, temperature=temperature)
            self._chain = build_chain(self._llm)
        except EnvironmentError as exc:
            print(f"[TalentScoutBot] Init failed: {exc}")
            self._llm = None
            self._chain = None

    def get_response(self, user_input: str, chat_history: list) -> tuple[str, dict | None]:
        """
        Processes a user's chat input through the LLM and attempts to extract
        a concluding JSON payload if the interview is finished.

        Args:
            user_input (str): The raw text provided by the user.
            chat_history (list): A list of previous LangChain message objects.

        Returns:
            tuple[str, dict | None]: A tuple containing:
                - The bot's conversational text reply (cleaned of JSON if present).
                - A dictionary containing gathered candidate data, or None if the
                  interview is still ongoing or no data was extracted.
        """
        if self._chain is None:
            return (
                "⚠️ System error: LLM not initialised. "
                "Please ensure GROQ_API_KEY is correctly configured.",
                None,
            )

        try:
            # Pass the conversation context and new input to the LLM chain
            ai_msg = self._chain.invoke({
                "chat_history": chat_history,
                "input": user_input,
            })
            raw_text = ai_msg.content
            
            # Check if the LLM outputted the final JSON block
            extracted_data = extract_json(raw_text)
            
            # If JSON data was found, strip it out of the displayed reply
            response_text = clean_response(raw_text) if extracted_data else raw_text
            
            return response_text, extracted_data

        except Exception as exc:
            return f"I apologise, I encountered an error: {exc}", None
