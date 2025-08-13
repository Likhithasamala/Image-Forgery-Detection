from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from prediction import predict_result
from metadata import extract_metadata

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'venu/img/'

# Ensure necessary folders exist
for folder in ['venu', 'venu/img', 'venu/masks', 'venu/csv']:
    if not os.path.exists(folder):
        os.makedirs(folder)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Predict result using ELA and metadata
        prediction, confidence, ela_filename = predict_result(file_path)
        metadata = extract_metadata(file_path)
        
        # Build the URLs for original and ELA images
        original_image_url = url_for('static', filename=f'img/{filename}')
        ela_image_url = url_for('static', filename=f'img/{ela_filename}')

        return render_template('result.html', 
                               original_image_url=original_image_url, 
                               ela_image_url=ela_image_url, 
                               prediction=prediction, 
                               confidence=confidence, 
                               metadata=metadata)

if __name__ == '__main__':
    app.run(debug=True)
