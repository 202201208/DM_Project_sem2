import os
from flask import Flask, redirect, render_template, request, send_file, after_this_request, session
from werkzeug.utils import secure_filename
import cv2

from image_encryption import encrypt_image, decrypt_image
from utils import allowed_file
from image_processing import apply_kernal, negative_img, reflecting_img, resize_img, rotate_img, scale_img, shearing_img, translate_img

UPLOAD_FOLDER = 'static/uploads'
DOWNLOAD_FOLDER = 'static/downloads'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or "$(hdKY(@H51Mgk*%^sd"

def get_cookie(request):
    mode = request.cookies.get("mode")
    if(mode == "dark"):
        return 1
    else:
        return 0
    
@app.route("/")
def home():
  return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/togglemode")
def darkmode():
  dark = session.get("theme")
  if dark == "dark":
      session["theme"] = "light"
  else:
      session["theme"] = "dark"
  url = request.referrer
  return redirect(url)

@app.route("/tools")
def tools():
    return render_template("tools.html")

@app.route("/learn")
def learn():
    return redirect("/learn/introduction")

@app.route("/learn/introduction")
def learn_intro():
    return render_template("learn/introduction.html")

@app.route("/learn/encryption")
def learn_encryption():
    return render_template("learn/encryption.html")

@app.route("/learn/embossing")
def learn_embossing():
    return render_template("learn/embossing.html")

@app.route("/learn/enhancement")
def learn_enhancement():
    return render_template("learn/enhancement.html")

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

@app.route("/tools/scaling", methods=['GET', 'POST'])
def scaling():
  if(request.method == "POST"):
    if 'file' not in request.files:
      return render_template("notFound.html")
    file = request.files['file']
    fx = float(request.form.get("fx"))
    fy = float(request.form.get("fy"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      scale_img(img, fx, fy, path)
      return render_template("tools/scaling.html",output=True, original_img=filename, output_img=filename, action_path="scaling")
    else:
       return render_template("tools/scaling.html", output=False, action_path="scaling")
  return render_template("tools/scaling.html", output=False, action_path="scaling")  

@app.route("/tools/resizing", methods=['GET', 'POST'])
def resizing():
  if(request.method == "POST"):
    if 'file' not in request.files:
      return render_template("notFound.html")
    file = request.files['file']
    width = int(request.form.get("width"))
    height = int(request.form.get("height"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      resize_img(img, width, height, path)
      return render_template("tools/resizing.html",output=True, original_img=filename, output_img=filename, action_path="resizing")
    else:
       return render_template("tools/resizing.html", output=False, action_path="resizing")
  return render_template("tools/resizing.html", output=False, action_path="resizing")  

@app.route("/tools/translate", methods=['GET', 'POST'])
def translate():
  if(request.method == "POST"):
    if 'file' not in request.files:
      return render_template("notFound.html")
    file = request.files['file']
    tx = int(request.form.get("tx"))
    ty = int(request.form.get("ty"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      translate_img(img, tx, ty, path)
      return render_template("tools/translate.html",output=True, original_img=filename, output_img=filename, action_path="translate")
    else:
       return render_template("tools/translate.html", output=False, action_path="translate")
  return render_template("tools/translate.html", output=False, action_path="translate")

@app.route("/tools/rotate", methods=['GET', 'POST'])
def rotate():
  if(request.method == "POST"):
    if 'file' not in request.files:
      return render_template("notFound.html")
    file = request.files['file']
    x = int(request.form.get("x"))
    y = int(request.form.get("y"))
    deg = float(request.form.get("deg"))
    scale = float(request.form.get("scale"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      rotate_img(img, x, y, deg, scale, path)
      return render_template("tools/rotate.html",output=True, original_img=filename, output_img=filename, action_path="rotate")
    else:
       return render_template("tools/rotate.html", output=False, action_path="rotate")
  return render_template("tools/rotate.html", output=False, action_path="rotate")

@app.route("/tools/shearing", methods=['GET', 'POST'])
def shearing():
  if(request.method == "POST"):
    if 'file' not in request.files:
      return render_template("notFound.html")
    file = request.files['file']
    sx = float(request.form.get("sx"))
    sy = float(request.form.get("sy"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      shearing_img(img, sx, sy, path)
      return render_template("tools/shearing.html",output=True, original_img=filename, output_img=filename, action_path="shearing")
    else:
       return render_template("tools/shearing.html", output=False, action_path="shearing")
  return render_template("tools/shearing.html", output=False, action_path="shearing")

@app.route("/tools/reflecting", methods=['GET', 'POST'])
def reflecting():
  if(request.method == "POST"):
    if 'file' not in request.files:
      return render_template("notFound.html")
    file = request.files['file']
    f = int(request.form.get("flip"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      reflecting_img(img, f, path)
      return render_template("tools/reflecting.html",output=True, original_img=filename, output_img=filename, action_path="reflecting")
    else:
       return render_template("tools/reflecting.html", output=False, action_path="reflecting")
  return render_template("tools/reflecting.html", output=False, action_path="reflecting")

@app.route("/tools/negative", methods=['GET', 'POST'])
def negative():
  if(request.method == "POST"):
    if 'file' not in request.files:
      return render_template("notFound.html")
    file = request.files['file']
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      negative_img(img, path)
      return render_template("tools/negative.html",output=True, original_img=filename, output_img=filename, action_path="negative")
    else:
       return render_template("tools/negative.html", output=False, action_path="negative")
  return render_template("tools/negative.html", output=False, action_path="negative")

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

app.run(debug=True, port=3000)