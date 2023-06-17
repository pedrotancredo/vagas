"""
    Este programa minimiza a distância média entre alunos e escolas levando-se em consideração a
    localização de ambos e a quantidade de vagas disponíveis.

    O programa é organizado em módulos, a saber:

    - main.py:
    Ponto de entrada do programa. Importa funções necessárias de outros arquivos.

    - utils.py:
    Armazena funções auxiliares usadas em várias partes do seu programa.
    Contem funções como get_data() (obter dados), clean_data() (limpar dados) e outras funções
    utilitárias não seja específicas de um módulo em particular.

    - data_processing.py:
    Armazena as funções relacionadas ao processamento de dados.
    Contem funções como preprocess_data(), analyze_data() e outras funções de manipulação ou
    análise de dados.

    - model.py:
    Armazena as funções relacionadas a aprendizado de máquina.
    Contem funçães como model_data() (treinar modelo) e outras funções para treinamento, avaliação
    ou qualquer outra operação específica em modelos.

    - visualization.py:
    Armazena funções relacionadas à visualização de dados ou plotagem.
    Contem funções para criar vários gráficos, diagramas ou representações visuais de dados.

    - streamlit_app.py:
    Armazena as funçães relacionadas à interface do usuário.
    Neste arquivo, está a definição do código da aplicação Streamlit.
    Contem código de definição do layout, componentes de interface do usuário e interações.
    """

# https://towardsdatascience.com/understanding-python-imports-init-py-and-pythonpath-once-and-for-all-4c5249ab6355

import streamlit as st
from streamlit_lottie import st_lottie
# from streamlit_lottie import st_lottie_spinner

import os
import sys
import page
import requests
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

MAIN_PATH = os.path.normpath(__file__)
sys.path.append(os.path.dirname(MAIN_PATH))

@st.cache_data()
def load_lottieurl(url: str):
    r = requests.get(url,timeout=30)
    if r.status_code != 200:
        return None
    return r.json()
# https://lottiefiles.com/mograph
lootie_list = ['https://assets1.lottiefiles.com/packages/lf20_nonpuabv.json',
               'https://assets8.lottiefiles.com/packages/lf20_awP420Zf8l.json',
               'https://assets8.lottiefiles.com/private_files/lf30_TBKozE.json',
               'https://assets2.lottiefiles.com/packages/lf20_x0ysvaqt.json',
               'https://assets10.lottiefiles.com/datafiles/MaKSoctsyXXTCDOpDktJYEcS3ws5SI6CLDo7iyMc/ex-splash.json',
               'https://assets9.lottiefiles.com/packages/lf20_D8Mw4zIZPL.json',]


lootie = load_lottieurl(lootie_list[4])
st_lottie(lootie, key='intro')
st.markdown("# Otimização da alocação estudantil")
st.markdown("Modelo para otimização de alocação de alunos em escolas com base \
                na minimização da distância média entre aluno e escola.")


tabs = st.tabs(["🎯Objetivo", "🎨Gerador de Dados", "🌍Resultado"])

with tabs[0]:
    page.intro.show()

with tabs[1]:
    page.generator.show()

with tabs[2]:
    page.model.show()