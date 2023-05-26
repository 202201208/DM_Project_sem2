import os
from flask import Flask, make_response, redirect, render_template, request, send_file, after_this_request
from werkzeug.utils import secure_filename
import cv2

from image_encryption import encrypt_image, decrypt_image
from utils import allowed_file, get_cookie
from image_processing import apply_kernal

UPLOAD_FOLDER = 'static/uploads'
DOWNLOAD_FOLDER = 'static/downloads'



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
# app.secret_key = 'secret_key'




def convertGray(filename):
    img = cv2.imread(f"static/uploads/{filename}")
    processedImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f"static/downloads/{filename}", processedImg)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/darkmode")
def darkmode():
  resp = make_response('Setting the cookie') 
  resp.set_cookie('mode','dark')
  return redirect(request.referrer)

@app.route("/lightmode")
def lightmode():
  resp = make_response('Setting the cookie') 
  resp.set_cookie('mode','light')
  return redirect(request.referrer)

@app.route("/tools")
def tools():
    return render_template("tools.html")

@app.route("/learn")
def learn():
    return redirect("/learn/introduction")

@app.route("/learn/introduction")
def intro():
    mode = get_cookie(request)
    return render_template("introduction.html", mode=mode)

@app.route("/tools/encryption", methods=['GET', 'POST'])
def encryption():
  if(request.method == "POST"):
    if 'file' not in request.files:
      return render_template("notFound.html")
    file = request.files['file']
    key = request.form.get("key")
    encrypt = int(request.form.get("encrypt"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      if(encrypt == 1):
        encrypt_image(img, path, key)
      else:
        decrypt_image(img, path, key)
      return render_template("tools/encryption.html",output=True, original_img=filename, output_img=filename, action_path="encryption")
    else:
       return render_template("tools/encryption.html", output=False, action_path="encryption")
  return render_template("tools/encryption.html", output=False, action_path="encryption")

@app.route("/tools/applykernel", methods=['GET', 'POST'])
def applykernel():
  mat = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
  if(request.method == "POST"):
    
    if 'file' not in request.files:
      return render_template("notFound.html")
    file = request.files['file']
    for i in range(3):
       for j in range(3):
          mat[i][j] = float(request.form.get(f"mat{i}{j}"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      apply_kernal(img, mat, path)
      return render_template("tools/kernel.html",output=True, original_img=filename, output_img=filename, action_path="applykernel", mat=mat)
    else:
       return render_template("tools/kernel.html", output=False, action_path="applykernel", mat=mat)
  return render_template("tools/kernel.html", output=False, action_path="applykernel", mat=mat)

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
    return send_file(downloads, download_name=filename, as_attachment=True )
    

@app.errorhandler(404)
def not_found(e):
   return render_template("notFound.html", e=e)

@app.errorhandler(500)
def internal_error(e):
   return render_template("notFound.html", e=e)
app.run(debug=True, port=3000)