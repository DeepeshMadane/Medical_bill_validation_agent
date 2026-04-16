from utils.llm import generate_gemini_api

def decide_next_step(state):
    prompt = f"""
You are an AI agent controlling a medical bill processing system.

Current state:
- Has OCR text: {bool(state.get("text"))}
- Has parsed bill: {bool(state.get("bill"))}
- Has results: {bool(state.get("results"))}

Available actions:
1. ocr → extract text from image
2. parse → extract structured data
3. process → validate bill using tariff
4. end → finish

Decide the NEXT BEST ACTION.

Rules:
- If no text → choose "ocr"
- If text exists but no bill → choose "parse"
- If bill exists but no results → choose "process"
- If everything done → choose "end"

Return ONLY one word:
ocr / parse / process / end
"""

    response = generate_gemini_api(prompt)

    if isinstance(response, dict):
        decision = response.get("output", "").strip().lower()
    else:
        decision = response.strip().lower()

    return decision