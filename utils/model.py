import numpy as np
import pandas as pd
# import geopandas as gpd
# import streamlit as st


def calcula_matriz_distancias(df1, df2):
    pontos_df1 = df1.to_crs(31983)['geometry']
    pontos_df2 = df2.to_crs(31983)['geometry']

    matriz_distancias = []

    for ponto_df1 in pontos_df1:
        linha_distancias = []
        for ponto_df2 in pontos_df2:
            distancia = ponto_df1.distance(ponto_df2)
            linha_distancias.append(distancia)
        matriz_distancias.append(linha_distancias)

    return matriz_distancias


def aloca_alunos(gdf_alunos, gdf_escolas, seed, bairro_indice):

    # gdf_alunos = gpd.GeoDataFrame(gdf_alunos)
    # gdf_escolas = gpd.GeoDataFrame(gdf_escolas)
    # gdf_alunos.crs = 4326
    # gdf_escolas.crs = 4326

    np.random.seed(seed)

    gdf_alunos['geometry'] = gdf_alunos.to_crs(4326).geometry.values
    gdf_escolas['geometry'] = gdf_escolas.to_crs(4326).geometry.values
    alocacao_list = []
    vagas = list(gdf_escolas['vagas'])

    for index, row in gdf_alunos.iterrows():
        start_x = row['geometry'].coords[0][0]
        start_y = row['geometry'].coords[0][1]

        escola_disponível = False

        while (not escola_disponível) and (sum(vagas) > 0):
            escola_index = np.random.randint(0, len(gdf_escolas))
            if vagas[escola_index] >= 1:
                end_x = gdf_escolas.iloc[escola_index]['geometry'].coords[0][0]
                end_y = gdf_escolas.iloc[escola_index]['geometry'].coords[0][1]
                vagas[escola_index] = vagas[escola_index] - 1
                gdf_alunos.at[index, 'escola'] = escola_index
                escola_disponível = True
                alocacao_list.append([start_x, start_y, end_x, end_y])

    df_alocacao = pd.DataFrame(alocacao_list, columns=[
        'start_x', 'start_y', 'end_x', 'end_y'])

    return df_alocacao

def aplica_alocacao(gdf_alunos, gdf_escolas, dataframe, bairro_indice):

    df_melted = dataframe.melt(
    id_vars=['index'], var_name='escola', value_name='valor')
    df_melted = df_melted[df_melted['valor'] == 1][['index','escola']].rename(columns={'index' : 'aluno'}).set_index('aluno').sort_index()

    alocacao_list = []
    for index, row in gdf_alunos.iterrows():
        start_x = row['geometry'].coords[0][0]
        start_y = row['geometry'].coords[0][1]
        escola_index = int(df_melted.loc[index]['escola'])
        # st.write(escola_index)
        end_x = gdf_escolas.iloc[escola_index]['geometry'].coords[0][0]
        end_y = gdf_escolas.iloc[escola_index]['geometry'].coords[0][1]
        alocacao_list.append([start_x, start_y, end_x, end_y])

    df_nova_alocacao = pd.DataFrame(alocacao_list, columns=['start_x', 'start_y', 'end_x', 'end_y'])

    return df_nova_alocacao