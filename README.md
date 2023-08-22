# zoomsamples
Samples for the Zoom developer platform.

* `prettifydict.py` - enter a Python dictionary from a log file to see it in human-readable JSON.
* `S2Saccesstoken.py` - get an access token for your [server-to-server app](https://developers.zoom.us/docs/internal-apps/).
* `S2Srequest.py` - make a request using your [server-to-server access token](https://developers.zoom.us/docs/internal-apps/s2s-oauth/).
* `validatewebhook` - Python [Zoom webhook validator](https://developers.zoom.us/docs/api/rest/webhook-reference/) and event logger that you can deploy to [Heroku](https://www.heroku.com/).
* `zoom_dash.py` - list participant names from all meetings for the specified user in the account (requires an access token).

## Setup

1. Create a virtual environment.

    ```bash
    $ python -m venv venv
    $ . venv/bin/activate
    ```

2. Install requirements.

    ```
    pip install -r requirements.txt
    ```

3. [Create a Zoom account](https://marketplace.zoom.us/) and a [Server-to-server OAuth app](https://developers.zoom.us/docs/internal-apps/).

4. Copy `.env.example` and rename to `.env` and enter your keys.
