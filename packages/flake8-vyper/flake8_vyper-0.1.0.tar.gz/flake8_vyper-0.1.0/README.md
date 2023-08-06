# flake8-vyper

Flake8 vyper plugin.  This plugin is experimental, so, beware.

## Install

    pip install flake8-vyper

## VyperFilterPlugin

This plugin filters out false-positives for expected Vyper globals and types.

### Usage

Alter your `.flake8` config so that the following lines are included in the
`[flake8]` section of the INI.

    [flake8]
    format = vyper_filter
    filename = *.py,*.vy

Alternatively, you can specify this with the `flake8` CLI command:

    flake8 --format=vyper_filter
