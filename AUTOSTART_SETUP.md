# Configurar Auto-Start do RelogioPonto

## ⚠️ REQUISITOS
- Privilégios de **ADMINISTRADOR** no Windows
- Python instalado em `C:\RelogioPonto\.venv\Scripts\python.exe`
- Virtual environment configurado

---

## ✅ PASSO 1: Registrar o Auto-Start

1. Abra o explorador de arquivos
2. Navegue para: `C:\RelogioPonto\`
3. **Clique com botão direito** no arquivo `registrar_autostart.bat`
4. Selecione: **"Executar como administrador"**
5. Pressione **[Enter]** quando pedido

O script irá:
- Remover qualquer tarefa anterior
- Registrar a nova tarefa no Windows Task Scheduler
- Confirmar o sucesso

---

## ✅ PASSO 2: Testar o Auto-Start Configurado

### Opção A: Reiniciar o Windows
Reinicie o computador e verifique se o RelogioPonto inicia automaticamente.

### Opção B: Testar Manualmente (sem reiniciar)
Execute no PowerShell (como administrador):
```powershell
C:\RelogioPonto\auto_start_flask_v2.ps1
```

---

## 📋 Verificar o Status

### Ver a tarefa no Task Scheduler
1. Pressione `Windows + R`
2. Digite: `taskschd.msc`
3. Procure por: **RelogioPonto** (em Library → Microsoft → Windows)

### Ver logs de inicialização
- Arquivo: `C:\RelogioPonto\auto_start.log`
- Este arquivo registra cada tentativa de inicialização

### Verificar se o Flask está rodando
```powershell
Get-Process python | Where-Object {$_.CommandLine -like '*app.py*'}
```

---

## 🔧 Como Desabilitar o Auto-Start

Se precisar desabilitar o auto-start, execute no PowerShell (como administrador):
```powershell
schtasks /delete /tn "RelogioPonto" /f
```

---

## 🚨 Solução de Problemas

### 1. Erro ao registrar: "Acesso negado"
→ Abra o `registrar_autostart.bat` **como administrador**

### 2. O programa não inicia após reiniciar
→ Verifique o arquivo de log:
```powershell
Get-Content "C:\RelogioPonto\auto_start.log"
```

### 3. A janela do Flask fica visível
→ Isso é normal com o script v2 (executa em background)

### 4. O Python não foi encontrado
→ Confirme que existe: `C:\RelogioPonto\.venv\Scripts\python.exe`
→ Se não existir, recrie o virtual environment:
```powershell
cd C:\RelogioPonto
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

---

## 📊 O que acontece no Auto-Start

1. Windows inicia o script PowerShell
2. Aguarda **30 segundos** (importante se usar rede externa)
3. Remove sessões anteriores de `session.db`
4. Inicia o Flask em background, sem janela visível
5. Registra tudo em `auto_start.log`

---

## 🔗 Mais Informações

Arquivo de configuração: `auto_start_flask_v2.ps1`
Tarefa: Task Scheduler → RelogioPonto → OnLogon
Logs: `C:\RelogioPonto\auto_start.log`
