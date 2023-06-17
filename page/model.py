import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
from utils.visualization import plotmap, ag_grid
from utils.model import aplica_alocacao


def show():
    '''Mostra página de modelo de dados'''
    st.markdown('## Validação da solução')
    st.markdown('''<div style="text-align: justify;"><p>Devido à falta de tempo
    e à aproximação do prazo de entrega, a equipe enfrentou dificuldades para
    elaborar uma solução completa utilizando Python. A resolução de problemas de
    otimização envolve uma série de etapas, desde a modelagem matemática até a
    implementação do algoritmo de busca. Essas etapas demandam tempo para
    desenvolvimento, testes e ajustes. Além disso, a equipe precisaria lidar
    com questões como a criação de estruturas de dados adequadas, a implementação
    das restrições de vagas nas escolas e a definição da função objetivo de
    minimização da distância média.</p>
    <p>Diante desses desafios e da necessidade de cumprir o prazo estabelecido,
    a equipe optou por utilizar o solver do Excel. O Excel oferece uma interface
    amigável e ferramentas de otimização embutidas que podem simplificar o
    processo de resolução de problemas como o de alocação de alunos em escolas.
    O solver do Excel permite definir as variáveis de decisão, as restrições e a
    função objetivo de forma intuitiva, e realiza automaticamente o cálculo da
    solução ótima. Embora essa abordagem possa ter algumas limitações em termos
    de flexibilidade e escalabilidade, ela oferece uma solução viável e eficiente
    dentro do prazo estabelecido.</p>
    <p>Além disso, é importante ressaltar que o resultado obtido pelo solver do
    Excel pode ser facilmente importado e visualizado através de uma interface
    intuitiva. O Excel permite a criação de planilhas personalizadas, nas quais
    é possível organizar os dados de forma clara e apresentar os resultados de
    maneira visualmente atraente. Gráficos, tabelas e outras ferramentas de
    visualização podem ser utilizados para apresentar a distribuição ótima dos
    alunos nas escolas, destacando a minimização da distância média e atendendo
    aos critérios de capacidade das instituições de ensino. Essa interface amigável
    facilita a compreensão dos resultados por parte dos usuários, permitindo uma
    análise mais detalhada e a tomada de decisões com base nas soluções obtidas.
    Dessa forma, o uso do solver do Excel proporciona uma abordagem prática e
    eficaz para resolver o problema de alocação de alunos em escolas, atendendo
     às restrições de tempo e fornecendo resultados de maneira clara e acessível.
     </p></div>''',
                unsafe_allow_html=True)

    # st.file_uploader('Arquivo de modelo de dados', type=['xlsx'])
    if st.session_state['dados']:
        uploaded_file = st.file_uploader(label="__Carregue aqui o arquivo de solução:__", type=["csv"])
        if uploaded_file is not None:
            # To read file as bytes:
            # bytes_data = uploaded_file.getvalue()
            # st.write(bytes_data)
            # To convert to a string based IO:
            # stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            # st.write(stringio)
            # To read file as string:
            # string_data = stringio.read()
            # st.write(string_data)
            # Can be used wherever a "file-like" object is accepted:
            nova_alocacao = pd.read_csv(uploaded_file, sep=';')
            # st.write(nova_alocacao)

            gdf_alunos = st.session_state['gdf_alunos']
            gdf_escolas = st.session_state['gdf_escolas']
            df_alocacao = st.session_state['df_alocacao']
            df_matriz = st.session_state['df_matriz']
            distancias = st.session_state['distancias']
            bairro_indice = 1

            # st.write(nova_alocacao.set_index('index'))
            # st.write(gdf_alunos)
            # st.write( gdf_escolas)
            r = plotmap(gdf_alunos, gdf_escolas, df_alocacao)
            st.pydeck_chart(r, use_container_width=True)
            a0 = np.array(df_matriz)
            a1 = np.array(nova_alocacao.set_index('index'))
            b = np.array(distancias)
            c = len(gdf_alunos)
            original = np.sum(np.multiply(a0,b))/c
            novo = np.sum(np.multiply(a1,b))/c
            # delta = novo - original
            delta_pct = (novo - original)/original*100

            st.metric(label='Distância Média Original', value=f'{original:.2f} m')

            df_teste = aplica_alocacao(gdf_alunos, gdf_escolas, nova_alocacao, bairro_indice)

            r = plotmap(gdf_alunos, gdf_escolas, df_teste)
            st.pydeck_chart(r, use_container_width=True)
            st.metric(label='Distância Média Nova', value=f'{novo:.2f} m',delta=f'{delta_pct:.2f} %', delta_color='inverse')
            # st.markdown('# 😜😍🎉🌹🎉🌹')



    else:
        st.error('Necessário gerar dados para análise antes de carregar a solução')