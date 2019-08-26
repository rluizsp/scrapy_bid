from scrapy.pipelines.files import GCSFilesStore, FilesPipeline


class GCSFilesStoreJSON(GCSFilesStore):
    CREDENTIALS = {
  "type": "service_account",
  "project_id": "scrapy-bid",
  "private_key_id": "d0422d44f96d313c9dcc9d1bb02d482c42a242a3",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDN7qUS1LuIsWVe\ndB83TFuCGSAKOhI6JjGFQgKfc00r8V4c9dsSyLmVUwx37qYNxWucUBUjeiU8HMz7\nw3z2W2/pTaDT586BCPDwjnkAQeSuEd4D7HqjfIfY5PK76LTiomSKknH8TNK0NtX7\n+zkyoE54GVLq1nbYBz6sOuDUXxG+lKo7/f+NzAf9dVv0OVFujRtGVUBcx5iEldWm\neTPNM9Gyo9/bPUlMB48CRuD4W/C01lkgzNjGfM854HgEtIiMI2unCzhfe/850U+Q\nyghDpZ+mEBDy1Z2/g713co5HRPYjokZKESZWCrU7nViwrK0f10x+LcKnMr3zN1AR\nCIZhBua5AgMBAAECggEAAuwaB5RhPOVXjOmU79HzknsMy1hbndug5EU1iFG4jKEW\nNs7+VtvmVkohaSpHzPY6OrOgOSqokJvQBNqXUV+mzOa/G4K0mXwo/yDmcqx8tEOo\npOGcM+m2e8tz7lq1BmpLhvPhDjWA3/HPQ44jF6bStj2VwaNdeF9R8lu7iQf4Vn37\nC0kCjtoSQIz1usGXBWBJubNpcqiHU1b9z+TjNksTkVQhiRscJlTKrxqyqYF0zldo\nP0foCNLpmxTOLoeqdtggciC+o4TLDPEkxMyn4nReT4uCdpo4Gl1Kec2I0v83epIc\nJPMIGLndEU1JFe+Vbcun54hITkhNmaZ7+9lxGkknAQKBgQD39ktcskrJQJUh9Ogx\nB7wW0885qPb49Ht7AdXcq/mLxQRUw8PG4uqqZHhi7c5U+wk9um9gmhc5tmMtcRTR\np/ttZHde40z8QB8DZxb5HHwTZmN5mHt+1td4qSdyTBKMV2aDdK6q/nWTR50/zFP0\nu8GlFdEG2oaEfFejFbtE9kUxSQKBgQDUm5EYteUjlxsOlUAfCN1gY+WA5wV6to2m\nX6DVbaxF0RQE+HeDHW4X2FVwOMQGlfUiXhCVJqF5cBt/nHl0IsE884XgBN+T1vWK\n8JoYwcsx/AHsGtozqy324QJEBjJIRgP1vfA7i+UEdC2vZzC0tUP7UBZPMCcG0+Qu\nRCGAQNh58QKBgQD19PF2BkhWbmA/aX2zvLdecUUZLbek5GVjc0Oee1uxv4B3UCPv\nMQCSecxMXRSQiN32w+pciRxGm9qupX+AIz8rmD8r+Q1RHY1lw6ku+ok8eRBs+cpt\n20+qGSfOoRS47qz58hCb/oHD0IJzWQtiM6d2SDipsrNB0VDgrNqwIhQqOQKBgQCU\nbg98ivDwSfxP0A82G4BCXTvLJH6Ez5JRBw5IMwtEqtUpKzZ0yUUlTJlJgbgJSQQc\n/ELjflbZa1UnYFzCocj6/qEGZyCYHEjMuXE7u4Ba4y+MYKrZy7aJV0m3qAPOxWLa\nW8KuL9qxo1KJ1KcCYlKVz7HjkyCL+b6iNlqVKbB4YQKBgFwp2I9BWIoexGXp2DY7\nNptaQPeIQg+AZtvRWwlhTf+YQYbuEtfkjALHah1ZGsv/ukvjlivH4fLTJ4Bp5Opq\n/8fhfI0iabeuZDxp3V+b1yflf2qcbfrW+HUszHfBuTE+bGjTKvHQXE2oyPrqzqt0\nfAaHcL+jAMwdV3fVCfZgwNCX\n-----END PRIVATE KEY-----\n",
  "client_email": "429338049156-compute@developer.gserviceaccount.com",
  "client_id": "117560538359305668376",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/429338049156-compute%40developer.gserviceaccount.com"
}


def __init__(self, uri):
  from google.cloud import storage
  client = storage.Client.from_service_account_info(self.CREDENTIALS)
  bucket, prefix = uri[5:].split('/', 1)
  self.bucket = client.bucket(bucket)
  self.prefix = prefix


class GCSFilePipeline(FilesPipeline):

    def __init__(self, store_uri, download_func=None, settings=None):
        super(GCSFilePipeline, self).__init__(store_uri, download_func, settings)