
import trafilatura
import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def clean_html_to_txt(html):
    try:  
        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False,
            favor_recall=False,
        )
        if extracted:
            return extracted
    except Exception as e:
        raise e


def get_response_from_llm(user_prompt, system_prompt, model):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in the environment or .env file. Please define GROQ_API_KEY in your .env file.")

    # Map invalid/openai models to a valid Groq model (e.g., llama-3.1-8b-instant)
    if "openai" in model or "gpt-oss" in model:
        model = "llama-3.1-8b-instant"

    groq_client = Groq(api_key=api_key)
    chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            model=model,
        )
    return chat_completion.choices[0].message.content

