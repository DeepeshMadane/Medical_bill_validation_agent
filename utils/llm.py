import requests

def generate_gemini_api(prompt, text=""):
    url = "http://192.168.0.89:9004/generate_text_PIMS"
    data = {"prompt": prompt, "ocr_text": text}

    try:
        res = requests.post(url, json=data, timeout=30)
        return res.json()
    except Exception as e:
        return {"error": str(e)}