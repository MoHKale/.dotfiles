curl -LO 'https://raw.githubusercontent.com/ycm-core/ycmd/master/ycmd/default_settings.json' 2>/dev/null && python3 -u "${YCMD_PATH:-${HOME}/.vim/plugged/YouCompleteMe/third_party/ycmd/ycmd}" --options_file default_settings.json