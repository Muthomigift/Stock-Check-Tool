import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise SystemExit("No API key found. Add GEMINI_API_KEY=your-key to your .env file.")

client = genai.Client(api_key=api_key)

tools = [{
    "function_declarations": [{
        "name": "get_stock_level",
        "description": "Get the current stock quantity for a product at Kamau Stores",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "The name of the product to check",
                }
            },
            "required": ["product_name"],
        },
    }]
}]

# Simulate a database lookup (in a production system, this queries SQLite or an API)
inventory = {
    "maize flour": 120,
    "wheat flour": 85,
    "rice": 200,
    "sugar": 0,
    "cooking oil": 45,
}


def get_stock_level(product_name):
    product = product_name.lower().strip()
    if product in inventory:
        qty = inventory[product]
        if qty == 0:
            return f"{product_name} is currently out of stock."
        return f"{product_name}: {qty} units in stock."
    return f"Product '{product_name}' not found in the system."


response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="How much maize flour do we have?",
    config={"tools": tools},
)

if response.function_calls:
    call = response.function_calls[0]
    result = get_stock_level(call.args["product_name"])
    print(f"Function called: {call.name}({call.args})")
    print(f"Result: {result}")
else:
    print(response.text)