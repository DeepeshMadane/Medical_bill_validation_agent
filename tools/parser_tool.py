import re
from langchain_core.output_parsers import JsonOutputParser
from utils.llm import generate_gemini_api


parser = JsonOutputParser()

def build_prompt(text: str):
    return f"""
You are an expert system that extracts tables from OCR text of hospital bills.

The text contains a TABLE with columns:
Sr No | Investigation | Charges

Your job:
- Extract ALL rows from the Investigation table
- Each row contains:
  - service name
  - billed cost
- Ignore header rows and totals

IMPORTANT:
- There are MULTIPLE rows → DO NOT return only one
- Extract EVERY row (1, 2, 3, 4, ...)
- Even if formatting is broken, reconstruct the table
- Fix OCR mistakes (e.g., Biood → Blood, HIV1&2 → HIV 1 & 2)

Example:
Input:
1 Blood Group 100.00
2 CBC (Complete Blood Count) 250.00

Output:
[
  {{"service": "Blood Group", "billed_cost": 100}},
  {{"service": "CBC", "billed_cost": 250}}
]

Now extract from this:

{text}

Return ONLY JSON:
{{
  "hospital": "hospital name",
  "items": [
    {{"service": "service name", "billed_cost": number}}
  ]
}}
"""

# 🔥 Safe JSON extractor (minimal)
def extract_json(text):
    start = text.find("{")
    end = text.rfind("}")
    
    if start != -1 and end != -1:
        return text[start:end+1]
    
    return text


def parse_bill(text: str):
    prompt = build_prompt(text)

    response = generate_gemini_api(prompt, text)

    if isinstance(response, dict) and "error" in response:
        print("LLM Error:", response["error"])
        return None

    # ✅ FIX HERE
    if isinstance(response, dict):
        raw_output = response.get("output", "")
    else:
        raw_output = response

    try:
        cleaned = extract_json(raw_output)

        try:
            return parser.parse(cleaned)
        except:
            import json
            return json.loads(cleaned)

    except Exception as e:
        print("Parsing failed:", raw_output)
        print("Error:", e)
        return None