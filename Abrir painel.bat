@echo off
setlocal
rem Aponta o painel para a pasta de dados deste projeto, esteja ela onde estiver,
rem e abre o projeto no Power BI Desktop. Feche o Power BI antes de usar.
set "RAIZ=%~dp0"
powershell -NoProfile -Command "$ErrorActionPreference = 'Stop'; $raiz = $env:RAIZ.TrimEnd('\'); $dados = Join-Path (Join-Path $raiz 'dados') '3_modelo'; $arq = Join-Path (Join-Path (Join-Path (Join-Path $raiz 'powerbi') 'AntesDaNotaVermelha.SemanticModel') 'definition') 'expressions.tmdl'; if (-not (Test-Path -LiteralPath (Join-Path $dados 'dTurma.parquet'))) { Write-Host 'Nao encontrei a pasta dados\3_modelo ao lado deste arquivo. Extraia o zip inteiro antes de abrir.'; exit 1 }; $q = [char]34; $utf8 = New-Object System.Text.UTF8Encoding($false); $linhas = [System.IO.File]::ReadAllLines($arq, $utf8); $achou = $false; for ($i = 0; $i -lt $linhas.Length; $i++) { if ($linhas[$i].StartsWith('expression PastaDados = ')) { $linhas[$i] = 'expression PastaDados = ' + $q + $dados + $q + ' meta [IsParameterQuery=true, Type=' + $q + 'Text' + $q + ', IsParameterQueryRequired=true]'; $achou = $true } }; if (-not $achou) { Write-Host 'Nao encontrei o parametro PastaDados no modelo.'; exit 1 }; [System.IO.File]::WriteAllLines($arq, $linhas, $utf8); Write-Host ('Dados apontados para: ' + $dados)"
if errorlevel 1 goto erro
start "" "%~dp0powerbi\AntesDaNotaVermelha.pbip"
exit /b 0
:erro
echo.
echo Nao foi possivel ajustar o caminho dos dados. Veja a mensagem acima.
pause
exit /b 1
