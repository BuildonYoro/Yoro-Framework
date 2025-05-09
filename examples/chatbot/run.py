import os

import litellm
from agents import Solution, SolutionConfig

from dotenv import load_dotenv
litellm.set_verbose = True

load_dotenv()

if os.environ.get("OPENAI_BASE_URL") is None:
    os.environ["OPENAI_BASE_URL"] = ""
if os.environ.get("OPENAI_API_KEY") is None:
    os.environ["OPENAI_API_KEY"] = ""


solution = Solution(config=SolutionConfig("examples/chatbot/config.json"))
solution.run()
