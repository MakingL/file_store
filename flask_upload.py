# -*- coding: utf-8 -*-
from datetime import datetime
import os
import os.path
from flask import Flask, request, jsonify, send_from_directory, abort

UPLOAD_FOLDER = './upload_files'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024


@app.route('/')
def hello_world():
    return abort(404)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'code': "403", 'msg': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'code': "401", 'msg': 'No selected file'})
        try:
            if file and allowed_file(file.filename):
                origin_file_name = file.filename
                filename = origin_file_name

                # filename = secure_filename(file.filename)

                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # timestamp = request.args.get('timestamp')
                timestamp = datetime.now()
                print("POST a file: {}  time: {}".format(
                    os.path.join(app.config['UPLOAD_FOLDER'], filename),
                    timestamp))
                return jsonify({'code': "200", "msg": "OK"})
            else:
                return jsonify({'code': "502", 'msg': 'File not allowed'})
        except Exception as e:
            return jsonify({'code': "503", 'filename': '', 'msg': 'Error occurred'})
    else:
        return jsonify({'code': "402", 'filename': '', 'msg': 'Method not allowed'})


@app.route('/delete', methods=['GET'])
def delete_file():
    if request.method == 'GET':
        filename = request.args.get('filename')
        if filename is None:
            return jsonify({'code': "403", 'msg': 'No file name'})
        try:
            full_name = os.path.join(UPLOAD_FOLDER, filename)

            if os.path.exists(full_name):
                os.remove(full_name)
                # timestamp = request.args.get('timestamp')
                timestamp = datetime.now()
                print("Deleted a file: {}   time: {}".format(
                    full_name,
                    timestamp
                ))
                return jsonify({'code': "200", 'msg': 'OK'})
            else:
                return jsonify({'code': "502", 'msg': 'File not exist'})
        except Exception as e:
            return jsonify({'code': "503", 'msg': 'File deleted error'})

    else:
        return jsonify({'code': "402", 'msg': 'Method not allowed'})


@app.route("/download/<path:filename>", methods=['GET'])
def downloader(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


@app.route("/getlist", methods=['GET'])
def getlist():
    file_names = [name for name in os.listdir(UPLOAD_FOLDER)
                  if os.path.isfile(os.path.join(UPLOAD_FOLDER, name))]

    # Get all dirs
    dir_names = [name for name in os.listdir(UPLOAD_FOLDER)
                 if os.path.isdir(os.path.join(UPLOAD_FOLDER, name))]
    return jsonify({'code': "200", 'files': file_names, "directors": dir_names})


if __name__ == '__main__':
    app.run(
        # debug=True,
        host="0.0.0.0",
        port=8089)
