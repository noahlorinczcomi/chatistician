# server.py is not part of the distro for the user
pyinstaller \
    --onefile \
    --icon="../icons/AppIcon.icns" \
    --name Chatv0 \
    --add-data "local_config.yaml:." \
    --add-data "utils.py:." \
    local_client.py
