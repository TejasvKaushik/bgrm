from flask import Flask, request, send_file, render_template
from rembg import remove
from PIL import Image
from io import BytesIO
import os
from waitress import serve


app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    if '.' not in filename:
        return False
    
    name, extension = filename.rsplit('.', 1)
    
    if extension.lower() not in ALLOWED_EXTENSIONS:
        return False
        
    return True

@app.route("/", methods=['GET', 'POST'])
def rawdogging_this():
    if request.method == 'POST':
        if 'file' not in request.files: 
            return 'No file uploaded', 400
        
        file = request.files['file']
        if file.filename == '':
            return 'No file selected', 400
        
        if file and allowed_file(file.filename):
            try:
                input_image = Image.open(file.stream)
                output_image = remove(input_image, post_process_mask=True)
                img_io = BytesIO()
                output_image.save(img_io, 'PNG')
                img_io.seek(0)

                return send_file(img_io, mimetype="image/png", as_attachment=True, download_name=f"{file.filename.rsplit('.', 1)[0]}_bgremoved.png")
            except Exception as e:
                return f'Error processing image: {e}', 500
        else:
            return 'Invalid file type. Only image files are allowed.', 400
    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    serve(app, host="0.0.0.0", port=port)