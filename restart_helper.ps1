# restart_helper.ps1
# Espera um curto período, depois inicia uma nova instância da aplicação
Start-Sleep -Seconds 1
$cwd = 'C:\RelogioPonto'
$file = Join-Path $cwd '.venv\Scripts\python.exe'
$args = 'app.py'

if (-not (Test-Path $file)) {
	$logFile = Join-Path $cwd 'restart.log'
	$now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
	Add-Content -Path $logFile -Value "$now - ERRO: Python .venv nao encontrado em $file" -ErrorAction SilentlyContinue
	exit 1
}

# Inicia a aplicação em uma janela de terminal visível
# Registrar tentativa de reinício
$logFile = Join-Path $cwd 'restart.log'
$now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
try {
	$entry = "$now - Iniciando reinício. Python: $file Args: $args WorkingDir: $cwd"
	Add-Content -Path $logFile -Value $entry -ErrorAction SilentlyContinue
} catch {
	# se falhar ao gravar log, não impedir o restart
}

Start-Process -FilePath $file -ArgumentList $args -WorkingDirectory $cwd -WindowStyle Normal
