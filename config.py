"""Google Cloud Storage Configuration."""
from os import environ


# Google Cloud Storage
bucketName = environ.get('scrapy-bid')
bucketFolder = environ.get('bid')

# Data
localFolder = environ.get('data')