import json

from openai import AzureOpenAI

from app.core.config import get_settings
from app.tools.property_tools import TOOL_DEFINITIONS, execute_tool


SYSTEM_PROMPT = """
You are Aqarmind, an AI-powered real estate advisory assistant.
Use approved tools when structured property data, calculations, or grounded
knowledge are needed. Never invent property availability, financial guarantees,
or investment returns. Clearly distinguish estimates from confirmed facts.
""".strip()


def ai_is_configured() -> bool:
    s = get_settings()
    return all([s.azure_openai_endpoint, s.azure_openai_api_key, s.azure_openai_deployment])


def get_client() -> AzureOpenAI:
    s = get_settings()
    if not ai_is_configured():
        raise RuntimeError("Azure OpenAI configuration is incomplete.")

    return AzureOpenAI(
        azure_endpoint=s.azure_openai_endpoint,
        api_key=s.azure_openai_api_key,
        api_version=s.azure_openai_api_version,
    )


def generate_chat_answer(user_message: str) -> str:
    s = get_settings()
    client = get_client()
    messages: list[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    first = client.chat.completions.create(
        model=s.azure_openai_deployment,
        messages=messages,
        tools=TOOL_DEFINITIONS,
        tool_choice="auto",
        max_tokens=s.max_output_tokens,
        temperature=0.2,
    )

    assistant_message = first.choices[0].message
    if not assistant_message.tool_calls:
        return assistant_message.content or ""

    messages.append(assistant_message)

    for tool_call in assistant_message.tool_calls:
        arguments = json.loads(tool_call.function.arguments or "{}")
        result = execute_tool(tool_call.function.name, arguments)
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, default=str),
            }
        )

    final = client.chat.completions.create(
        model=s.azure_openai_deployment,
        messages=messages,
        max_tokens=s.max_output_tokens,
        temperature=0.2,
    )
    return final.choices[0].message.content or ""
