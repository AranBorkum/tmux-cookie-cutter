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
Create a `.tmux-cookie-cutter.toml` file in your `$HOME/.config/` directory _or_ a bespoke one in the root of your project. Configure this with the following values:

```toml
[shared]
setup_command = "neofetch"
envvars = [
    { VARIABLE_1 = ... },
    { VARIABLE_2 = ... },
]

[neovim]
command = "nvim"
setup_command = "source .venv/bin/activate"
envvars = [
    { VARIABLE_3 = ... },
    { VARIABLE_4 = ... },
]

[terminal]
name = "terminal"
setup_command = "source .venv/bin/activate"
envvars = [
    { VARIABLE_4 = ... },
    { VARIABLE_5 = ... },
]
panes = [
    { split_direction = "vertical", size = 25 },
    { split_direction = "horizontal", size = 40 },
]
```

The name field is optional. By default the name of the window will match the value in the square brackets. If you specify a name value this will override this value, allowing you to have multiple windows with the same name.

Shared values will be applied to every tmux window, removing the need for repetition. You can define `envvars` and `setup_command` only as shared values.
