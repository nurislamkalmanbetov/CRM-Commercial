import os

from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class PathMixin:
    """Mixin for preventing NotImplementedError"""
    def path(self, name):
        pass


class StaticStorage(S3Boto3Storage, PathMixin):
    location = 'static'
    default_acl = 'public-read'
    querystring_auth = False
    file_overwrite = True


class PublicMediaStorage(S3Boto3Storage, PathMixin):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage, PathMixin):
    location = 'media'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False
