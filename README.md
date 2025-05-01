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

### run

```sh
source .venv/bin/activate

# Get daily info something like
$ scp tgilkerson@udev:/home/tgilkerson/gitlab-rs-glu/tony.gilkerson/notebook/reporting/msr/2025-04/thedaily04.md ./.temp/rptwrk04/

# Redact
python3 src/main.py redact \
  -i .temp/rptwrk04/thedaily04.md \
  -r .temp/keep/replacements.yaml 
  

# Generate report in a scratch workspace
```sh
cp .temp/rptwrk04/thedaily04\(redacted\).md  ~/temp/rpt-scratch
# open workspace and follow instruction in the readme
code ~/temp/rpt-scratch

# Over in the scratch work space the msr(redacted).md was created and copied back into this project
# i.e. .temp/rptwrk04/msr(redacted).md
#
# Now back in this project, unredact to create msr(unredacted).md
#
cp ~/temp/rpt-scratch/msr\(redacted\).md .temp/rptwrk04/
python src/main.py  unredact \
  --msr_redacted .temp/rptwrk04/msr\(redacted\).md \
  -r .temp/keep/replacements.yaml 
  
# Generate a pdf
command-shif-p -> Markdown: Convert Document

# send it over
scp ./.temp/rptwrk04/msr\(unredacted\).md tgilkerson@udev:/home/tgilkerson/gitlab-rs-glu/tony.gilkerson/notebook/reporting/msr/2025-04 


```
