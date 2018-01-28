Text-mode interface for provisioning cloud nodes.

WARNING: Pre-alpha, I don't recommend using this yourself.

Installation (development)
=====
  pip install -e .

Configuration
=====
  sudo cp config.yaml.example /etc/boxes.yaml

Set the `api_token` to your DigitalOcean access token.

Usage
=====
  boxes

![Main menu](docs/screenshots/main_menu.png "Main menu")

![Node menu](docs/screenshots/node_menu.png "Node menu")

TODO
=====
* Parse and pretty-print all responses.
* Progress/wait popup, or async operations.  Mode to queue operations and
confirm execution.
* Ui segments window into sections, e.g. log window
* Also write to log file.
* Rebuild and resize are pending merge of
https://github.com/apache/libcloud/pull/1169
* Ui.menu to abstract key-based menus or list menus where we have to autogen
the keys
* Menu item for running cloud-level commands.  Parse and explain what groups
and hosts ansible playbooks will run on by default.
* Main loop rather than exiting after a single command.  Stay in submenus until
escape key.
* Recently used hotlist.
* First check for config in CWD/.boxes.yaml, ~/.boxes.yaml, maybe cascade
between each.
* Realtime command output
