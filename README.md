# zoomsamples
Samples using the Zoom developer platform.

* `S2Saccesstoken.py` - get an access token for your server-to-server app.
* `S2Srequest.py` - make a request using your access token.
* `zoom_dash.py` - list participant names from all meetings for the specified user in the account.
* **validatewebhook** - deploy this code to Heroku to set up webhooks and receive responses in a log. See the readme for instructions & how to save webhook responses to a database.
* `prettifydict.py` - enter a Python dictionary from a log file to see it in human-readable JSON.

## Setup

Create a virtual environment.

```bash
$ python -m venv venv
$ . venv/bin/activate
```

Install requirements.

```
pip install -r requirements.txt
```

[Create a Zoom account](https://marketplace.zoom.us/) and a [Server-to-server OAuth app](https://developers.zoom.us/docs/internal-apps/).

Copy `.env.example` and rename to `.env` and enter your keys.
