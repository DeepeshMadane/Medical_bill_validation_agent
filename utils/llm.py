import requests

def generate_gemini_api(prompt, text=""):
    url = "your_url"
    data = {"prompt": prompt, "ocr_text": text}

    try:
        res = requests.post(url, json=data, timeout=30)
        return res.json()
    except Exception as e:
        return {"error": str(e)}
