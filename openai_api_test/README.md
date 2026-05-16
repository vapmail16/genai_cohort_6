# OpenAI API Connection Test

Simple script to verify OpenAI API connectivity using the API key from the monorepo `.env`.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python test_openai.py
```

Loads `OPENAI_API_KEY` from (first match):

- `capstone_project/backend/.env` (if present)
- project root `.env`
- `openai_api_test/.env` (copy `.env.example` if needed)

## Expected Output

```
Loaded .env from: .../capstone_project/backend/.env
Testing OpenAI API connection...
Response: OK
SUCCESS: OpenAI API connection works.
```
