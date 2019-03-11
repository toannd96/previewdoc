import os
import yaml
import sys

with open("app.yaml", "r") as stream:
    try:
        config = yaml.load(stream)
    except Exception as e:
        sys.exit(str(e))


def _get_config_value(key, default_value):
    return os.environ.get(key, config.get(key, default_value))


class BaseConfig(object):
    UPLOAD_FOLDER = _get_config_value("UPLOAD_FOLDER", "upload")
    CONVERT_FOLDER = _get_config_value("CONVERT_FOLDER", "convert")
    MAX_CONTENT_LENGTH = _get_config_value("MAX_CONTENT_LENGTH", 52428800)
    ALLOWED_EXTENSIONS = _get_config_value(
        "ALLOWED_EXTENSIONS", ["txt", "docx", "doc", "xls", "xlsx", "pptx"]
    )


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class StagingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    DEBUG = False


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "staging": StagingConfig,
}
