import os
from PIL import Image
from flask import Flask, jsonify, redirect, render_template, request, send_file, after_this_request, session
from werkzeug.utils import secure_filename
import cv2

from image_encryption import encrypt_image, decrypt_image
from image_steganography import decode_image, encode_image
from utils import allowed_file
from image_processing import apply_kernal, cannyedgedetector_img, embossing_img, gammatransformation_img, gaussianfilter_img, highpassfilter_img, histogramequalization_img, logtransformation_img, lowpassfilter_img, maxfilter_img, medianfilter_img, minfilter_img, negative_img, reflecting_img, resize_img, rotate_img, scale_img, shearing_img, translate_img

UPLOAD_FOLDER = 'static/uploads'
DOWNLOAD_FOLDER = 'static/downloads'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or "$(hdKY(@H51Mgk*%^sd"

def get_size(file_path, unit='bytes'):
    file_size = os.path.getsize(file_path)
    exponents_map = {'bytes': 0, 'kb': 1, 'mb': 2, 'gb': 3}
    if unit not in exponents_map:
        raise ValueError("Must select from \
        ['bytes', 'kb', 'mb', 'gb']")
    else:
        size = file_size / 1024 ** exponents_map[unit]
        return round(size, 3)
   
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

@app.route("/learn/whatisimage")
def learn_whatisimage():
    return render_template("learn/whatisimage.html")

@app.route("/learn/encryption")
def learn_encryption():
    return render_template("learn/encryption.html")

@app.route("/learn/embossing")
def learn_embossing():
    return render_template("learn/embossing.html")

@app.route("/learn/enhancement")
def learn_enhancement():
    return render_template("learn/enhancement.html")

@app.route("/learn/transformation")
def learn_transformation():
    return render_template("learn/transformation.html")

@app.route("/learn/noisereduction")
def learn_noisereduction():
    return render_template("learn/noisereduction.html")

@app.route("/learn/edgedetection")
def learn_edgedetection():
    return render_template("learn/edgedetection.html")

@app.route("/learn/steganography")
def learn_steganography():
    return render_template("learn/steganography.html")


@app.route("/tools/encryption", methods=['GET', 'POST'])
def encryption():
  if(request.method == "POST"):
    file = request.files['file']
    key = request.form.get("key")
    encrypt = int(request.form.get("encrypt"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 1.000):
        return jsonify({
          "output" : False,
          "action_path" : "encryption",
          "text" : False,
          "big_size" : True
        })
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      if(encrypt == 1):
        encrypt_image(img, path, key)
      else:
        decrypt_image(img, path, key)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "encryption",
        "text" : False
      })
    else:
      return jsonify({
        "output" : False,
        "action_path" : "encryption",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/encryption.html")

@app.route("/tools/applykernel", methods=['GET', 'POST'])
def applykernel():
  mat = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
  if(request.method == "POST"):
    
      
    file = request.files['file']
    for i in range(3):
       for j in range(3):
          try:
            mat[i][j] = float(request.form.get(f"mat{i}{j}"))
          except:
            return jsonify({
              "output" : False,
              "action_path" : "applykernel",
              "text" : False,
              "validData" : True
            })
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "applykernel",
          "text" : False,
          "big_size" : True
        })
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      apply_kernal(img, mat, path)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "applykernel",
        "text" : False
      })
    else:
      return jsonify({
        "output" : False,
        "action_path" : "applykernel",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/kernel.html")

@app.route("/tools/scaling", methods=['GET', 'POST'])
def scaling():
  if(request.method == "POST"):
    
      
    file = request.files['file']
    fx = float(request.form.get("fx"))
    fy = float(request.form.get("fy"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "scaling",
          "text" : False,
          "big_size" : True
        })
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      scale_img(img, fx, fy, path)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "scaling",
        "text" : False
      })
    else:
      return jsonify({
        "output" : False,
        "action_path" : "scaling",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/scaling.html")  

@app.route("/tools/resizing", methods=['GET', 'POST'])
def resizing():
  if(request.method == "POST"):
    
      
    file = request.files['file']
    width = int(request.form.get("width"))
    height = int(request.form.get("height"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "resizing",
          "text" : False,
          "big_size" : True
        })
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      resize_img(img, width, height, path)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "resizing",
        "text" : False
      })
    else:
      return jsonify({
        "output" : False,
        "action_path" : "resizing",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/resizing.html")  

@app.route("/tools/translate", methods=['GET', 'POST'])
def translate():
  if(request.method == "POST"):
    
      
    file = request.files['file']
    tx = int(request.form.get("tx"))
    ty = int(request.form.get("ty"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "translate",
          "text" : False,
          "big_size" : True
        })
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      translate_img(img, tx, ty, path)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "translate",
        "text" : False
      })
    else:
       return jsonify({
        "output" : False,
        "action_path" : "translate",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/translate.html")

@app.route("/tools/rotate", methods=['GET', 'POST'])
def rotate():
  if(request.method == "POST"):
    
      
    file = request.files['file']
    deg = float(request.form.get("deg"))
    scale = float(request.form.get("scale"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "rotate",
          "text" : False,
          "big_size" : True
        })
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      rotate_img(img, deg, scale, path)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "rotate",
        "text" : False
      })
    else:
       return jsonify({
        "output" : False,
        "action_path" : "rotate",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/rotate.html")

@app.route("/tools/shearing", methods=['GET', 'POST'])
def shearing():
  if(request.method == "POST"):
    
      
    file = request.files['file']
    sx = float(request.form.get("sx"))
    sy = float(request.form.get("sy"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "shearing",
          "text" : False,
          "big_size" : True
        })
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      shearing_img(img, sx, sy, path)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "shearing",
        "text" : False
      })
    else:
       return jsonify({
        "output" : False,
        "action_path" : "shearing",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/shearing.html")

@app.route("/tools/reflecting", methods=['GET', 'POST'])
def reflecting():
  if(request.method == "POST"):
    
      
    file = request.files['file']
    f = int(request.form.get("flip"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "reflecting",
          "text" : False,
          "big_size" : True
        })
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      reflecting_img(img, f, path)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "reflecting",
        "text" : False
      })
    else:
       return jsonify({
        "output" : False,
        "action_path" : "reflecting",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/reflecting.html")

@app.route("/tools/negative", methods=['GET', 'POST'])
def negative():
  if(request.method == "POST"):
    
      
    file = request.files['file']
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "negative",
          "text" : False,
          "big_size" : True
        })
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      negative_img(img, path)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "negative",
        "text" : False
      })
    else:
       return jsonify({
        "output" : False,
        "action_path" : "negative",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/negative.html")

@app.route("/tools/logtransformation", methods=['GET', 'POST'])
def logtransformation():
  if(request.method == "POST"):
    
      
    file = request.files['file']
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "logtransformation",
          "text" : False,
          "big_size" : True
        })
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      logtransformation_img(img, path)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "logtransformation",
        "text" : False
      })
    else:
       return jsonify({
        "output" : False,
        "action_path" : "logtransformation",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/logtransformation.html")

@app.route("/tools/gammatransformation", methods=['GET', 'POST'])
def gammatransformation():
  if(request.method == "POST"):
    
      
    file = request.files['file']
    g = float(request.form.get("g"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "gammatransformation",
          "text" : False,
          "big_size" : True
        })
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      gammatransformation_img(img, g, path)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "gammatransformation",
        "text" : False
      })
    else:
       return jsonify({
        "output" : False,
        "action_path" : "gammatransformation",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/gammatransformation.html")

@app.route("/tools/gaussianfilter", methods=['GET', 'POST'])
def gaussianfilter():
  if(request.method == "POST"):
    
      
    file = request.files['file']
    r = int(float(request.form.get("radius")))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "gaussianfilter",
          "text" : False,
          "big_size" : True
        })
      original_path = f"static/uploads/{filename}"
      path = f"static/downloads/{filename}"
      gaussianfilter_img(original_path,r,  path)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "gaussianfilter",
        "text" : False
      })
    else:
       return jsonify({
        "output" : False,
        "action_path" : "gaussianfilter",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/gaussianfilter.html")

@app.route("/tools/medianfilter", methods=['GET', 'POST'])
def medianfilter():
  if(request.method == "POST"):
    
      
    file = request.files['file']
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "medianfilter",
          "text" : False,
          "big_size" : True
        })
      original_path = f"static/uploads/{filename}"
      path = f"static/downloads/{filename}"
      medianfilter_img(original_path, path)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "medianfilter",
        "text" : False
      })
    else:
       return jsonify({
        "output" : False,
        "action_path" : "medianfilter",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/medianfilter.html")

@app.route("/tools/minfilter", methods=['GET', 'POST'])
def minfilter():
  if(request.method == "POST"):
    
      
    file = request.files['file']
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "minfilter",
          "text" : False,
          "big_size" : True
        })
      original_path = f"static/uploads/{filename}"
      path = f"static/downloads/{filename}"
      minfilter_img(original_path, path)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "minfilter",
        "text" : False
      })
    else:
       return jsonify({
        "output" : False,
        "action_path" : "minfilter",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/minfilter.html")

@app.route("/tools/maxfilter", methods=['GET', 'POST'])
def maxfilter():
  if(request.method == "POST"):
    
      
    file = request.files['file']
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "maxfilter",
          "text" : False,
          "big_size" : True
        })
      original_path = f"static/uploads/{filename}"
      path = f"static/downloads/{filename}"
      maxfilter_img(original_path, path)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "maxfilter",
        "text" : False
      })
    else:
       return jsonify({
        "output" : False,
        "action_path" : "maxfilter",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/maxfilter.html")

@app.route('/downloads/<path:filename>')
def download(filename):
    downloads = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    return send_file(downloads, download_name=filename, as_attachment=True )
    
@app.route("/tools/cannyedgedetector", methods=['GET', 'POST'])
def cannyedgedetector():
  if(request.method == "POST"):
    
      
    file = request.files['file']
    l = int(request.form.get("lower"))
    u = int(request.form.get("upper"))
    a = int(request.form.get("aperture"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "cannyedgedetector",
          "text" : False,
          "big_size" : True
        })
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      cannyedgedetector_img(img, l, u, a, path)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "cannyedgedetector",
        "text" : False
      })
    else:
       return jsonify({
        "output" : False,
        "action_path" : "cannyedgedetector",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/cannyedgedetector.html")

@app.route("/tools/embossing", methods=['GET', 'POST'])
def embossing():
  mat = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
  if(request.method == "POST"):
    
      
    file = request.files['file']
    for i in range(3):
       for j in range(3):
          try:
            mat[i][j] = int(float(request.form.get(f"mat{i}{j}")))
          except:
            return jsonify({
              "output" : False,
              "action_path" : "embossing",
              "text" : False,
              "validData" : True
            })
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "embossing",
          "text" : False,
          "big_size" : True
        })
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      embossing_img(img, mat, path)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "embossing",
        "text" : False
      })
    else:
       return jsonify({
        "output" : False,
        "action_path" : "embossing",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/embossing.html")

@app.route("/tools/steganography", methods = ['GET', 'POST'])
def steganography():
  if(request.method == "POST"):
    
      
    file = request.files['file']
    text = request.form.get("secret")
    encode = int(request.form.get("encode"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "steganography",
          "text" : False,
          "big_size" : True
        })
      img = f"static/uploads/{filename}"
      d_path = f"static/downloads/"
      if(encode == 1):
        output = encode_image(img, text, d_path, filename)
        return jsonify({
          "output" : True,
          "original_img" : filename,
          "output_img" : output,
          "action_path" : "steganography",
          "text" : False
        })
      else:
        secret = decode_image(img)
        if(secret == '%%%%%%%%%%'):
          return jsonify({
            "output" : False,
            "action_path" : "steganography",
            "text" : True,
            "msg" : "This Image is not Encoded"
          })
        return jsonify({
          "output" : False,
          "action_path" : "steganography",
          "text" : True,
          "msg" : "Decoded Text is Here",
          "secret" : secret
        })
    else:
       return jsonify({
        "output" : False,
        "action_path" : "steganography",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/steganography.html")

@app.route("/tools/lowpassfilter", methods=['GET', 'POST'])
def lowpassfilter():
  if(request.method == "POST"):
    
      
    file = request.files['file']
    radius = int(request.form.get("radius"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "lowpassfilter",
          "text" : False,
          "big_size" : True
        })
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      lowpassfilter_img(img, radius, path)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "lowpassfilter",
        "text" : False
      })
    else:
       return jsonify({
        "output" : False,
        "action_path" : "lowpassfilter",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/lowpassfilter.html")

@app.route("/tools/highpassfilter", methods=['GET', 'POST'])
def highpassfilter():
  if(request.method == "POST"):
    
      
    file = request.files['file']
    radius = int(request.form.get("radius"))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "highpassfilter",
          "text" : False,
          "big_size" : True
        })
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      highpassfilter_img(img, radius, path)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "highpassfilter",
        "text" : False
      })
    else:
       return jsonify({
        "output" : False,
        "action_path" : "highpassfilter",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/highpassfilter.html")

@app.route("/tools/histogramequalization", methods=['GET', 'POST'])
def histogramequalization():
  if(request.method == "POST"):
    
      
    file = request.files['file']
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      if(get_size(f"static/uploads/{filename}", 'mb') > 50.000):
        return jsonify({
          "output" : False,
          "action_path" : "histogramequalization",
          "text" : False,
          "big_size" : True
        })
      img = cv2.imread(f"static/uploads/{filename}")
      path = f"static/downloads/{filename}"
      histogramequalization_img(img, path)
      return jsonify({
        "output" : True,
        "original_img" : filename,
        "output_img" : filename,
        "action_path" : "histogramequalization",
        "text" : False
      })
    else:
       return jsonify({
        "output" : False,
        "action_path" : "histogramequalization",
        "text" : False,
        "validData" : True
      })
  return render_template("tools/histogramequalization.html")

@app.errorhandler(404)
def not_found(e):
   return render_template("notFound.html", e=e)

@app.route("/admin/clearfolders")
def clearuploads():
  all_files = os.listdir(UPLOAD_FOLDER)
  for f in all_files:
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'],f))
  all_files = os.listdir(DOWNLOAD_FOLDER)
  for f in all_files:
    os.remove(os.path.join(app.config['DOWNLOAD_FOLDER'],f))
  return redirect("/")

# if(__name__ == "__main__"):
#   app.run(debug=True)