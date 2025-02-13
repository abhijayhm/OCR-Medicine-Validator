# OCR Medicine Validator

This project is a Flask-based web application that:  
1. Extracts text from uploaded images using Tesseract OCR.  
2. Uses an AI model from Hugging Face (Qwen2.5-Coder-32B-Instruct) to structure the extracted data.  
3. Validates the extracted medicine details against a predefined JSON database.  

## Prerequisites

- Python 3.x installed  
- Tesseract OCR installed (`C:\Program Files\Tesseract-OCR\tesseract.exe` for Windows)  
- A Hugging Face API key  

## Installation

1. Clone the repository:  
   ```sh
   git clone https://github.com/yourusername/OCR-Medicine-Validator.git
   cd OCR-Medicine-Validator
   ```

2. Install dependencies:  
   ```sh
   pip install -r requirements.txt
   ```

3. Set up Tesseract OCR:  
   - Ensure that Tesseract OCR is installed on your system.  
   - Update the `pytesseract.pytesseract.tesseract_cmd` path in `app.py` if necessary.  

4. Run the Flask application:  
   ```sh
   python app.py
   ```

5. Open the application in your browser:  
   ```
   http://127.0.0.1:5000/
   ```

6. If above steps don't work, refer to steps.txt

## Usage

- Upload an image containing medicine details.  
- The system extracts and processes the text.  
- The extracted data is structured and validated against a predefined JSON database.  
- The validation result is displayed.  

## Files and Structure

```
OCR-Medicine-Validator/
│── app.py              # Main Flask application
│── medicines.json      # JSON database of medicines
│── templates/
│   ├── upload.html     # File upload page
│   ├── result.html     # Display validation results
│── requirements.txt    # Python dependencies
│── README.md           # Project documentation
```

## Dependencies

The required dependencies are listed in `requirements.txt`. To install them, run:  
```sh
pip install -r requirements.txt
```

## API Key

You need a Hugging Face API key to use the AI model. Replace `API_KEY` in `app.py` with your own key. 