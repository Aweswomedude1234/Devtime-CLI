#!/bin/sh

set -e

INSTALL_DIR="$HOME/.local/bin"
DEVTime_URL="https://github.com/Aweswomedude1234/Devtime-CLI/releases/download/v1.0.0/devtime"

mkdir -p "$INSTALL_DIR"

echo "Installing DevTime . . ."
curl -L "$DEVTime_URL" -o "$INSTALL_DIR/devtime"
chmod +x "$INSTALL_DIR/devtime"

if ! grep -q 'HOME/.local/bin' "$HOME/.zshrc" 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
fi

echo ""
echo "DevTime installed successfully."
echo ""
echo "Open a new terminal and run: "
echo " devtime"