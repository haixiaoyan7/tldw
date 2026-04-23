# TLDW — Too Long; Didn't Watch

A backend service that takes a SharePoint/OneDrive video sharing link, downloads the video via Microsoft Graph API, transcribes it, and generates a summary — so you don't have to watch the whole thing.

## Architecture

```
Client (any frontend)
  │
  │  POST /api/analyze  { "url": "<share link>" }
  │
  ▼
FastAPI Backend (SSE streaming)
  ├── getVedio.py   — Microsoft Graph auth & file resolution
  ├── transcript.py — Video transcription & analysis (WIP)
  └── main.py       — API entry point, streams progress via SSE
```

### Pipeline

1. **Resolve** — Converts a SharePoint/OneDrive sharing URL into a direct download URL using the Microsoft Graph `/shares` API.
2. **Transcribe** — Sends the file to an external transcription service and saves the `.srt` result locally.
3. **Analyze / Summarize** — Sends the transcription to an analysis service to produce a summary.

Progress for each stage is streamed back to the client as **Server-Sent Events (SSE)**.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Web Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| Auth | [MSAL](https://github.com/AzureAD/microsoft-authentication-library-for-python) (device code flow) |
| HTTP Client | `requests` |
| API | Microsoft Graph v1.0 |

## Getting Started

### Prerequisites

- Python 3.8+
- An Azure AD app registration with **Files.Read** permission

### Installation

```bash
cd tldw/backend
pip install -r requirements.txt
```

### Configuration

Edit the placeholder values in `app/getVedio.py`:

```python
TENANT_ID     = "YOUR_TENANT_ID"
CLIENT_ID     = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
SITE_NAME     = "YOUR_SITE_NAME"
```

### Run

```bash
cd tldw/backend
uvicorn app.main:app --reload
```

The server starts at `http://127.0.0.1:8000`.

## API

### `POST /api/analyze`

Accepts a SharePoint/OneDrive sharing URL and streams processing status.

**Request**

```json
{
  "url": "https://xxxxx-my.sharepoint.com/:v:/g/personal/..."
}
```

**Response** (`text/event-stream`)

```
data: get video...

data: analyze video...

data: generate summary...

data: Done
```

On failure:

```
data: ERROR: can't get file
```

## Project Structure

```
tldw/
└── backend/
    ├── requirements.txt
    └── app/
        ├── main.py          # FastAPI app & SSE endpoint
        ├── getVedio.py       # Graph API auth, token cache, file download
        └── transcript.py     # Transcription & analysis helpers (WIP)
```

## Status

This project is a **work in progress**. The Graph file-resolution flow is functional; transcription and summarization stages are stubbed out and pending integration with external services.

## License

Internal use.
