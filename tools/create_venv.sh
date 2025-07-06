#!/bin/bash
#-----------------------------------------
# Set-up the global environment variables
#-----------------------------------------
SCRIPT_FULL_PATH=$(readlink -f "${BASH_SOURCE[0]}")
SCRIPT_DIR_PATH="${SCRIPT_FULL_PATH%/*}"

#-----------------------------------------
# Error Handling: Ensure virtual environment is deactivated on failure
#-----------------------------------------
cleanup() {
    if [[ -n "$VIRTUAL_ENV" ]]; then
        echo "⚠️ Deactivating the virtual environment..."
        deactivate
    fi
}
trap cleanup EXIT  # This runs cleanup() when the script exits (on error or completion)

#-----------------------------------------
# Create Python Virtual environment and
# Install the package to it.
#-----------------------------------------
python3 -m venv "${SCRIPT_DIR_PATH}/../simulation_venv" || { echo "❌ Cannot create the Python Virtual environment"; exit 1; }
source "${SCRIPT_DIR_PATH}/../simulation_venv/bin/activate" || { echo "❌ Cannot source <VENV>/bin/activate"; exit 1; }
pip install --upgrade pip || { echo "❌ Cannot upgrade the PIP version"; exit 1; }

# Ensure no conflicts by uninstalling first
pip uninstall -y cont_sys_sim

# Install package in editable mode with force-reinstall
pip install --force-reinstall -e "${SCRIPT_DIR_PATH}/.." || { echo "❌ Failed to install the package"; exit 1; }

echo "✅ Installation completed successfully!"
