
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

from src.agents.base_agent import BaseAgent
load_dotenv()

class BaseLLMAgent(BaseAgent):

    def __init__(self):

        os.environ["GOOGLE_API_KEY"] = (
            os.getenv("GOOGLE_API_KEY")
        )

        self.model = init_chat_model(
            "google_genai:gemini-2.5-flash"
        )