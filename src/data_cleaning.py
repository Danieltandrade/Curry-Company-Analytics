"""
Docstring para dataframe.data_manipulation

Função para manipulação de DataFrames utilizando Pandas.
"""

# Importando Bibliotecas
import os
import pandas as pd
import streamlit as st
import logging


# Inicializa o logger
logger = logging.getLogger(__name__)

@st.cache_data
def df_cleaning(path: str, df_clean: bool = True) -> pd.DataFrame | None:
    """
    Função para carregar e limpar um DataFrame a partir de um arquivo CSV.
    Limpeza inclui remoção de nulos, ajuste de tipos de dados, remoção de espaços em branco,
    e tratamento específico de colunas.

    Args:
        path (str): Caminho para o arquivo CSV.
        df_clean (bool): Se True, aplica a limpeza no DataFrame. Se False, retorna o DataFrame bruto.
    Returns:
        pd.DataFrame: DataFrame limpo ou bruto dependendo do parâmetro df_clean.
    Raises:
        FileNotFoundError: Se o arquivo no caminho especificado não for encontrado.
    
    Exemplo de uso:
        df_cleaned = df_cleaning('path', df_clean=True)
    """
    
    # 1. Verificação de segurança
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    try:
        # O Pandas vai ler "NaN " (com espaço) e "conditions NaN" automaticamente como dados nulos.
        na_formats = ["NaN ", "NaN", "conditions NaN"]
        df = pd.read_csv(path, na_values=na_formats)

        if not df_clean:
            return df

        # --- INÍCIO DA LIMPEZA ---
        
        # 1. Remoção de Nulos (Substitui as 7 linhas de filtros manuais)
        # Removemos linhas onde qualquer coluna essencial tenha virado NaN na leitura
        df.dropna(inplace=True)

        # 2. Limpeza de Espaços em Branco (Strip) em massa
        # Seleciona apenas colunas do tipo 'object' (texto) e remove espaços das pontas
        cols_texto = df.select_dtypes(include=['object']).columns
        df[cols_texto] = df[cols_texto].apply(lambda x: x.str.strip())

        # 3. Ajuste de Tipos Numéricos
        # Usamos o dicionário para organizar a conversão
        df = df.astype({
            'Delivery_person_Age': int,
            'multiple_deliveries': int,
            'Delivery_person_Ratings': float
        })

        # 5. Tratamento de Datas
        df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%d-%m-%Y')
        df['Week_of_Year'] = df['Order_Date'].dt.isocalendar().week

        # 6. Limpeza Específica (Regex e Replace)
        
        # Remove '(min) ' e converte para int
        # Regex: pega apenas os dígitos (\d+)
        df['Time_taken(min)'] = df['Time_taken(min)'].astype(str).str.extract(r'(\d+)').astype(int)

        # Remove a palavra 'conditions ' de qualquer clima (mais genérico que o dicionário)
        df['Weatherconditions'] = df['Weatherconditions'].str.replace('conditions ', '', regex=False)
        
        # Resetar o index após a remoção de linhas é boa prática
        df.reset_index(drop=True, inplace=True)

        return df

    except FileNotFoundError:
        # Erro específico: Arquivo não existe
        logger.error(f"Arquivo não encontrado no caminho: {path}")
        return None  # Retornar None é muitas vezes melhor que DF vazio (explico abaixo)

    except pd.errors.EmptyDataError:
        # Erro específico: O arquivo csv está vazio
        logger.error("O arquivo CSV está vazio.")
        return None

    except KeyError as e:
        # Erro específico: Mudaram o nome de uma coluna no CSV original
        logger.error(f"Coluna obrigatória não encontrada no CSV: {e}")
        return None

    except Exception as e:
        # O "Pega-Tudo" fica apenas para o imprevisto real
        logger.error(f"Erro inesperado: {e}", exc_info=True)
        return None
