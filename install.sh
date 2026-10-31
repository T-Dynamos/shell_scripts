#!/usr/bin/env bash
# install.sh - One-line installer and updater for T-Dynamos shell_scripts
set -euo pipefail

REPO_URL="https://github.com/T-Dynamos/shell_scripts.git"
INSTALL_DIR="${HOME}/.local/bin"

echo "==> Installing / Updating T-Dynamos shell_scripts into ${INSTALL_DIR}..."
mkdir -p "${INSTALL_DIR}"

# If already inside the repo directory, install directly from working copy
if [[ -f "./td_script_info" && -f "./td_math2img" ]]; then
    echo "==> Installing directly from local repository..."
    install -m 755 -v td_* "${INSTALL_DIR}/"
else
    # Otherwise clone to an isolated temporary directory
    TMP_DIR="$(mktemp -d)"
    trap 'rm -rf "${TMP_DIR}"' EXIT

    echo "==> Fetching latest scripts from GitHub..."
    git clone --depth 1 "${REPO_URL}" "${TMP_DIR}" >/dev/null 2>&1
    install -m 755 -v "${TMP_DIR}"/td_* "${INSTALL_DIR}/"
fi

echo "==> Installation complete!"
echo "==> Installed scripts:"
ls -1 "${INSTALL_DIR}"/td_* 2>/dev/null | xargs -n 1 basename | sed 's/^/    - /'

if [[ ":$PATH:" != *":${INSTALL_DIR}:"* ]]; then
    echo ""
    echo "Notice: '${INSTALL_DIR}' is not currently in your PATH."
    echo "Add this to your ~/.bashrc or ~/.zshrc:"
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
fi
