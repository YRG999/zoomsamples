# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Created `credentials.py` as a standalone utility for managing environment variables.
- Added support for **1Password secret references** (`op://`) in the `.env` file.
- Automatically resolves 1Password secrets using the `op` CLI.
- Integrated `get_credentials` into all core scripts:
  - `access_request.py`
  - `S2Saccesstoken.py`
  - `S2Srequest.py`
  - `zoom_dash.py`
  - `getaccountsettings.py`
  - `validatewebhook/app.py`
- Updated `.env.example` with instructions for using 1Password secret references.

## [1.0.1] - 2025-12-02

### Changed
- Major update to `.env.example`.
- Extensive file updates and structural improvements (currently in testing).

## [1.0.0] - 2024-09-06

### Added
- Initial project structure with Zoom API samples.
- OAuth 2.0 authorization flow (`access_request.py`).
- Server-to-Server (S2S) OAuth support (`S2Saccesstoken.py`, `S2Srequest.py`).
- Meeting dashboard participant retrieval (`zoom_dash.py`).
- Webhook validation sample (`validatewebhook/`).
- Utility for prettifying dictionary responses (`prettifydict.py`).
- Basic CLI for interaction (`zoom_cli.py`).

### Changed
- Improved `.gitignore` for security.
- Updated documentation and requirements.

## [0.1.0] - 2023-04-19

### Added
- First commit with basic Zoom API request samples and README.
