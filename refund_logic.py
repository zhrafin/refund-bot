import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def refund_policy_helper(user_input):
    prompt = f"""
You are a refund policy assistant. Use the following rules to determine if a product is returnable:

1. Returns are accepted within 7 days of delivery.
2. The item must be unused and in its original packaging.
3. Sale items and specific categories like cosmetics, lingerie, and personal care items are not returnable.

Now, based on the customer's message, decide whether their product is eligible for return. Be clear, polite, and helpful.

Customer says: "{user_input}"
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response['choices'][0]['message']['content']
