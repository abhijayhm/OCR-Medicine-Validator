from flask import Flask, render_template, request
import pytesseract
from PIL import Image
import json
from datetime import datetime
from transformers import pipeline

import json

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

API_KEY = "<YOUR API KEY HERE>"
from huggingface_hub import InferenceClient

client = InferenceClient(api_key=API_KEY)


def query_online_model(prompt):
    """
    Queries the online model API with the given prompt and returns the response.
    """
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    completion = client.chat.completions.create(
        model="Qwen/Qwen2.5-Coder-32B-Instruct", 
        messages=messages, 
        max_tokens=500
    )

    print(completion.choices[0].message.content)
    return json.loads(completion.choices[0].message.content)

print(__name__)
app = Flask(__name__)

# Load JSON data
with open('medicines.json', 'r') as file:
    medicines = json.load(file)
# print(medicines, type(medicines))
@app.route('/')
def upload_form():
    # decorator is same as adding some code before
    return render_template('upload.html')
    # and or after this

@app.route('/upload', methods=['POST'])
def process_upload():
    uploaded_file = request.files['file']
    if uploaded_file:
        # Perform OCR
        image = Image.open(uploaded_file)
        extracted_text = pytesseract.pytesseract.image_to_string(image)
        print(extracted_text)

        # Use Llama 3 for structured extraction
        prompt = f"""This is OCR string: `{extracted_text}`
Extract medicine info for the following structure and give only the JSON as response; write as a json loadable string. don't prepend or append ```json or anything:
{{
  "name": "",
  "marketer": "",
  "expiry_date": ""
}}"""
        llama_response = query_online_model(prompt)
        # return llama response
        
        # Extract JSON from the online model's response
        if llama_response:
            structured_data = llama_response

            # Validate against the JSON database
            result = validate_data(structured_data, medicines)
            return render_template('result.html', result=result)
    # return r
    return render_template('result.html', result={"status": "Error", "details": "No file uploaded."})


def validate_data(data, medicines):
    """
    Validates extracted medicine data against the JSON database.
    """
    for med in medicines['tablets']:
        if (med['name'] == data['name'] or  
            med['marketer'] == data['marketer']):
            try:
                if datetime.strptime(med['expiry_date'], '%Y-%m-%d') >= datetime.now():
                    return {"status": "Valid", "details": data}
            except:
                return {"status": "Valid but expiry not known", "details": data}
    return {"status": "Invalid", "details": data}

if __name__ == '__main__':
    app.run(debug=True)
