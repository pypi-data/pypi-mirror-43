# flake8-vyper

Flake8 wrapper to support Vyper.  This is experimental, so, beware.

## Install

    pip install flake8-vyper

## Usage

You can run flake8 with this wrapper with the command `flake8-vyper`.

## Configuration

You can use all the same CLI options as flake8, but config should be done in the `flake8-vyper`
section to prevent conflicts.  Here's an example `tox.ini` for a project with python and vyper:

    [flake8]
    exclude = .git,__pycache__,build
    max-line-length = 100
    filename = *.py

    [flake8-vyper]
    exclude = .git,__pycache__,build
    max-line-length = 100
    filename = *.vy
