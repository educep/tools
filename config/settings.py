"""
Created by Analitika at 19/11/2024
contact@analitika.fr
"""

# External imports
import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file if it exists
load_dotenv()

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t", "yes", "y")
ISLOCAL_DB = os.getenv("ISLOCAL_DB", "True").lower() in ("true", "1", "t", "yes", "y")

# FOLDER IN S3
# CONTENT_LIBRARY_FOLDER = "content_library"

# WORDPRESS IDENTIFIERS AND PARAMETERS FOR TESTING
WP_URL = os.getenv("WP_URL", None)
WP_USERNAME = os.getenv("WP_USERNAME", None)
WP_ACCESSKEY = os.getenv("WP_ACCESSKEY", None)

# Environment variables for AWS credentials and configuration
# AWS_KMS_NAME = "MySecrets"  # Name you want for your secret
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", None)
AWS_ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID", None)
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", None)
AWS_CLI_ACCESS_KEY_ID = os.getenv("AWS_CLI_ACCESS_KEY_ID", None)
AWS_CLI_SECRET_ACCESS_KEY = os.getenv("AWS_CLI_SECRET_ACCESS_KEY", None)
AWS_ACCESS_KEY_SQS_ID = os.getenv("AWS_ACCESS_KEY_SQS_ID", None)
AWS_SECRET_ACCESS_SQS_KEY = os.getenv("AWS_SECRET_ACCESS_SQS_KEY", None)
AWS_SQS_QUEUE_NAME = os.getenv("AWS_SQS_QUEUE_NAME", None)
AWS_REGION = os.getenv("AWS_REGION", None)
AWS_FOLDER = os.getenv("AWS_FOLDER", None)
S3_BUCKET_NAME = os.getenv("AWS_BUCKET", None)

# SES
AWS_SES_USERNAME = os.getenv("AWS_SES_USERNAME", "")
AWS_SES_PASSWORD = os.getenv("AWS_SES_PASSWORD", "")
AWS_SMTP_HOST = os.getenv("AWS_SMTP_HOST", "")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 857))
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "")
LOGO_URL = os.getenv("LOGO_URL", "")
RECIPIENTS = os.getenv("RECIPIENTS", "")

# OPENAI IDENTIFIERS AND PARAMETERS
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
ORGANIZATION_ID = os.getenv("ORGANIZATION_ID", None)
COMPLETIONS_MODEL = os.getenv("COMPLETIONS_MODEL", None)
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", None)
# ANTHROPIC IDENTIFIERS AND PARAMETERS
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", None)
# DEEPSEEK IDENTIFIERS AND PARAMETERS
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", None)
# BEDROCK IDENTIFIERS AND PARAMETERS
AWS_BR_ACCESS_KEY_ID = os.getenv("AWS_BR_ACCESS_KEY_ID", None)
AWS_BR_SECRET_ACCESS_KEY = os.getenv("AWS_BR_SECRET_ACCESS_KEY", None)

provider_configs = {}

if OPENAI_API_KEY:
    provider_configs["openai"] = {"api_key": OPENAI_API_KEY}
if ANTHROPIC_API_KEY:
    provider_configs["anthropic"] = {"api_key": ANTHROPIC_API_KEY}
if DEEPSEEK_API_KEY:
    provider_configs["deepseek"] = {
        "api_key": DEEPSEEK_API_KEY,
        "base_url": "https://api.deepseek.com",
    }
if AWS_BR_ACCESS_KEY_ID:
    provider_configs["aws"] = {
        "aws_access_key": AWS_BR_ACCESS_KEY_ID,
        "aws_secret_key": AWS_BR_SECRET_ACCESS_KEY,
        "aws_region": "us-east-1",
    }


COMPLETION_MODELS_LIST = [
    "deepseek:deepseek-chat",
    "openai:gpt-4o-mini",
    "openai:gpt-4o",
    "anthropic:claude-3-5-sonnet-latest",
    "anthropic:claude-3-5-haiku-latest",
    "anthropic:claude-3-opus-latest",
    "aws:amazon.nova-micro-v1:0",
    "aws:amazon.nova-lite-v1:0",
    "aws:amazon.nova-pro-v1:0",
]

IMAGE_MODELS_LIST = [
    "openai:dall-e-3",
    "aws:amazon.nova-canvas-v1:0",
]

# Time format for filenames
TIME_FORMAT = "%Y-%m-%d_%Hpp%M"

# DATABASES
notion_database_id = os.getenv("DB_NOTION", None)
notion_database_key = os.getenv("KEY_NOTION", None)

main_database_name = os.getenv("DATABASE_NAME", None)
main_database_user = os.getenv("DATABASE_USER", None)
main_database_password = os.getenv("DATABASE_PASSWORD", None)
main_database_host = os.getenv("DATABASE_HOST", None)
main_database_port = os.getenv("DATABASE_PORT", None)
main_database_ssl = os.getenv("DATABASE_SSL", None)


# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJ_ROOT / "data"
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

if __name__ == "__main__":
    logger.info("Done")
