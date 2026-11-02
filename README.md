## ⚠️ This Project assumes some intermediate knowledge
- configuring software to use PATH variable
- basic usage of terminal or command prompt
- installation of software suites
<br><br>
## 📝 A list of required tools / components for this project:
- Install Node.js: [download](https://nodejs.org/en/download)
- Verify the install in bash/cmd with the following commands:<br>
  `node --version` , `npm --version`
- With node and npm verified, install Angular CLI with the following command:<br>
  `npm install -g @angular/cli`
- Verify Angular CLI with:<br>
  `ng --version`
- Download and install PostgreSQL: [download](https://www.postgresql.org/download/)
- Verify PostgreSQL install by running:<br>
  `pg_isready` result should be :P0RT# - accepting connections
<br><br>
## 🛠️ Installing pgvector for PostgreSQL (required)
Download the latest pgvector from github here: [pgvector](https://github.com/pgvector/pgvector)<br>
<br>
⚠️ **`pgvector`** is released as a set of files that needs to be built for its parent OS.  <br>It can then be used by the running postgreSQL instance to persist vector embeddings. <br><br>
The github maintained by the authors of pgvector has detailed instructions for building to either OS.
<br><br>
## 🚀 Python / Fastapi setup

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

### install python

    uv python install

Installs the latest stable Python toolchain

### from the workspace directory root (/framework-demo)

    uv sync

Reads uv.lock and ensures your local environment matches the dependency tree found there or it downloads the dependencies needed for each service to run properly

### start the fastapi-service

    uv run --package fastapi-service uvicorn fastapi_service.main:app --reload

Starts the fastapi-service for testing on port 8000
