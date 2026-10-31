## 🚀 getting started
This project uses Python 3.15.2 with **`uv`**, a fast, all-in-one Python package and workspace manager written in Rust. It handles dependencies and can help manage or download Python versions.

### install `uv`
Choose your operating system to install the standalone **`uv`** binary:

* **macOS & Linux:**
    ```bash
    curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh

* **powershell:**
    ```bash
    -ExecutionPolicy ByPass -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"

### clone the repository
`git clone https://github.com/Not3Worthy/framework-demo.git`

## environment setup

### if needed, install python

    uv python install

Installs the latest stable Python toolchain

### from the workspace directory root (/framework-demo)

    uv sync

Reads uv.lock and ensures your local environment matches the dependency tree found there or it downloads the deps needed for each service to run properly

### start the fastapi-service

    uv run --package fastapi-service uvicorn fastapi_service.main:app --reload

Starts the fastapi-service for testing on port 8000