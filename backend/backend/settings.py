import os
import io
import environ
import google.auth
from google.cloud import secretmanager

# Import the original settings from each template
from .basesettings import *

# Load the settings from the environment variable
env = environ.Env()
env_file = os.path.join(BASE_DIR, ".env")
# env.read_env(io.StringIO(os.environ.get("APPLICATION_SETTINGS", None)))

# Attempt to load the Project ID into the environment, safely failing on error.
try:
    _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
except google.auth.exceptions.DefaultCredentialsError:
    pass

if os.path.isfile(env_file):
    # Use a local secret file, if provided

    env.read_env(env_file)
# ...
elif os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    # Pull secrets from Secret Manager
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

    env.read_env(io.StringIO(payload))
else:
    raise Exception("No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.")
# Setting this value from django-environ
SECRET_KEY = env("SECRET_KEY")

# If defined, add service URL to Django security settings
CLOUDRUN_SERVICE_URL = env("CLOUDRUN_SERVICE_URL", default=None)
if CLOUDRUN_SERVICE_URL:
    ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc]
    CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]
else:
    ALLOWED_HOSTS = ["*"]

# Default false. True allows default landing pages to be visible
DEBUG = env("DEBUG", default=False)

# Set this value from django-environ
# DATABASES = {"default": env("DATABASE_URL")}

DATABASES = {
    'default': {
        'DATABASE_URL': env("DATABASE_URL"),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eews_db',
        'USER': 'eews',
        'PASSWORD' : 'admin123',
        'HOST' : '127.0.0.1',
        'PORT' : '8001'
    }
}

# Change database settings if using the Cloud SQL Auth Proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 8001

if "api" not in INSTALLED_APPS:
     INSTALLED_APPS += ["api"] # for custom data migration

# Define static storage via django-storages[google]
GS_BUCKET_NAME = env("GS_BUCKET_NAME")
STATICFILES_DIRS = []
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_DEFAULT_ACL = "publicRead"