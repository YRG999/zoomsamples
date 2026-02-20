# request_handler.py
# Usage: Centralized request handling for Zoom API interactions

import requests
import access_request

DEFAULT_TIMEOUT = 10


def _build_headers(extra_headers=None):
    access_token = access_request.access_token
    if not access_token:
        raise RuntimeError("Missing access token. Authorize the application first.")
    headers = {"Authorization": f"Bearer {access_token}"}
    if extra_headers:
        headers.update(extra_headers)
    return headers


def _refresh_tokens():
    tokens = access_request.refresh_access_token(
        access_request.client_id,
        access_request.client_secret,
        access_request.refresh_token,
    )
    access_request.access_token = tokens["access_token"]
    access_request.refresh_token = tokens["refresh_token"]
    return tokens


def make_request(
    resource="user_info",
    *,
    method=None,
    endpoint=None,
    params=None,
    data=None,
    json=None,
    headers=None,
    timeout=DEFAULT_TIMEOUT,
):
    if resource == "user_info":
        method = method or "GET"
        endpoint = endpoint or "https://api.zoom.us/v2/users/me"
    elif not (method and endpoint):
        raise ValueError("Custom requests require both method and endpoint.")

    method = method.upper()
    request_headers = _build_headers(headers)

    try:
        response = requests.request(
            method,
            endpoint,
            params=params,
            data=data,
            json=json,
            headers=request_headers,
            timeout=timeout,
        )
    except requests.RequestException as exc:
        raise requests.RequestException(f"Network error during Zoom API request: {exc}") from exc

    if response.status_code == 401:
        if not access_request.refresh_token:
            raise requests.HTTPError(
                f"Unauthorized request: {response.text}",
                response=response,
            )
        _refresh_tokens()
        request_headers = _build_headers(headers)
        try:
            response = requests.request(
                method,
                endpoint,
                params=params,
                data=data,
                json=json,
                headers=request_headers,
                timeout=timeout,
            )
        except requests.RequestException as exc:
            raise requests.RequestException(f"Network error during Zoom API retry: {exc}") from exc

    if not response.ok:
        raise requests.HTTPError(
            f"Zoom API request failed: {response.status_code} - {response.text}",
            response=response,
        )

    return response.json()


def get_user_info():
    return make_request("user_info")
