# Zoomsamples

> Samples for the Zoom developer platform.

This repository provides a collection of Python scripts to interact with the Zoom API, covering OAuth flows, Server-to-Server OAuth, meeting data retrieval, and webhook validation. It also includes a CLI for easy testing.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [API](#api)
- [Contributing](#contributing)

## Background

This project serves as a reference for developers looking to integrate Zoom's API into their Python applications. It demonstrates various authentication methods (OAuth 2.0, Server-to-Server OAuth) and common API tasks like fetching meeting data and validating webhooks.

## Install

### Prerequisites

- [1Password CLI](https://developer.1password.com/docs/cli/) (optional, if using secret references)
- [Python 3](https://www.python.org/downloads/)
- [Zoom Account](https://marketplace.zoom.us/) and a [Server-to-server OAuth app](https://developers.zoom.us/docs/internal-apps/)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/YRG999/zoomsamples.git
   cd zoomsamples
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Copy `.env.example` to `.env` and fill in your keys. You can use 1Password secret references (e.g., `op://vault/item/field`) if the 1Password CLI is installed.

## Usage

### Zoom CLI

The easiest way to explore the API samples is through the interactive CLI:

```bash
python zoom_cli.py
```

Options include:
1. **Authorize**: Opens the OAuth URL, exchanges the code for tokens, and persists them to `.env`.
2. **Get user info**: Retrieves and displays information for the currently authorized user.
3. **Refresh tokens**: Manually refreshes the stored access token.
4. **Custom request**: Executes a custom HTTP request against the Zoom API.

### Individual Scripts

Scripts can also be run individually for specific tasks:

- **Server-to-Server OAuth**: `python S2Saccesstoken.py` or `python S2Srequest.py`
- **Meeting Data**: `python zoom_dash.py`
- **Webhook Validation**: `python validatewebhook/app.py`

## API

| Script | Purpose |
| --- | --- |
| `access_request.py` | OAuth 2.0 helper for token exchange and refresh. |
| `request_handler.py` | Shared utilities for Zoom API requests with automatic token handling. |
| `credentials.py` | Standalone utility to resolve secrets from `.env` or 1Password. |
| `getaccountsettings.py` | Fetches account-level settings. |
| `zoom_dash.py` | Lists meetings and participants for the current user. |
| `S2Saccesstoken.py` | Obtains S2S OAuth access tokens. |
| `S2Srequest.py` | Example GET request using S2S OAuth. |
| `validatewebhook/app.py` | Flask application to validate Zoom webhook CRC requests. |
| `prettifydict.py` | Helper to pretty-print dictionary strings as JSON. |

## Contributing

PRs accepted.

Small note: If editing the README, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.
