from flask import Flask, request, jsonify
import easyocr
import base64
import io
from PIL import Image

app = Flask(__name__)
reader = easyocr.Reader(['en','vi'])  

@app.route('/', methods=['POST'])
def ocr():
    try:
        data = request.json
        if 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400
        
        image_data = base64.b64decode(data['image'])
        image = Image.open(io.BytesIO(image_data))
        
        result = reader.readtext(image)
        extracted_text = [text[1] for text in result]  
        
        return jsonify({'text': extracted_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
