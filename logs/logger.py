# logging/logger.py

import os
import json
import sys
from datetime import datetime
from google.cloud import storage

# Only import and initialize GCS client if not in local development
if os.getenv('FLASK_ENV') != 'development':
    storage_client = storage.Client()
    GCS_BUCKET_NAME = 'your-gcs-bucket-name'

def log_stderr(severity, message, **kwargs):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "severity": severity,
        "message": message,
        **kwargs
    }
    print(json.dumps(log_entry), file=sys.stderr)

def log_gcs(severity, message, **kwargs):
    if os.getenv('FLASK_ENV') == 'development':
        return  # Skip GCS logging in development

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "severity": severity,
        "message": message,
        **kwargs
    }
    
    filename = f"logs/{datetime.utcnow().strftime('%Y/%m/%d/%H/%M%S_%f')}.json"
    
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_string(json.dumps(log_entry))

def log(severity, message, **kwargs):
    log_stderr(severity, message, **kwargs)
    log_gcs(severity, message, **kwargs)