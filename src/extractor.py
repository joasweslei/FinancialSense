import pandas as pd
import requests
from datetime import date


def fetch_sgs_data(serie_id):
    """
    Filtro 1: Extração de dados do Sistema de Gerenciamento de Séries Temporais do BC.
    """
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie_id}/dados?formato=json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        dados_res = response.json()

        df = pd.DataFrame(response.json())
        print(f"Dados retornados da Série {serie_id}")
        return df
    except Exception as e:
        print(f"Erro na extração da série {serie_id}: {e}")
        return None

def fetch_sgs_data_by_date(serie_id, start_date):
    # Parâmetros
    data_final = date.today()
    
    # Formatar datas no padrão dd/mm/aaaa
    params = {
        "formato": "json",
        "dataInicial": start_date.strftime("%d/%m/%Y"),
        "dataFinal": data_final.strftime("%d/%m/%Y"),
    }

    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie_id}/dados"

    response = requests.get(url, params=params)
    response.raise_for_status()  # Lança exceção se houver erro HTTP

    dados = response.json()
    df = pd.DataFrame(dados)
    print(f"Dados retornados da Série {serie_id}")
    return df

def get_economic_events():
    """
    Retorna um DataFrame com eventos econômicos, por exemplo, Liberação do FGTS
    """
    eventos = [
        {"data": "2017-03-01", "evento": "Início Saques FGTS Inativo"},
        {"data": "2017-07-01", "evento": "Fim Saques FGTS Inativo"},
        {"data": "2020-04-01", "evento": "Auxílio Emergencial / Pandemia"},
        {"data": "2022-04-01", "evento": "Saque Extraordinário FGTS"}
    ]
    df_eventos = pd.DataFrame(eventos)
    df_eventos['data'] = pd.to_datetime(df_eventos['data'])
    return df_eventos


