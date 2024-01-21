import boto3
import configparser


class store:
    def __init__(self, key):
        config = configparser.ConfigParser()
        config.read("aws.ini")
        AWS_ACCESS_KEY_ID = config["credential"]["AWS_ACCESS_KEY_ID"]
        AWS_SECRET_ACCESS_KEY = config["credential"]["AWS_SECRET_ACCESS_KEY"]
        sess = sess = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self._s3_client = sess.client("s3")
        self._bucket = config["s3"]["BUCKET"]
        self._key = key

    def get(self):
        r = self._s3_client.get_object(Bucket=self._bucket, Key=self._key)
        body = r["Body"].read()
        return body.decode("utf-8")

    def put(self, s):
        self._s3_client.put_object(
            Bucket=self._bucket, Key=self._key, Body=str(s).encode("utf-8")
        )
