# flake8-vyper

Flake8 wrapper to support Vyper.  This is experimental, so, beware.

## Install

    pip install flake8-vyper

## Usage

You can run flake8 with this wrapper with the command `flake8-vyper`.

## Configuration

Alter your `.flake8` config so that the `filename` is set for your Vyper files
in the `[flake8]` section of the INI.

    [flake8]
    filename = *.vy

Alternatively, you can specify this with the `flake8` CLI command:

    flake8-vyper --filename="*.vy"
