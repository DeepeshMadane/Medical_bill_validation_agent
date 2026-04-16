from utils.llm import generate_gemini_api
from tools.ocr_tool import extract_text
from tools.parser_tool import parse_bill
from tools.rag_tool import search_tariff
from tools.compare_tool import compare_cost


def agent_pipeline(image_path, retriever):
    
    # Step 1: OCR
    text = extract_text(image_path)
    print("OCR TEXT:\n", text)

    # Step 2: Parse
    bill = parse_bill(text)

    results = []

    for item in bill["items"]:
        service = item["service"]
        billed = item["billed_cost"]

        # Step 3: RAG
        retrieved = search_tariff(retriever, service, bill["hospital"])

        # Step 4: Compare
        analysis = compare_cost(billed, retrieved)

        results.append({
            "service": service,
            "billed": billed,
            **analysis
        })

    return results