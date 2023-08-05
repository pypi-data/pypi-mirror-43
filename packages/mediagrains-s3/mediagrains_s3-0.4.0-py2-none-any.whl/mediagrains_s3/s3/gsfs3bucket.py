#!/usr/bin/python
#
# Copyright 2018 British Broadcasting Corporation
#
# This is an internal BBC tool and is not licensed externally
# If you have received a copy of this erroneously then you do
# not have permission to reproduce it.

"""\
Simple library for reading and writing grains to/from S3 buckets
"""

from __future__ import print_function
from __future__ import absolute_import

import boto3
import botocore.exceptions
from io import BytesIO
from mediagrains.gsf import load

from ..bucket import GSFBucket
from .encoder import GSFS3Encoder
from ..progresstrackers import GSFDownloaderProgressTracker, GSFUploaderProgressTracker

__all__ = ["GSFS3Bucket"]


class GSFS3Bucket(GSFBucket):
    """A class representing an S3 bucket. The constructor takes a bucket_name.

    Optionally a boto3.client object and/or a boto3.s3.transfer.TransferConfig object can be provided to customise
    the class's behaviour.

    Optionally access to the S3 bucket can be validated. Note that a botocore.exceptions.ClientError with a reponse
    code of 403 (`exception.response["Error"]["Code"] == 403`) may be raised if the bucket exists in another account
    and therefore cannot be accessed/created; because AWS S3 bucket names are global across a region.

    :param bucket_name: Name of S3 bucket to use
    :param client: Optional boto3.client object; if one is not supplied it will be created
    :param config: Optional boto3.s3.transfer.TransferConfig; if not supplied defaults will be used instead
    :param region: AWS region in which to access bucket. If not supplied will be extracted from endpoint URL or
                   local boto3 defaults.
    :param endpoint_url: Endpoint at which to access S3 (or equivalent implementation)
    :param check_bucket_accessible: Check that the bucket exists and its metadata can be accessed. Defaults to False.
                                    Always True if create_bucket=True
    :param create_bucket: If the bucket doesn't exist, attempt to create it. Implies check_bucket_accessible=True

    :raises botocore.exceptions.ClientError: If bucket access validation failes
    """
    def __init__(self, bucket_name, client=None, config=None, region=None, profile_name=None, endpoint_url=None,
                 check_bucket_accessible=False, create_bucket=False):
        super(GSFS3Bucket, self).__init__()
        self.bucket_name = bucket_name
        self.client = client
        self.config = config
        if self.client is None:
            session_kwargs = {}
            if profile_name is not None:
                session_kwargs['profile_name'] = profile_name
            session = boto3.Session(**session_kwargs)
            client_kwargs = {}
            if region is not None:
                client_kwargs['region_name'] = region
            if endpoint_url is not None:
                client_kwargs['endpoint_url'] = endpoint_url
            self.client = session.client('s3', **client_kwargs)

        if check_bucket_accessible or create_bucket:
            try:
                # Try and list the bucket; if an exception is raised let it bubble up to the caller
                self.client.head_bucket(Bucket=bucket_name)
            except botocore.exceptions.ClientError as e:
                if create_bucket and e.response["Error"]["Code"] == "404":
                    try:
                        self.client.create_bucket(
                            Bucket=bucket_name,
                            CreateBucketConfiguration={"LocationConstraint": self.client.meta.region_name}
                        )
                    except self.client.exceptions.BucketAlreadyOwnedByYou:
                        pass  # Somebody else created the bucket between the head_bucket call and here - carry on
                else:
                    raise e

    def get_encoder(self, key, cls=None, **kwargs):
        """Returns a GSFS3Encoder object which writes to a given S3 object.
        :param key: an S3 object key
        :param cls: the class to use for encoding, GSFS3Encoder is the default, others must inherit from it

        other keyword arguments will be fed to the class constructor.
        The object returned by this method will upload to the bucket when dump
        or end_dump is called."""
        if cls is None:
            cls = GSFS3Encoder
        if not issubclass(cls, GSFS3Encoder):
            raise TypeError("{!r} is not a subclass of GSFS3Encoder".format(cls))
        progress_tracker = GSFUploaderProgressTracker(self.bucket_name, key)
        self.progress_trackers.append(progress_tracker)
        return cls(self.bucket_name, key, boto3_client=self.client, boto3_upload_callback=progress_tracker,
                   boto3_config=self.config, **kwargs)

    def upload(self, key, grains, cls=None, segment_tags=None, **kwargs):
        """Serialise a series of grains into an S3 object.
        :param key: an S3 object key
        :param grains: an iterable of grain objects
        :param segment_tags: a list of pairs of strings to use as tags for the segment created
        :param cls: the class to use for encoding, GSFS3Encoder is the default, others must inherit from it

        other keyword arguments will be fed to the class constructor.
        This method will serialise the grains in a single segment."""

        enc = self.get_encoder(key, cls=cls, **kwargs)
        seg = enc.add_segment(tags=segment_tags)
        seg.add_grains(grains)
        # Nb. this will call start_dump and end_dump, so it actually starts the upload
        enc.dump()

    def download(self, key, cls=None, parse_grain=None, download_extra_args=None, **kwargs):
        """Deserialise grains from an amazon S3 bucket into python, returns a
        pair of (head, segments) where head is a python dict containing general
        metadata from the file, and segments is a dictionary mapping numeric
        segment ids to lists of Grain objects.

        :param key: The S3 object key
        :param cls: The class to use in decoding, the default is mediagrains.gsf.GSFDecoder
        :param parse_grain: A function that takes a (meta, data) tuple and returns a grain object
        the default is mediagrains.Grain
        :param download_extra_args: Extra arguments to pass to boto3.client.download_fileobj as ExtraArgs

        Extra kwargs will be passed to the decoder constructor."""
        b = BytesIO()
        progress_tracker = GSFDownloaderProgressTracker(self.bucket_name, key)
        self.progress_trackers.append(progress_tracker)
        progress_tracker.max_size = self.client.head_object(Bucket=self.bucket_name, Key=key)["ContentLength"]
        self.client.download_fileobj(self.bucket_name, key, b,
                                     ExtraArgs=download_extra_args,
                                     Callback=progress_tracker,
                                     Config=self.config)
        progress_tracker.max_size = len(b.getvalue())
        b.seek(0)
        (head, grains) = load(b, cls=cls, parse_grain=parse_grain, **kwargs)
        return (head, grains)
