"""OOP interface for S3.
"""

import io
import os

import boto3
from tinyimage import TinyImage


class S3Manager(object):
  """Class for managing s3 tasks.
  """

  def __init__(self, access_key, secret_key, region="us-east-1"):
    """Create s3 client.
    """
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region)
    self.client = session.client("s3")

  def create_bucket(self, bucket_name):
    """Create new bucket.
    """
    bucket = self.client.create_bucket(Bucket=bucket_name)
    assert "Location" in bucket, "Bucket creation failed"

  def get_object(self, bucket_name, obj_key):
    """Get object binary data from bucket.

    Args:
      obj_key: object key.
    Returns:
      object data.
    """
    res = self.client.get_object(Bucket=bucket_name, Key=obj_key)
    obj_data = res["Body"].read()
    return obj_data

  def upload_file(self, filepath, bucket_name, file_key):
    """Upload a file to bucket.

    Returns:
      file url.
    """
    self.client.upload_file(filepath, bucket_name, file_key)

  def upload_img_file(self, filepath, bucket_name, file_key):
    """Upload image file.
    """
    _, img_ext = os.path.splitext(os.path.split(filepath)[1])
    upload_args = {}
    if img_ext in [".jpg", ".jpeg"]:
      upload_args["ContentType"] = "image/jpeg"
    elif img_ext == ".png":
      upload_args["ContentType"] = "image/png"
    else:
      raise Exception("invalid image type")
    self.client.upload_file(
        filepath, bucket_name, file_key, ExtraArgs=upload_args)
    return self.generate_presigned_url(bucket_name, file_key, 3600)

  def upload_img_bin(self,
                     bucket_name,
                     img_bin,
                     img_format="png",
                     key_prefix="",
                     make_public=False):
    """Upload image binary data to bucket.

    Key is named: prefix/img_sha.format.

    Args:
      img_bin: image binary data.
      img_format: type of image, only support jpy or png.
      key_prefix: prefix of image key, used to create folders.
      make_public: whether to make it publically accessible.
    Returns:
      image object key.
    """
    img_format = img_format.lower()
    assert img_format in ["png", "jpg",
                          "jpeg"], "img_format must be either png, jpg, jpeg."
    # make sure no duplicate images are saved.
    img_obj = TinyImage(img_bin=img_bin)
    key_prefix = key_prefix.strip("/")
    img_key_name = "{}/{}.{}".format(key_prefix,
                                     img_obj.get_base64_sha_encoding(),
                                     img_format)
    img_key_name = img_key_name.strip("/")
    upload_args = {}
    if img_format in ["jpg", "jpeg"]:
      upload_args["ContentType"] = "image/jpeg"
    if img_format == "png":
      upload_args["ContentType"] = "image/png"
    if make_public:
      upload_args["ACL"] = "public-read"
    self.client.upload_fileobj(
        io.BytesIO(img_bin), bucket_name, img_key_name, ExtraArgs=upload_args)
    if make_public:
      return img_key_name
    else:
      self.generate_presigned_url()

  def upload_img_base64(self,
                        bucket_name,
                        img_base64,
                        img_format="jpg",
                        key_prefix="",
                        make_public=False):
    """Save image data to bucket.

    sha1 is used as key for image data.

    Args:
      img_base64: base64 string of image.
    Returns:
      image sha hash as key.
    """
    img_obj = TinyImage(img_base64=img_base64)
    img_url = self.upload_img_bin(bucket_name, img_obj.to_binary(), img_format,
                                  key_prefix, make_public)
    return img_url

  def generate_obj_public_url(self, bucket_name, obj_key):
    """Generate url of object.

    Args:
      obj_key: key to object in the bucket.

    Returns:
      the url for object.
    """
    img_url = "{}/{}/{}".format(self.client.meta.endpoint_url, bucket_name,
                                obj_key)
    return img_url

  def generate_presigned_url(self, bucket_name, obj_key, expire_secs=604800):
    """Generate a temporary url.

    Args:
      obj_key: key of object in the current bucket.

    Returns:
      presigned url for the target object.
    """
    url = self.client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": bucket_name,
            "Key": obj_key
        },
        ExpiresIn=expire_secs)
    return url
