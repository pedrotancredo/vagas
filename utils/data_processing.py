import random
import numpy as np
import pandas as pd
import geopandas as gpd
import streamlit as st
from utils.utils import gera_nome_escola
from utils.utils import generate_random_points_in_polygon
from utils.utils import pessoa_random


@st.cache_data
def gerar_alunos(_polygon, num_alunos, num_seed, bairro_indice):
    num_seed += 1
    alunos = generate_random_points_in_polygon(_polygon, num_alunos, num_seed)

    gdf_alunos = gpd.GeoDataFrame(geometry=alunos, crs=29193)  # type: ignore
    gdf_alunos['escola'] = int(0)

    ## TODO BOTA NOME NOME NO ALUNO!!! ##
    nome_alunos = set()
    # name_seed = num_seed
    while len(nome_alunos) < num_alunos:
        nome_alunos.add(pessoa_random().nome)
        # name_seed += 1
    gdf_alunos['nome_aluno'] = list(nome_alunos)

    # Display the points
    # st.sidebar.write(f"{len(alunos)} alunos gerados")

    return gdf_alunos

def gera_vagas(num_vagas, num_seed):
    random.seed(num_seed)
    return random.randint(num_vagas[0], num_vagas[1])

@st.cache_data
def gerar_escolas(_polygon, num_escolas, num_vagas, num_seed, bairro_indice):
    np.random.seed(num_seed)

    escolas = generate_random_points_in_polygon(
        _polygon, num_escolas, num_seed)

    gdf_escolas = gpd.GeoDataFrame(geometry=escolas, crs=29193)  # type: ignore
    # gdf_escolas['vagas'] = gdf_escolas.apply(gera_vagas, args=(num_vagas,num_seed), axis=1)
    for index, row in gdf_escolas.iterrows():
        gdf_escolas.at[index, 'vagas'] = gera_vagas(num_vagas, num_seed)
        num_seed += 1


    nome_escolas = set()
    name_seed = num_seed
    while len(nome_escolas) < num_escolas:
        nome_escolas.add(gera_nome_escola(seed=name_seed))
        name_seed += 1

    gdf_escolas['nome_escola'] = list(nome_escolas)

    return gdf_escolas


from shapely.geometry import Point
import pandas as pd

def calcular_matriz_distancias(df1, df2):
    pontos_df1 = [Point(row['longitude'], row['latitude']) for _, row in df1.iterrows()]
    pontos_df2 = [Point(row['longitude'], row['latitude']) for _, row in df2.iterrows()]

    matriz_distancias = [[ponto_df1.distance(ponto_df2) for ponto_df2 in pontos_df2] for ponto_df1 in pontos_df1]

    return matriz_distancias
