

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} # , 'gif', 'webp'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    

def get_cookie(request):
    mode = request.cookies.get("mode")
    if(mode == "dark"):
        return 1
    else:
        return 0
