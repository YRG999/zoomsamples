# zoomsamples
Samples using the Zoom developer platform.

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

Create a Zoom account and a Server-to-server OAuth app.

Copy `.env.example` and rename to `.env` and enter your keys.

## Samples

* `S2Saccesstoken.py` - Run to get your access token, then add it to your `.env` file to make calls.
* `S2Srequest.py` - Try out your first request.
* `zoom_dash.py` - Get a list of participants from each of your meetings.
