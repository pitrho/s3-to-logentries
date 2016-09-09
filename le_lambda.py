import boto3
import socket
import ssl
import datetime
import re
import urllib
import csv
import zlib
import json
from le_config import *

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    host = 'data.logentries.com'
    port = 20000
    s_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = ssl.wrap_socket(
        s_,
        ca_certs='le_certs.pem',
        cert_reqs=ssl.CERT_REQUIRED
    )

    s.connect((host, port))

    if validate_uuid(log_token) is False:
        print("{0} - Log token not valid ...".format(str(log_token)))
        raise SystemExit

    else:
        # Get the object from the event and show its content type
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'])\
            .decode('utf8')

        try:
            response = s3.get_object(Bucket=bucket, Key=key)

            size = response['ContentLength']
            size_units = "KB"
            if size_as_mb:
                size = float(size) / float(1000000)
                size_units = "MB"

            msg = "{} LOG_TYPE: {}, OBJECT_KEY: {}, BUCKET_NAME: {}, "\
                  "FILE_SIZE: {}, FILE_SIZE_UNIT: {}\n"\
                  .format(
                    log_token, log_type_name, key, bucket, size, size_units
                  )

            s.sendall(msg)

            if send_body:
                body = response['Body']
                data = body.read()
                # If the name has a .gz extension, then decompress the data
                if key[-3:] == '.gz':
                    data = zlib.decompress(data, 16+zlib.MAX_WBITS)
                lines = data.split("\n")
                for line in lines:
                    msg = "{} {}\n".format(log_token, line)
                    s.sendall(msg)

        except Exception as e:
            print e
            msg = "{} Error getting file='{}' from bucket='{}'. "\
                  "Make sure they exist and your bucket is in the same "\
                  "region as this function.\n"\
                  .format(log_token, key, bucket)
            s.sendall(msg)

        finally:
            s.close()

def validate_uuid(uuid_string):
    regex = re.compile('^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$', re.I)
    match = regex.match(uuid_string)
    return bool(match)
