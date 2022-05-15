install() {
  link ~/.Xresources                                    \
       ~/.xinitrc                                       \
       ~/.xprofile                                      \
       xbindkeysrc:"$XDG_CONFIG_HOME/xbindkeys/config"
  link-to "$XDG_BIN_DIR/" ./cmds/*
  link-to "$XDG_CONFIG_HOME/Xresources/" ./Xresources.d/*
  run-cmd touch "$XDG_CONFIG_HOME/Xresources/local"

  packages yay:xorg,xorg-xinit,xbindkeys,xorg-setxkbmap,wmctrl,xdotool,xclip \
           apt:xclip
  packages pip:notify-send

  if [ -e "$DOTFILES/setup/cache/arch" ]; then
    info 'Installing Graphics Drivers for Xorg'
    graphics_card=$(lspci | grep -e VGA -e 3D |
                      rev | cut -d: -f1 | rev |
                      sed -e 's/^ *//' -e 's/ *$//' |
                      tr '[:upper:]' '[:lower:]')

    if package pacman; then
      case "$graphics_card" in
        *intel*)
          package pacman xf86-video-intel
          ;;
        *vmware*)
          package pacman xf86-video-vmware
          ;;
        *nvidia*)
          package pacman xf86-video-nouveau
          ;;
        *)
          error "Unable to determine graphics card: $graphics_card"
          ;;
      esac
    fi
  fi
}
