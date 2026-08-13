from app.services.database import search_properties
from app.services.mortgage import calculate_mortgage
from app.services.search import retrieve_knowledge


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_properties",
            "description": "Search structured property inventory using buyer filters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "area": {"type": "string"},
                    "bedrooms": {"type": "integer"},
                    "max_price_aed": {"type": "number"},
                    "property_type": {"type": "string"},
                    "developer": {"type": "string"},
                },
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_mortgage",
            "description": "Calculate an illustrative mortgage payment using deterministic math.",
            "parameters": {
                "type": "object",
                "properties": {
                    "property_price_aed": {"type": "number"},
                    "down_payment_percent": {"type": "number"},
                    "annual_interest_rate": {"type": "number"},
                    "tenure_years": {"type": "integer"},
                },
                "required": ["property_price_aed"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "retrieve_knowledge_context",
            "description": "Retrieve grounded context from the Aqarmind knowledge index.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "top_k": {"type": "integer", "minimum": 1, "maximum": 10},
                },
                "required": ["question"],
                "additionalProperties": False,
            },
        },
    },
]


def execute_tool(name: str, arguments: dict):
    if name == "search_properties":
        return search_properties(**arguments)
    if name == "calculate_mortgage":
        return calculate_mortgage(
            property_price_aed=arguments["property_price_aed"],
            down_payment_percent=arguments.get("down_payment_percent", 20),
            annual_interest_rate=arguments.get("annual_interest_rate", 4.5),
            tenure_years=arguments.get("tenure_years", 25),
        )
    if name == "retrieve_knowledge_context":
        return retrieve_knowledge(
            question=arguments["question"],
            top_k=arguments.get("top_k", 5),
        )
    raise ValueError(f"Unsupported tool: {name}")
