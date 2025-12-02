# Zoom samples

Samples for the Zoom developer platform.

## Setup

1. Create a virtual environment.

    ```zsh
    python3 -m venv venv
    . venv/bin/activate
    ```

2. Install requirements.

    ```zsh
    pip install -r requirements.txt
    ```

3. [Create a Zoom account](https://marketplace.zoom.us/) and a [Server-to-server OAuth app](https://developers.zoom.us/docs/internal-apps/).

4. Copy `.env.example` and rename to `.env`, then fill in your keys.

## File guide

| File | Description | Run |
| --- | --- | --- |
| `access_request.py` | OAuth helper that exchanges and refreshes tokens. | `python access_request.py` |
| `request_handler.py` | Shared request utilities that reuse stored tokens. | Imported |
| `zoom_cli.py` | Interactive CLI for authorization and API calls. | `python zoom_cli.py` |
| `getaccountsettings.py` | Fetches account settings with automatic token refresh. | `python getaccountsettings.py` |
| `zoom_dash.py` | Lists meetings and participants for the current user. | `python zoom_dash.py` |
| `S2Saccesstoken.py` | Obtains an access token for Server-to-Server OAuth. | `python S2Saccesstoken.py` |
| `S2Srequest.py` | Sample GET request using a Server-to-Server token. | `python S2Srequest.py` |
| `validatewebhook/app.py` | Flask webhook validator for Zoom URL verification. | `python validatewebhook/app.py` |
| `prettifydict.py` | Converts dict strings into pretty-printed JSON. | `python prettifydict.py` |

## Quick start: Zoom CLI

1. Ensure dependencies are installed and `.env` includes `CLIENT_ID`, `CLIENT_SECRET`, and `REDIRECT_URI`.
2. Launch the CLI menu:

    ```zsh
    python zoom_cli.py
    ```

3. Pick an action:
    - `1` Authorize (open the URL, supply the code; tokens persist to `.env`).
    - `2` Retrieve current user info.
    - `3` Refresh stored tokens.
    - `4` Run a custom request (enter method, endpoint, optional JSON query params).
