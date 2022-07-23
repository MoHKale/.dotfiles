clean -rf "$XDG_CONFIG_HOME/theme"

makedir "$XDG_CONFIG_HOME/theme"

link                                            \
  -p theme-                                     \
  "$XDG_BIN_DIR/battery-life"                   \
  "$XDG_BIN_DIR/cpu-load"                       \
  "$XDG_BIN_DIR/disk-free"                      \
  "$XDG_BIN_DIR/docker"                         \
  "$XDG_BIN_DIR/github-notifications"           \
  "$XDG_BIN_DIR/mpd-playback"                   \
  "$XDG_BIN_DIR/mullvad-vpn"                    \
  "$XDG_BIN_DIR/nordvpn"                        \
  "$XDG_BIN_DIR/notmuch"                        \
  "$XDG_BIN_DIR/status-misc"                    \
  "$XDG_BIN_DIR/transmission"
