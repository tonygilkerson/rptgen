# rptgen

Report Generator

## Setup

```sh
mkdir .venv

python3 -m venv .venv
source .venv/bin/activate
pip install poetry



## Dev Env
echo "TODO=todo >> .env

# Install project dependencies
# see: https://python-poetry.org/docs/basic-usage/
poetry install

# If you want to install the dependencies only, run the install command with the --no-root flag:
poetry install --no-root
```

## Dev

```sh
python3 -m src.main
```

## Dist

Python wheel

```sh
. .venv/bin/activate # if not done already

# dev install to see if it works
poetry build
poetry install
rptgen

# build for dist
poetry build
```

## As a User

To use `rptgen`, as opposed to develop `rptgen` then do the following:

```sh
# Make sure the latest release is installed
pip3 install ~/github/tonygilkerson/rptgen/dist/rptgen-0.1.0-py3-none-any.whl --user

# or if not using a venv  
pip3 install ~/github/tonygilkerson/rptgen/dist/rptgen-0.1.0-py3-none-any.whl --break-system-packages --user  

# In a shell with no active python venv
rptgen
```
