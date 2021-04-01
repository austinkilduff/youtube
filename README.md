# youtube
Terminal based YouTube client with Vim bindings

Full functionality assumes you have `youtube-dl`, `mpv`, `newsboat`, and [`linkhandler`](https://github.com/LukeSmithxyz/voidrice/blob/master/.local/bin/linkhandler) installed, as well as all the `requests` Python library (all others are included).

Keybindings:
* `INSERT` mode:
  - `ESC`: enter `NORMAL` mode
  - `ENTER`: search for search term
* `NORMAL` mode:
  - `i`: enter `INSERT` mode
  - `q`: quit program
  - `j`: move cursor down
  - `k`: move cursor up
  - `y`: open link in youtube-dl
  - `m`: open link in mpv
  - `o`: open link in default web browser
  - `l`: open link in linkhandler
  - `c`: add channel to newsboat subscriptions
