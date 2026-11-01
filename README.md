# Stock Check with Gemini Function Calling

A short Python script that shows how function calling works with the Google Gemini API. A shop owner asks a question in plain English ("How much maize flour do we have?"), the model decides to look up the stock, and the script runs a Python function that returns the answer.

## What it does

1. Describes a function called `get_stock_level` to the model.
2. Sends the question "How much maize flour do we have?".
3. The model replies with a request to call `get_stock_level` with a product name.
4. The script runs the function on a small simulated inventory and prints the result.

If the question does not need a stock lookup, the model answers normally and the script prints that answer.

## How function calling works

The model never runs code. It only asks for a function to be called, and your own program does the work:

| Step | Who does it | What happens |
|---|---|---|
| 1 | Your script | Sends the question and a description of `get_stock_level` |
| 2 | The model | Decides the function is needed and returns its name and arguments |
| 3 | Your script | Runs `get_stock_level` and gets the result |

Because your code runs the function, you stay in control. The model only sees the result if you send it back, and this script does not.

## The parts of the code

| Part | What it does |
|---|---|
| `tools` | Tells the model the function's name, what it does, and its input (`product_name`, a required text value) |
| `inventory` | A dictionary that stands in for a database. A real system would query SQLite or an API |
| `get_stock_level()` | Looks up the product, ignoring capital letters and extra spaces, and returns a message |
| `generate_content(...)` | Sends the question and the tool description to Gemini |
| `response.function_calls` | The list of function calls the model asked for. It is empty when the model answers directly |

The function returns one of three messages:

- `<product>: <quantity> units in stock.` when the product is in stock.
- `<product> is currently out of stock.` when the quantity is 0.
- `Product '<product>' not found in the system.` when it is not in the inventory.

## Setup

1. Install Python 3.9 or newer.
2. Install the libraries:
   ```
   pip install -r requirements.txt
   ```
3. Get a free API key from [Google AI Studio](https://aistudio.google.com).
4. Copy `.env.example` to `.env` and put your key in it:
   ```
   GEMINI_API_KEY=your-key-here
   ```
   Do not use quotes or spaces around `=`.

## Run it

```
python stock_check.py
```

Expected output:

```
Function called: get_stock_level({'product_name': 'maize flour'})
Result: maize flour: 120 units in stock.
```

The product name inside the brackets comes from the model, so its capital letters or spacing can differ slightly. The result does not change, because the function ignores capital letters.

## Try other questions

Change the text after `contents=` in `stock_check.py`:

| Question | What you should see |
|---|---|
| Do we have sugar? | `sugar is currently out of stock.` (the name may appear as the model wrote it) |
| How much salt do we have? | `Product 'salt' not found in the system.` |
| What is the capital of Kenya? | No function call. The model's normal answer is printed |

## Limits

- The inventory is simulated and held in the script.
- The script stops after running the function. It does not send the result back to the model to get a written reply.
- It handles one function call and one question, with no error handling or retries. If the Gemini service is busy (error 503), run it again.

## Notes

- Model names change over time. If you see a "model not found" error, copy a current model name from Google AI Studio and update the `model=` line.
- The free tier has rate limits, and content sent on the free tier can be used to improve Google's products. Do not send private information.
- Never share your API key or upload your `.env` file.
