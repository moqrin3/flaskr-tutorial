from __future__ import absolute_import
from app import ALLOWED_EXTENSIONS, BUCKET_NAME
from werkzeug.exceptions import BadRequest
from werkzeug import secure_filename
import six
import datetime
import boto3
import os
UPLOADS_FOLDER = "uploads"


def _check_extension(filename, allowed_extensions):
    if ('.' not in filename or
            filename.split('.').pop().lower() not in allowed_extensions):
        raise BadRequest(
            "{0} has an invalid name or extension".format(filename))


def _safe_filename(filename):

    filename = secure_filename(filename)
    return filename


def upload_file(file_stream, filename, content_type):

    _check_extension(filename, ALLOWED_EXTENSIONS)
    filename = _safe_filename(filename)

    object_name = filename
    s3 = boto3.client('s3')
    s3.upload_file(f"uploads/{filename}", BUCKET_NAME, object_name)

    bucket_location = s3.get_bucket_location(Bucket=BUCKET_NAME)
    url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
        bucket_location['LocationConstraint'],
        BUCKET_NAME,
        filename)

    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    print(url)

    return url
