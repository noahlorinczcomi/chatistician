# server.py is not part of the distro for the user
pyinstaller \
    --onefile \
    --icon="../icons/AppIcon.icns" \
    --name Chatv0 \
    --add-data "config.yaml:." \
    --add-data "utils.py:." \
    client.py
