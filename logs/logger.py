# logging/logger.py

import os
import json
import sys
from datetime import datetime
from google.cloud import storage

# Only import and initialize GCS client if not in local development
if os.getenv('FLASK_ENV') != 'development':
    storage_client = storage.Client()
    GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME', 'flashcard-logs-429516')
    GCS_LOG_FILE = 'flashcard/logging/app_logs.json'

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
    
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(GCS_LOG_FILE)

    # Download existing content
    existing_content = ''
    if blob.exists():
        existing_content = blob.download_as_text()

    # Append new log entry
    updated_content = existing_content + json.dumps(log_entry) + '\n'

    # Upload updated content
    blob.upload_from_string(updated_content)

def log(severity, message, **kwargs):
    log_stderr(severity, message, **kwargs)
    log_gcs(severity, message, **kwargs)