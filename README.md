# Tmux Cookie Cutter

Letting you define your tmux window setup configuration, pre-run environment setup and launch programs as you start a new tmux session.

## Installation
### Installation with [Tmux Plugin Manager](https://github.com/tmux-plugins/tpm) (recommended)

Add plugin to the list of TPM plugins in `.tmux.conf`:

```shell
set -g @plugin 'AranBorkum/tmux-cookie-cutter'
```

Hit `prefix + I` to fetch the plugin and source it.

### Manual Installation

Clone the repo:

```shell
$ git clone https://github.com/AranBorkum/tmux-cookie-cutter ~/clone/path
```

Add this line to the bottom of `.tmux.conf`:

```shell
run-shell ~/clone/path/cookie-cutter.tmux
```

Reload TMUX environment:

```shell
# type this in terminal
$ tmux source-file ~/.tmux.conf
```

## Usage
Create a `.tmux-cookie-cutter.yaml` file in your `$HOME/.config/` directory _or_ a bespoke one in the root of your project. Configure this with the following values:

```yaml
default_windows:
  - name: "neovim"
    envvars:
        - VARIABLE_1=...
        - VARIABLE_2=...
    setup_command: "source .venv/bin/activate"
    command: "nvim"
  - name: "terminal"
    envvars:
        - VARIABLE_1=...
        - VARIABLE_2=...
    setup_command: "source .venv/bin/activate"
    command:
    panes:
        - split_direction: "vertical"
        - split_direction: "horizontal"
          command: ./manage runserver
```

Optionally, you can set the python interpreter to use, it defaults to python3:

```shell
set-option -g @cookie_cutter_python "python3"
```

Be sure it has PyYAML available, you can use `uv` to run it with the `pyyaml` package:

```shell
set-option -g @cookie_cutter_python "uv run --with pyyaml"
```
