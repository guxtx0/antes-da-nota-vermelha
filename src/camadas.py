"""As três camadas de dados. O Python só orquestra: toda transformação está nos arquivos .sql."""
import io
import urllib.request
import zipfile

import duckdb

from config import ARQUIVOS, BRUTO, MODELO, ORIGEM, REFERENCIAS, SQL, TRATADO, URL_OULAD

DESCRICOES = {
    "bruto": "Cópia fiel do arquivo de origem, tudo como texto",
    "tratado": "Tipos corrigidos, vazios padronizados, duplicatas resolvidas, textos em português",
    "modelo": "Tabela do modelo estrela lida pelo Power BI",
}


def conectar():
    """Abre o DuckDB e expõe cada camada já gravada como um esquema (bruto, tratado, modelo, ref)."""
    con = duckdb.connect()
    for esquema, pasta in (("bruto", BRUTO), ("tratado", TRATADO), ("modelo", MODELO)):
        con.execute(f"CREATE SCHEMA IF NOT EXISTS {esquema}")
        for arq in sorted(pasta.glob("*.parquet")):
            con.execute(f'CREATE OR REPLACE VIEW {esquema}."{arq.stem}" AS SELECT * FROM read_parquet(\'{arq}\')')
    con.execute("CREATE SCHEMA IF NOT EXISTS ref")
    con.execute(f"""CREATE OR REPLACE VIEW ref.traducoes AS
                    SELECT * FROM read_csv('{REFERENCIAS / "traducoes.csv"}', header = true, all_varchar = true)""")
    return con


def gravar(con, consulta, destino, parametros=None):
    """Grava o resultado de uma consulta em Parquet e devolve (linhas, colunas)."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    con.execute(f"COPY ({consulta}) TO '{destino}' (FORMAT parquet, COMPRESSION snappy)", parametros)
    linhas = con.execute(f"SELECT count(*) FROM read_parquet('{destino}')").fetchone()[0]
    colunas = len(con.execute(f"DESCRIBE SELECT * FROM read_parquet('{destino}')").fetchall())
    return linhas, colunas


def baixar_origem():
    if all((ORIGEM / f"{nome}.csv").exists() for nome in ARQUIVOS):
        return
    ORIGEM.mkdir(parents=True, exist_ok=True)
    print(f"  baixando o OULAD de {URL_OULAD}")
    with urllib.request.urlopen(URL_OULAD) as resposta:
        zipfile.ZipFile(io.BytesIO(resposta.read())).extractall(ORIGEM)


def carregar_bruto(linhagem):
    """Camada 1: cada CSV vira um Parquet idêntico. Nada é interpretado aqui."""
    baixar_origem()
    con = duckdb.connect()
    for arquivo, tabela in ARQUIVOS.items():
        consulta = f"SELECT * FROM read_csv('{ORIGEM / (arquivo + '.csv')}', header = true, all_varchar = true)"
        linhas, colunas = gravar(con, consulta, BRUTO / f"{tabela}.parquet")
        linhagem.append(("1. Bruto", tabela, f"{arquivo}.csv", linhas, colunas, DESCRICOES["bruto"]))
        print(f"  bruto.{tabela}: {linhas:,} linhas")


def construir(camada, pasta_sql, destino, rotulo, linhagem):
    """Camadas 2 e 3: executa, em ordem alfabética, cada arquivo .sql da pasta."""
    for arq in sorted((SQL / pasta_sql).glob("*.sql")):
        con = conectar()
        texto = arq.read_text(encoding="utf-8")
        comentario = " ".join(l.lstrip("- ").strip() for l in texto.splitlines() if l.startswith("--"))
        linhas, colunas = gravar(con, texto, destino / f"{arq.stem}.parquet")
        linhagem.append((rotulo, arq.stem, f"sql/{pasta_sql}/{arq.name}", linhas, colunas,
                         comentario.split(". ")[0].rstrip(".") or DESCRICOES[camada]))
        print(f"  {camada}.{arq.stem}: {linhas:,} linhas")
