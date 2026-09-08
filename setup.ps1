# One-shot setup for Windows PowerShell. Run from the repo root:
#   .\setup.ps1
# If scripts are blocked:  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# Sets up the backend (venv, dependencies, migrations, seed data, tests)
# and the frontend (yarn dependencies, type check, tests).
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$repoRoot = $PSScriptRoot

$py = $null
foreach ($candidate in @("py -3", "python3", "python")) {
    try {
        $version = Invoke-Expression "$candidate -c `"import sys; print(sys.version_info >= (3, 10))`"" 2>$null
        if ($version -eq "True") { $py = $candidate; break }
    } catch {}
}
if (-not $py) {
    Write-Error "Python 3.10 or newer is required. Install it from https://www.python.org/downloads/ and re-run .\setup.ps1"
}
Write-Host "Using: $(Invoke-Expression "$py --version")"

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Error "Node 20 or newer is required and node was not found on PATH. Install it from https://nodejs.org/ and re-run .\setup.ps1"
}
$nodeMajor = [int](node -p "process.versions.node.split('.')[0]")
if ($nodeMajor -lt 20) {
    Write-Error "Node 20 or newer is required; found $(node --version). Install it from https://nodejs.org/ and re-run .\setup.ps1"
}
Write-Host "Using node: $(node --version)"

# frontend/yarn.lock is the frontend lockfile, so the install runs through yarn.
if (-not (Get-Command yarn -ErrorAction SilentlyContinue)) {
    Write-Error "yarn is required and was not found on PATH. Install it with 'corepack enable' or 'npm install -g yarn', then re-run .\setup.ps1"
}
Write-Host "Using yarn: $(yarn --version)"

Write-Host ""
Write-Host "Backend..."
Set-Location (Join-Path $repoRoot "backend")
if (-not (Test-Path ".venv")) { Invoke-Expression "$py -m venv .venv" }
& .\.venv\Scripts\Activate.ps1

Write-Host "Installing dependencies.."
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt

Set-Location "src"
python manage.py migrate --verbosity 0
python manage.py seed_data
Write-Host "Data seeded: users, purchase requests, approvals"

Set-Location ".."
# The API test is an unimplemented stub, so a failing test here is expected.
# Anything other than "tests ran and some failed" is a real setup problem.
$ErrorActionPreference = "Continue"
python -m pytest
$pytestStatus = $LASTEXITCODE
$ErrorActionPreference = "Stop"
if ($pytestStatus -gt 1) {
    Write-Error "pytest could not run. The backend is not set up correctly."
}

Write-Host ""
Write-Host "Frontend..."
Set-Location $repoRoot
# yarn v1 reports an unmet @babel/core peer dependency for every plugin the
# unused @babel/preset-* devDependencies pull in. Neither those nor the
# workspaces notice are actionable here, so they are filtered out.
$ErrorActionPreference = "Continue"
yarn --cwd frontend install --frozen-lockfile 2>&1 |
    Where-Object { $_ -notmatch 'has unmet peer dependency' -and $_ -notmatch 'Workspaces can only be enabled' }
$yarnStatus = $LASTEXITCODE
$ErrorActionPreference = "Stop"
if ($yarnStatus -ne 0) {
    Write-Error "yarn install failed. The frontend is not set up correctly."
}

# The type check and the test suite are the two checks the exercise ships with;
# running them here surfaces a broken toolchain at setup rather than later.
yarn --cwd frontend typecheck
yarn --cwd frontend test

Write-Host ""
Write-Host "Setup complete."
Write-Host ""
Write-Host "Ready to start exercise in backend/EXERCISE.md and frontend/EXERCISE.md."
Write-Host ""
Write-Host "To run the project, in two terminals from the repo root:"
Write-Host ""
Write-Host "  Frontend  yarn --cwd frontend dev"
Write-Host "  API       backend\.venv\Scripts\Activate.ps1; cd backend\src; python manage.py runserver 8000"
Write-Host ""
Write-Host "  Frontend  http://localhost:5173"
Write-Host "  API       http://localhost:8000/api/purchase-requests/"
