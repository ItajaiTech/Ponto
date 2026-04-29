param(
    [string]$TargetIp = "127.0.0.1"
)

$hostsPath = "$env:windir\System32\drivers\etc\hosts"
$domains = @("ponto.local", "ponto.admin")

if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Execute este script como Administrador para alterar o arquivo hosts." -ForegroundColor Yellow
    Write-Host "Entradas desejadas:" -ForegroundColor Yellow
    foreach ($domain in $domains) {
        Write-Host "  $TargetIp $domain" -ForegroundColor Yellow
    }
    exit 1
}

if (-not (Test-Path $hostsPath)) {
    Write-Host "Arquivo hosts nao encontrado: $hostsPath" -ForegroundColor Red
    exit 1
}

$content = Get-Content $hostsPath -ErrorAction Stop

foreach ($domain in $domains) {
    $pattern = "(^|\s)" + [regex]::Escape($domain) + "($|\s)"
    if ($content | Select-String -Pattern $pattern) {
        Write-Host "$domain ja possui entrada no hosts. Revise manualmente se quiser trocar o IP." -ForegroundColor Yellow
        continue
    }

    Add-Content -Path $hostsPath -Value "`r`n$TargetIp $domain"
    Write-Host "Entrada adicionada: $TargetIp $domain" -ForegroundColor Green
}

Write-Host "Configuracao de hosts finalizada." -ForegroundColor Green
