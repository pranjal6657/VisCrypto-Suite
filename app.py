from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
from logic import generate_shares, decrypt_shares_digitally
import shutil
import logging

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
app.secret_key = "super_secret"

logging.basicConfig(level=logging.INFO)

if os.path.exists(app.config['UPLOAD_FOLDER']):
    shutil.rmtree(app.config['UPLOAD_FOLDER'])
os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html', mode='home')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'file' not in request.files: return "No file"
    file = request.files['file']
    if file.filename == '': return "No filename"
    
    # 1. NEW: Get the optimization mode from the form
    # Default to 'text' if not specified
    optim_mode = request.form.get('optimization', 'text') 

    filename = secure_filename("secret_input.png")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # 2. Pass the mode to the logic function
    if generate_shares(filepath, app.config['UPLOAD_FOLDER'], mode=optim_mode):
        return render_template('index.html', 
                               mode='encrypt_success', 
                               share1='static/uploads/share1.png', 
                               share2='static/uploads/share2.png')
    else:
        return "Encryption Failed"

@app.route('/decrypt', methods=['POST'])
def decrypt():
    if 'share1' not in request.files or 'share2' not in request.files: return "Missing files"
    s1 = request.files['share1']
    s2 = request.files['share2']

    path1 = os.path.join(app.config['UPLOAD_FOLDER'], 'upload_s1.png')
    path2 = os.path.join(app.config['UPLOAD_FOLDER'], 'upload_s2.png')
    s1.save(path1)
    s2.save(path2)

    result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'recovered_secret.png')
    
    if decrypt_shares_digitally(path1, path2, result_path):
        return render_template('index.html', 
                               mode='decrypt_success',  # This triggers the tab switch
                               result='static/uploads/recovered_secret.png')
    return "Decryption Failed"

@app.route('/download/<filename>')
def download_file(filename):
    response = send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

if __name__ == '__main__':
    app.run(debug=True)