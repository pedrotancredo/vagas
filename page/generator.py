import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
from utils.data_processing import gerar_alunos, gerar_escolas
from utils.model import calcula_matriz_distancias
from utils.model import aloca_alunos
from utils.visualization import plotmap #, ag_grid


def show():
    '''Mostra as páginas'''

    # from plot import plotmap
    # from table import draw_table

    def func_gera_dados():
        st.session_state['dados'] = True
        return

    if 'dados' not in st.session_state:
        st.session_state['dados'] = False

    if 'polygon' not in st.session_state:
        bairros = r'./recursos/bairros/bairros_rj.shp'
        gdf_bairros = gpd.read_file(bairros).sort_values(
            by='nome', ascending=True)
        polygon = gdf_bairros['geometry'][0]
        st.session_state['polygon'] = polygon
        st.session_state['gdf_bairros'] = gdf_bairros

    # st.write(st.session_state['gdf_bairros'])
    gdf_bairros = st.session_state['gdf_bairros']
    polygon = st.session_state['polygon']

    ##############################################
    ################ INTERFACE ###################
    ##############################################

    st.markdown("## Gerador de Dados Aleatórios")

    st.markdown('''<div style="text-align: justify;"><p>O gerador de dados utilizado
    para alimentar o modelo de alocação de alunos em escolas funciona da seguinte
    maneira:</p></div>''', unsafe_allow_html=True)

    st.markdown('''<div style="text-align: justify;"><li>Primeiramente, é necessário
    especificar o <b>bairro</b> em que será realizada a alocação dos alunos.
    Isso permite restringir o escopo do problema, focando em uma área geográfica
    específica.</li>
    <li>A <b>semente</b> do gerador de números é outro parâmetro de entrada importante.
    Essa semente é utilizada para inicializar o gerador de números aleatórios,
    garantindo que os dados gerados sejam reproduzíveis. Ao fornecer a mesma
    semente em diferentes execuções, é possível obter conjuntos de dados consistentes
    e comparar diferentes soluções.</li>
    <li>O <b>número de alunos</b> é o parâmetro que define a quantidade de estudantes
    a serem alocados. Esse valor determina o tamanho do vetor de alunos a ser gerado,
    onde cada componente representa um aluno específico.</li>
    <li>As <b>vagas por escola</b> é um parâmetro que define a capacidade máxima
    de cada instituição de ensino. Essa informação é utilizada para definir o vetor
    de restrições de vagas, em que cada componente indica o número máximo de alunos
    que podem ser alocados em determinada escola.</li>
    <li>Por fim, o <b>número de escolas</b> é o parâmetro que determina a quantidade
    de instituições de ensino disponíveis para a alocação. Esse valor é utilizado
    para definir o vetor de escolas, onde cada componente representa uma escola
    específica.</li>
    <p>Com base nesses parâmetros de entrada, o gerador de dados utiliza o gerador
    de números aleatórios para criar conjuntos de dados aleatórios e representativos.
    Esses conjuntos de dados incluem as informações dos alunos, das escolas e das
    restrições de vagas, permitindo a realização de testes e simulações do modelo
    de alocação.</p></div>''',
                unsafe_allow_html=True)

    ##############################################
    ################ GEOMETRIA ###################
    ##############################################
    #  Sidebar

    with st.expander("Gerador de Dados", expanded=True):

        with st.form(key="form_dados"):
            st.selectbox('Bairro',
                         options=st.session_state['gdf_bairros']['nome'].unique(
                         ),
                         key='nome_bairro', index=113)
            col1, col2 = st.columns(2)
            col1.slider("Semente", min_value=0,
                        max_value=100, step=1, value=25, key='num_seed')
            col2.slider("Vagas por Escola",
                        min_value=0, max_value=20, step=1, value=[5, 20], key='num_vagas')
            col1.slider("Número de Alunos", min_value=1,
                        max_value=250, step=1, value=50, key='num_alunos')
            col2.slider("Número de Escolas",
                        min_value=1, max_value=20, step=1, value=4, key='num_escolas')

            st.form_submit_button(
                'Confirmar', on_click=func_gera_dados)

        # with st.sidebar.expander("Alocar Alunos", expanded=False):
            # define_alocacao = st.button('Alocar Alunos')

    if st.session_state['dados']:

        num_alunos = st.session_state['num_alunos']
        num_seed = st.session_state['num_seed']
        num_escolas = st.session_state['num_escolas']
        num_vagas = st.session_state['num_vagas']
        nome_bairro = st.session_state['nome_bairro']
        gdf_bairros = st.session_state['gdf_bairros']
        bairro_indice = int(
            (gdf_bairros.loc[gdf_bairros['nome'] == nome_bairro]['geometry'].index).to_list()[0])
        polygon = gdf_bairros['geometry'][bairro_indice]

        # polygon = gdf_bairros['geometry'][0]
        gdf_alunos = gerar_alunos(polygon, num_alunos, num_seed, bairro_indice)
        gdf_escolas = gerar_escolas(
            polygon, num_escolas, num_vagas, num_seed, bairro_indice)
        df_alocacao = aloca_alunos(
            gdf_alunos, gdf_escolas, num_seed, bairro_indice)
        
        st.session_state['gdf_alunos'] = gdf_alunos 
        st.session_state['gdf_escolas'] = gdf_escolas
        st.session_state['df_alocacao'] = df_alocacao

        r = plotmap(gdf_alunos, gdf_escolas, df_alocacao)
        st.pydeck_chart(r, use_container_width=True)

    #  DADOS #
    #  https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb

        # st.markdown('## Escolas:')

        # escolas = pd.DataFrame(
        #     gdf_escolas[["nome_escola", "vagas"]]).reset_index()

        # alunos = pd.DataFrame(gdf_alunos[["nome_aluno", "escola"]])

        # data = pd.merge(left=alunos, right=escolas, how='inner',
        #                 left_on='escola', right_on='index')

        distancias = calcula_matriz_distancias(gdf_alunos, gdf_escolas)
        st.session_state['distancias'] = distancias
        vetor = gdf_alunos['escola']

        n = len(vetor)
        m = len(gdf_escolas)
        matriz_pivotada = np.zeros((n, m))
        for i, valor in enumerate(vetor):
            matriz_pivotada[i, valor] = 1

        df_matriz = pd.DataFrame(matriz_pivotada)
        df_matriz.astype(int)

        st.session_state['df_matriz'] = df_matriz

        a = np.array(df_matriz)
        b = np.array(distancias)
        c = len(gdf_alunos)
        objetivo = np.sum(np.multiply(a,b))/c
        st.metric(label='Distância Média', value=f'{objetivo:.2f} m')

        st.markdown('## Download das informações geradas:')
        col1, col2 = st.columns([.5, 1])

        col1, col2 = st.columns([1, 1])
        col1.markdown('Matriz solução candidata inicial')

        col1.download_button(label="Baixar solução candidata",
                             data=df_matriz.reset_index().to_csv(
                                 sep='|', decimal=',',
                                 index=False).encode('utf-8'),
                             file_name='candidata.csv',
                             mime='text/csv')
        # st.write(vetor)
        col1.write(df_matriz)

        col2.markdown('Matriz distâncias aluno x escola ')
        col2.download_button(label="Baixar matriz de distâncias",
                             data=pd.DataFrame(distancias).reset_index().to_csv(
                                 sep='|', decimal=',',
                                 index=False).encode('utf-8'),
                             file_name='distancias.csv',
                             mime='text/csv')
        col2.write(pd.DataFrame(distancias))

        st.write('Vetor restrições de vagas por escola:')

        vagas = pd.DataFrame(gdf_escolas.drop(columns='geometry').reset_index())[["vagas"]]
        st.download_button(label="Baixar restrição de vagas",
                           data=vagas.to_csv(
                               sep='|', decimal=',',
                               index=False).encode('utf-8'),
                           file_name='vagas.csv',
                           mime='text/csv')

        st.write(vagas)
