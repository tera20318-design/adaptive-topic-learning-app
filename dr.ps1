param(
    [Parameter(Position = 0)]
    [string]$ModeOrTheme,

    [Parameter(Position = 1)]
    [string]$Theme,

    [string]$BaseDir,

    [switch]$Force
)

$ErrorActionPreference = "Stop"

function Show-Usage {
    Write-Host 'Usage: .\dr.ps1 "<research theme>"' -ForegroundColor Yellow
    Write-Host '       .\dr.ps1 v2 "<research theme>"' -ForegroundColor Yellow
}

function Resolve-PythonCommand {
    $candidates = @(
        @{ Executable = "py"; PrefixArgs = @("-3") },
        @{ Executable = "python"; PrefixArgs = @() },
        @{ Executable = "python3"; PrefixArgs = @() }
    )

    foreach ($candidate in $candidates) {
        if (-not (Get-Command $candidate.Executable -ErrorAction SilentlyContinue)) {
            continue
        }

        & $candidate.Executable @($candidate.PrefixArgs + @("-c", "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)")) | Out-Null
        if ($LASTEXITCODE -eq 0) {
            return $candidate
        }
    }

    throw "Python 3.10+ was not found. Install Python or use the py launcher, then run this command again."
}

function Get-SafeSlug([string]$Value, [string]$Fallback) {
    $slug = [regex]::Replace($Value.Trim(), "[^A-Za-z0-9._-]+", "-")
    $slug = $slug.Trim([char[]]"-._")
    if ([string]::IsNullOrWhiteSpace($slug)) {
        return $Fallback
    }
    return $slug
}

function Resolve-BaseDir([string]$RepoRoot, [string]$RequestedBaseDir) {
    if ([System.IO.Path]::IsPathRooted($RequestedBaseDir)) {
        return $RequestedBaseDir
    }
    return Join-Path $RepoRoot $RequestedBaseDir
}

if ([string]::IsNullOrWhiteSpace($ModeOrTheme)) {
    Show-Usage
    exit 1
}

$mode = "v1"
switch ($ModeOrTheme.ToLowerInvariant()) {
    "v1" { $mode = "v1" }
    "v2" { $mode = "v2" }
    default { $Theme = $ModeOrTheme }
}

if ([string]::IsNullOrWhiteSpace($Theme)) {
    Show-Usage
    exit 1
}

if ([string]::IsNullOrWhiteSpace($BaseDir)) {
    $BaseDir = if ($mode -eq "v2") { "runs-v2" } else { "runs" }
}

$repoRoot = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
$today = Get-Date -Format "yyyy-MM-dd"
$python = Resolve-PythonCommand
$baseDirPath = Resolve-BaseDir -RepoRoot $repoRoot -RequestedBaseDir $BaseDir

if ($mode -eq "v2") {
    $slugBase = Get-SafeSlug -Value $Theme -Fallback "research-v2-case"
    $caseDir = Join-Path $baseDirPath "$today-$slugBase"
    $requestPath = Join-Path $caseDir "request.json"
    $bundleDir = Join-Path $caseDir "bundle"
    $pythonArgs = @(
        "research-os-v2/scripts/init_case.py",
        $Theme,
        "--base-dir",
        $BaseDir,
        "--as-of-date",
        $today
    )
}
else {
    $slugBase = Get-SafeSlug -Value $Theme -Fallback ("research-" + (Get-Date -Format "HHmmss"))
    $caseDir = Join-Path $baseDirPath "$today-$slugBase"
    $pythonArgs = @(
        "research-os/scripts/init_research_project.py",
        $caseDir,
        "--title",
        $Theme
    )
}

if ($Force) {
    $pythonArgs += "--force"
}

Push-Location $repoRoot
try {
    & $python.Executable @($python.PrefixArgs + $pythonArgs)
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}
finally {
    Pop-Location
}

Write-Host ""
Write-Host "Research case created:" -ForegroundColor Green
Write-Host "  $caseDir"
Write-Host ""
Write-Host "Python command:" -ForegroundColor DarkGray
Write-Host "  $($python.Executable) $($python.PrefixArgs -join ' ')"
Write-Host ""
Write-Host "Next:" -ForegroundColor Cyan

if ($mode -eq "v2") {
    Write-Host "  1. Open request.json and notes.md in the new case"
    Write-Host "  2. Confirm the starter brief, especially reader, question, and jurisdiction"
    Write-Host "  3. Add real source_packets only after you have evidence"
    Write-Host "  4. Run: $($python.Executable) $($python.PrefixArgs -join ' ') research-os-v2/scripts/run_case.py ""$requestPath"" ""$bundleDir"""
}
else {
    Write-Host "  1. Open TASK.md and PLANS.md in the new case"
    Write-Host "  2. In Claude Code, /dr ""$Theme"" starts the same canonical pseudo-Pro kickoff flow"
    Write-Host "  3. Use research-os/prompts/parent_agent_prompt.md as the single pseudo-Pro master prompt"
    Write-Host "  4. Continue from the new case with source logging, claim extraction, red-team review, and final report work"
}
