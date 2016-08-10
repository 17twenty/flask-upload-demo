import os
from utils import json_response
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug import secure_filename

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['png', 'gif', 'jpeg', 'jpg'])

tmpl_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'static')

app = Flask(__name__, template_folder=tmpl_dir,
            static_folder=static_dir, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Limit uploads to 16MB. They'll get an
# Error 413 Request entity too large
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    """
    allowed_file just checks the acceptable extensions
      it could be extended to check the fileheader/mimetype
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/v/<item>")
def uploaded_file(item):
    return send_from_directory(app.config['UPLOAD_FOLDER'], item)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    files = dict(
        zip(os.listdir(app.config['UPLOAD_FOLDER']),
            ["/v/{}".format(k) for k in os.listdir(app.config['UPLOAD_FOLDER'])]))
    return render_template('/file_list.html', file_list=files)


@app.route("/upload", methods=['POST'])
def upload():
    """
    Plugin should be able to upload here and give us back a URL/item ID for us
      to reuse to download and populate using AJAX magic
    """
    file = None
    if 'file' in request.files:
        file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return json_response(
            message="Upload successful",
            result="/v/{}".format(filename)
        )
    return json_response(
        message="Invalid filename or extension (jpg, png, gif)",
        status_code=500
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
