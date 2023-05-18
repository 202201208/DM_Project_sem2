from io import BytesIO
import os
from flask import Flask, current_app, render_template, flash, request, send_file, after_this_request
from werkzeug.utils import secure_filename
import cv2

UPLOAD_FOLDER = 'static/uploads'
DOWNLOAD_FOLDER = 'static/downloads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.secret_key = 'secret_key'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convertGray(filename):
    img = cv2.imread(f"static/uploads/{filename}")
    processedImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f"static/downloads/{filename}", processedImg)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/toGrayScale", methods=['GET', 'POST'])
def grayScale():
    if(request.method == "POST"):
        if 'file' not in request.files:
            return render_template("notFound.html")
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            convertGray(filename)
            return render_template("downloadImage.html", filename=filename)
        
    return render_template("grayScale.html")

@app.route('/downloads/<path:filename>')
def download(filename):
    downloads = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    @after_this_request
    def remove_file(response):
        try:
            os.remove(os.path.join(app.config['DOWNLOAD_FOLDER'],filename))
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response

    # os.remove(os.path.join(app.config['DOWNLOAD_FOLDER'],filename))
    return send_file(downloads, download_name=filename, as_attachment=True )
    


app.run(debug=True, port=3000)