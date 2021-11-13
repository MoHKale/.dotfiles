import                                          \
  git                                           \
  info                                          \
  editors

# Also installs some package managers such as pip or gem.
import -b langs/*

import -b                                       \
  bat                                           \
  browsers/*                                    \
  cava                                          \
  cheat                                         \
  desktop/login/sddm                            \
  desktop/plasma                                \
  dolphin                                       \
  dropbox                                       \
  games/*                                       \
  gdb                                           \
  gimp                                          \
  gotop                                         \
  hledger                                       \
  hyper                                         \
  imv                                           \
  ipython                                       \
  konsole                                       \
  korganizer                                    \
  lf                                            \
  lint/*                                        \
  mc                                            \
  media/*                                       \
  pass                                          \
  polybar                                       \
  ranger                                        \
  ripgrep                                       \
  spectacle                                     \
  sxiv                                          \
  terminal/*                                    \
  thefuck                                       \
  tmux                                          \
  transmission                                  \
  wget                                          \
  wine                                          \
  zathura

if bots mail.server mail.client; then
  import mail
fi
