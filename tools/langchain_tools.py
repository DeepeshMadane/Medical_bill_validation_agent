from langchain.tools import tool
from tools.ocr_tool import extract_text
from tools.parser_tool import parse_bill
from tools.rag_tool import search_tariff
from tools.compare_tool import compare_cost


# -------------------------------
# OCR TOOL
# -------------------------------
@tool
def ocr_tool(image_path: str):
    """Extract text from hospital bill image"""
    return extract_text(image_path)


# -------------------------------
# PARSER TOOL
# -------------------------------
@tool
def parser_tool(text: str):
    """Convert raw OCR text into structured bill JSON"""
    return parse_bill(text)


# -------------------------------
# RAG TOOL
# -------------------------------
@tool
def rag_tool(input_data: str):
    """
    Input: service and hospital
    Example: "MRI in Metro Hospital"
    Returns tariff info
    """
    service, hospital = input_data.split("|")
    return search_tariff(service.strip(), hospital.strip())


# -------------------------------
# COMPARE TOOL
# -------------------------------
@tool
def compare_tool(input_data: str):
    """
    Input: billed_cost|retrieved_text
    """
    billed, retrieved = input_data.split("|", 1)
    return compare_cost(int(billed), retrieved)