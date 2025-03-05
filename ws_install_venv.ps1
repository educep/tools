# run it:
# .\ws_install_venv.ps1 -envName tools

# Get the environment name from the command line
param (
    [string]$envName
)

# Check if environment name is provided
if (-not $envName) {
    Write-Output "Please provide an environment name using --env <name>"
    exit
}

# Check if 'uv' is installed
$uvInstalled = $false

try {
    $uvVersion = uv --version 2>$null
    if ($uvVersion) {
        $uvInstalled = $true
        Write-Output "uv is already installed (Version: $uvVersion)."
    }
} catch {
    Write-Output "uv is not installed. Installing now..."
}

# Install 'uv' if not installed
if (-not $uvInstalled) {
    Write-Output "Installing uv..."
    Invoke-Expression (New-Object System.Net.WebClient).DownloadString('https://astral.sh/uv/install.ps1')

    # Verify installation
    try {
        $uvVersion = uv --version 2>$null
        if ($uvVersion) {
            Write-Output "uv installed successfully (Version: $uvVersion)."
            $uvInstalled = $true
        } else {
            Write-Output "uv installation failed. Please install manually."
            exit 1
        }
    } catch {
        Write-Output "uv installation failed. Please install manually."
        exit 1
    }
}

# Get the current username
$username = $env:USERNAME

# Define the path to the virtual environment based on the current user
$envPath = "C:/Users/$username/envs/$envName"

# Check if the virtual environment folder exists
if (Test-Path $envPath) {
    Write-Output "Virtual environment already exists. Skipping creation."
} else {
    # Create a virtual environment with uv
    Write-Output "Creating virtual environment '$envName'..."
    uv venv $envPath
}

# Activate the virtual environment
& "$envPath/Scripts/Activate.ps1"

# Install dependencies using uv
Write-Output "Installing dependencies from requirements.txt..."
# uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
uv pip install -r requirements.txt

Write-Output "Virtual environment '$envName' has been set up with uv."
