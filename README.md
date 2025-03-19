# AWS Tools Project

A Python project for managing AWS services, including S3 storage operations and Celery tasks with SQS integration.

## Features

- S3 Storage Management
  - Upload JSON files
  - Download files
  - Delete objects
  - Rename folders
- Celery Task Queue with AWS SQS
  - Asynchronous task processing
  - AWS SQS as message broker
  - Task status monitoring

## Prerequisites

- Python 3.12
- AWS Account with configured credentials
- AWS SQS queue set up
- AWS S3 bucket with appropriate permissions

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd tools
```

2. Install dependencies:
```bash
pip install -e .
```

## Configuration

1. Create a `.env_test` file in the root directory with the following variables:
```env
AWS_ACCESS_KEY_SQS_ID=your_access_key
AWS_SECRET_ACCESS_SQS_KEY=your_secret_key
AWS_REGION=your_region
AWS_ACCOUNT_ID=your_account_id
AWS_SQS_QUEUE_NAME=your_queue_name
AWS_FOLDER=your_s3_folder
```

## Usage

### S3 Storage Operations

```python
from aws import S3Manager

# Initialize S3 Manager
s3_manager = S3Manager()

# Upload JSON file
s3_manager.upload_json_file("test.json", {"data": "value"}, "prefix/path")

# Download file
content = s3_manager.download_from_s3("test.json", "prefix/path")

# Delete object
s3_manager.delete_object_from_s3("test.json", "prefix/path")
```

### Celery Tasks

1. Start Celery worker:
```bash
celery -A async_tasks.celery worker --pool=solo --loglevel=info
```

2. Run a test task:
```python
from async_tasks.celery import test_task
test_task.delay()
```

## Development

### Running Tests

```bash
python -m unittest aws/tests/aws_storage_test.py
```

### Code Quality

The project uses several tools to maintain code quality:

- mypy for type checking
- black for code formatting
- flake8 for style guide enforcement
- isort for import sorting

Run linting checks:
```bash
make lint
```

⚠️ **Important Development Notes:**

1. **Linting Consistency**:
   - Ensure that linting configurations in pre-commit hooks and Makefile are consistent
   - This includes settings for black, flake8, mypy, and isort
   - Check both `.pre-commit-config.yaml` and `Makefile` when updating lint settings

2. **Package Management**:
   - All new packages MUST be listed in `pyproject.toml`
   - Update both `pyproject.toml` and requirements files when adding dependencies
   - Specify version constraints to ensure reproducible builds

## Project Structure

```
.
├── async_tasks/
│   └── celery.py          # Celery configuration and tasks
├── aws/
│   ├── __init__.py
│   ├── s3_manager.py      # S3 operations implementation
│   └── tests/
│       └── aws_storage_test.py
├── config/
│   ├── __init__.py
│   ├── settings.py        # Configuration settings
│   └── py_settings.py     # Python-specific settings
├── pyproject.toml         # Project metadata and dependencies
├── .env_test             # Environment variables (not in repo)
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Run all tests and linting checks
4. Submit a pull request

## License

[Your License Here]

## Contact

Analitika - contact@analitika.fr
