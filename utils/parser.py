import os
from google import genai

def analyze_blueprint(api_key, pdf_path):
    client = genai.Client(api_key=api_key)
    uploaded_file = client.files.upload(file=pdf_path)
    
    prompt = """
    You are an expert Civil Quantity Surveyor and Estimator working for Aishwaryam Group.
    Analyze this uploaded construction drawing/document with 100% mathematical precision.
    Extract room-wise dimensions, compute square footages, and provide structured material quantity takeoffs.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[uploaded_file, prompt]
    )
    
    return response.text