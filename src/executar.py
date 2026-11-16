"""Roda o projeto de ponta a ponta: origem -> bruto -> tratado -> modelo -> alerta -> auditoria."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import alerta  # noqa: E402
import auditoria  # noqa: E402
import camadas  # noqa: E402
from config import MODELO, TRATADO  # noqa: E402


def etapa(nome, funcao, *args):
    inicio = time.time()
    print(f"[{nome}]")
    resultado = funcao(*args)
    print(f"  pronto em {time.time() - inicio:.0f}s")
    return resultado


if __name__ == "__main__":
    linhagem = []
    etapa("1. bruto", camadas.carregar_bruto, linhagem)
    etapa("2. tratado", camadas.construir, "tratado", "2_tratado", TRATADO, "2. Tratado", linhagem)
    etapa("3. modelo", camadas.construir, "modelo", "3_modelo", MODELO, "3. Modelo", linhagem)
    etapa("4. alerta", alerta.executar, linhagem)
    verificacoes = etapa("5. auditoria", auditoria.executar, linhagem)
    if (verificacoes.situacao == "Falhou").any():
        sys.exit("O pipeline terminou com verificações reprovadas.")
