import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLMFormatter:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv(
                "OPENROUTER_API_KEY"
            ),
            base_url="https://openrouter.ai/api/v1"
        )

    def format_response(
        self,
        query,
        worker,
        data
    ):

        prompt = f"""
You are CampusAgent.

User Query:
{query}

Worker Used:
{worker}

Retrieved Data:
{data}

Generate a clean professional answer.

Rules:
- Do not mention JSON.
- Do not mention databases.
- Use headings.
- Use bullet points.
- Be concise.
- Present information clearly.
"""

        response = (
            self.client.chat.completions.create(
                model="openai/gpt-oss-120b:free",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        )

        return (
            response
            .choices[0]
            .message
            .content
        )