# youtube
Terminal based YouTube client with Vim bindings

![image](https://user-images.githubusercontent.com/70523266/142730098-1056d385-c966-4ce4-9e9b-f7c4b77d2714.png)


Full functionality assumes you have `youtube-dl`, `mpv`, `newsboat`, and [`linkhandler`](https://github.com/LukeSmithxyz/voidrice/blob/master/.local/bin/linkhandler) installed, as well as all the `requests` Python library (all others are included). Also included is `copytext`, which can be placed anywhere on your `$PATH` to support url copying.

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
  - `a`: open link in youtube-dl to download audio
  - `m`: open link in mpv
  - `o`: open link in default web browser
  - `l`: open link in linkhandler
  - `n`: add channel to newsboat subscriptions
  - `c`: copy video url to clipboard
