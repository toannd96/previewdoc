"""Main app."""
# coding: utf-8
from flask import Flask
from resources.upload import upload_file, download_file
import os
from config import config


def create_app():
    """Docs.

    Function create app
    ---
    tags:
      - Main app
      - Config env app
      - Config url
    """
    app = Flask(__name__)

    # Get env
    env = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[env])
    app.add_url_rule(
        '/uploads', 'uploads', upload_file, methods=['POST', 'GET'])

    app.add_url_rule(
        '/download/<string:filename>',
        'download',
        download_file,
        methods=['GET'])
    return app


serve = create_app()

if __name__ == '__main__':
    serve.run()
