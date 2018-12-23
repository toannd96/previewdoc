# coding: utf-8
"""Docs."""
from flask import request, send_from_directory, make_response
from werkzeug import secure_filename
import json
import os
import cgi
import re
import requests
import datetime
import errno
from urlparse import urljoin
from config import BaseConfig


def allowed_file(filename):
    """Docs.

    Function check type file
    ---
    tags:
      - Checkfile
    parameters:
      - name: filename
        type: string
        description: file to upload
    responses:
      True:
        description: valid file format
      Fasle:
        description: invalid file format
    """
    return '.' in filename and \
           filename.split('.')[-1].lower() in BaseConfig.ALLOWED_EXTENSIONS


def convert_file(file_path):
    """Docs.

    # Author: Toannd

    # Function: Converting files using unoconv
    ---
    tags:
      - convert
    parameters:
      - name: filename
        type: string
        description: file to convert
    response:
        path to file convert with origin name
    """

    convert_folder = os.path.join(BaseConfig.CONVERT_FOLDER)
    file_name = file_path.rsplit(
        '/', 1)[1][:file_path.rsplit('/', 1)[1].rindex('.')] + '.pdf'  
    file_output_path = os.path.join(os.getcwd() + '/') \
        + convert_folder + '/' + file_name
    cmd = 'unoconv -f pdf --output=' + file_output_path + ' ' + file_path  

    _r = os.system(cmd)
    if int(_r) == 0:
        return True, file_name

    return False, ''


def _mkdir_upload_folder(upload_path):
    """ Create folder upload
    """

    try:
        os.makedirs(upload_path)
        return True, upload_path

    except OSError as e:
        if e.errno == errno.EEXIST:
            return True, upload_path
        else:
            return False, str(e)

    except Exception as e:
        return False, str(e)


def upload_file():
    """ API convert file
    - Get file via POST or GET
    - Download file to folder upload
    - Convert file
    - Return view converted file on the browser
    """

    date_today = datetime.date.today()
    upload_path = BaseConfig.UPLOAD_FOLDER + '/' + date_today.strftime(
        "%Y/%m/%d")  

    if request.method == 'POST':
        """ Handle file via POST
        - Get file upload via payload
        - Download file to folder upload
        """

        if 'file' not in request.files:
            return json.dumps({
                'status': '400',
                'message': u'Truyền file chưa đúng tham số '
            }), 400

        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ok, upload_path = _mkdir_upload_folder(upload_path)

            if not ok:
                return json.dumps({
                    'status': '500',
                    'message': u'Lỗi hệ thống'
                }), 500

            file_path = os.path.join(upload_path, filename)

            try:
                file.save(file_path)
            except Exception as e:
                return json.dumps({
                    'status':
                    '500',
                    'message':
                    u'Lỗi hệ thống, không thể upload file'
                }), 500
        else:
            return json.dumps({
                'status':
                '404',
                'message':
                "vui lòng tải lên file đúng định dạng ({})".format(
                    (', ').join(BaseConfig.ALLOWED_EXTENSIONS))
            }), 404  

    if request.method == 'GET':
        """ Handle file via GET
        - Get file from URL param
        - Download file to folder upload
        """

        if request.args.get('file') == '':
            return json.dumps({
                'status':
                '404',
                'message':
                'vui lòng truyền vào link file cần chuyển đổi'
            }), 404

        file_url = request.args.get('file')

        ok, upload_path = _mkdir_upload_folder(upload_path)

        if not ok:
            return json.dumps({
                'status': '500',
                'message': u'Lỗi hệ thống'
            }), 500

        if file_url.split('.')[-1] not in BaseConfig.ALLOWED_EXTENSIONS:
            content_disposition = requests.get(file_url).headers[
                'Content-Disposition']
            value, params = cgi.parse_header(content_disposition)
            name_file = params['filename']
            if re.search(r'\s', name_file):
                name_ext = name_file.split('.')[-1]
                name_edit = (name_file[:name_file.rindex('.')]).replace(
                    ' ', '-') + '.' + name_ext
                file_path = upload_path + '/' + name_edit
            else:
                file_path = upload_path + '/' + name_file

            try:
                r = requests.get(file_url, allow_redirects=True)
                open(file_path, 'wb').write(r.content)
            except Exception as e:
                return json.dumps({
                    'status':
                    '500',
                    'message':
                    u'Lỗi hệ thống, không thể download file'
                }), 500

        else:

            file_name_origin = file_url.rsplit('/', 1)[1]
            if file_name_origin.split('.')[
                    -1].lower() in BaseConfig.ALLOWED_EXTENSIONS:
                if re.search(r'\s', file_name_origin):
                    name_extension = file_name_origin.split('.')[-1]
                    file_name_edit = (
                        file_name_origin[:file_name_origin.rindex('.')]
                    ).replace(' ', '-') + '.' + name_extension
                    file_path = upload_path + '/' + file_name_edit
                else:
                    file_path = upload_path + '/' + file_name_origin

                    try:
                        r = requests.get(file_url, allow_redirects=True)
                        open(file_path, 'wb').write(r.content)
                    except Exception as e:
                        return json.dumps({
                            'status':
                            '500',
                            'message':
                            u'Lỗi hệ thống, không thể download file'
                        }), 500
            else:
                return json.dumps({
                    'status':
                    '404',
                    'message':
                    "vui lòng tải lên file đúng định dạng ({})".format(
                        (', ').join(BaseConfig.ALLOWED_EXTENSIONS))
                }), 404  

    ok, file_name = convert_file(file_path)
    
    file_path_convert = os.path.join(os.getcwd(), BaseConfig.CONVERT_FOLDER,
                                     file_name)
    with open(file_path_convert) as f:
        file_content = f.read()
    response = make_response(file_content)
    response.headers["Content-Disposition"] = "inline; filename={}".format(
        file_name)
    response.headers['Content-Type'] = 'application/pdf'
    return response


def download_file(filename):
    """Docs.

        Function download file
        ---
        tags:
          - Download
        parameters:
          - name: file
            type: string
            description: file to download
        responses:
          200:
            description: Download success
                        {'status': '200', 'message': '...'}
          401:
            description: Download falses
                        {'status': '401', message: '...'}
          404:
            description: File not found
        """

    return send_from_directory(
        directory=BaseConfig.CONVERT_FOLDER,
        filename=filename,
        as_attachment=True)
