# run_app_hidden.ps1
# Inicia o app em segundo plano ao ligar o PC.
$cwd = 'C:\RelogioPonto'

# Prioriza o Python da venv do projeto, se existir.
$venvPython = Join-Path $cwd '.venv\Scripts\python.exe'
if (Test-Path $venvPython) {
    $file = $venvPython
    $args = 'app.py'
} else {
    # Tenta localizar o executavel Python no sistema (caminho absoluto)
    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $cmd) { $cmd = Get-Command python3 -ErrorAction SilentlyContinue }

    if ($cmd) {
        $pythonPath = $cmd.Source
        $file = $pythonPath
        $args = 'app.py'
    } else {
        # tentar launcher 'py' (Windows)
        $pyCmd = Get-Command py -ErrorAction SilentlyContinue
        if ($pyCmd) {
            $file = $pyCmd.Source
            $args = '-3 app.py'
        } else {
            # fallback para 'python' sem caminho absoluto
            $file = 'python'
            $args = 'app.py'
        }
    }
}

$logFile = Join-Path $cwd 'startup.log'
$now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
try {
    $entry = "$now - Startup. Python: $file Args: $args WorkingDir: $cwd"
    Add-Content -Path $logFile -Value $entry -ErrorAction SilentlyContinue
} catch {
    # se falhar ao gravar log, nao impedir o start
}

Start-Process -FilePath $file -ArgumentList $args -WorkingDirectory $cwd -WindowStyle Hidden
