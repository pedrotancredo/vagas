""" Componente da Tabela """
import pydeck as pdk
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode


def ag_grid(data):
    """ Desenha Tabela """

    grid_builder = GridOptionsBuilder.from_dataframe(data)
    # grid_builder.configure_pagination(
        # paginationAutoPageSize=True)  # Add pagination
    grid_builder.configure_side_bar()  # Add a sidebar
    # grid_builder.configure_selection(
        # 'multiple', use_checkbox=True, groupSelectsChildren=True)  # Enable multi-row selection

    grid_builder.configure_column(
        field="nome_escola",

        header_name="Nome da Escola",
        # header_name="Power Plant",
        # flex=1,
        # tooltipField="powerPlant",
        # rowGroup=True,
        enableRowGroup = True,
        # hide = True,
    )
    grid_options = grid_builder.build()

    table = AgGrid(data,
                   gridOptions=grid_options,
                   data_return_mode=DataReturnMode.AS_INPUT,
                   update_mode=GridUpdateMode.MODEL_CHANGED,
                   fit_columns_on_grid_load=False,
                #    theme='streamlit',  # Add theme color to the table
                   rowbuffer=200,
                   enable_enterprise_modules=True,
                   height=350,
                   width='100%',
                   reload_data=True,
                   scrollbar_style='simple')
    return table

# https://www.ag-grid.com/javascript-data-grid/grouping-single-group-column/#example-enabling-single-group-column
def plotmap(gdf_alunos, gdf_escolas, df_alocacao):
    """Plota o mapa"""
    aluno_layer = pdk.Layer(
        "ScatterplotLayer",
        data=gdf_alunos.to_crs(4326),
        get_position="geometry.coordinates",
        get_color=[0, 255, 0, 100],
        get_radius=3,
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=6,
        radius_min_pixels=1,
        radius_max_pixels=100,
        line_width_min_pixels=1,
        get_fill_color=[255, 140, 0],
        get_line_color=[0, 0, 0],

    )

    escola_layer = pdk.Layer(
        "ScatterplotLayer",
        # greatCircle = True,
        data=gdf_escolas.to_crs(4326),
        get_position="geometry.coordinates",
        get_color=[0, 255, 0, 100],
        get_radius='[vagas]',
        pickable=True,
        opacity=0.5,
        stroked=True,
        filled=True,
        radius_scale=1,
        radius_min_pixels=5,
        radius_max_pixels=25,
        line_width_min_pixels=1,
        get_fill_color=[0, 140, 255],
        get_line_color=[0, 0, 0],
    )

    layer_arc = pdk.Layer(
        'ArcLayer',
        data=df_alocacao,
        get_width=2,
        opacity=0.5,
        get_source_position='[start_x, start_y]',
        get_target_position='[end_x, end_y]',
        get_source_color=[255, 90, 0],
        get_target_color=[0, 128, 200],
        get_tilt=15,
        pickable=True,
        auto_highlight=True,
        cluster_arc=True,
        get_cluster_radius=1,
        get_cluster=True,
    )
    # Create a PyDeck map and add both layers to it
    # view_state = pdk.ViewState(latitude=-22.8025, longitude=-43.1863, zoom=10)
    lon = gdf_alunos['geometry'].unary_union.centroid.coords[0][0]
    lat = gdf_alunos['geometry'].unary_union.centroid.coords[0][1]
    # bbox = gdf_alunos.total_bounds
    # width = bbox[2] - bbox[0]
    # height = bbox[3] - bbox[1]
    view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=14.5,pitch=70)

    return pdk.Deck(map_style=None,layers=[aluno_layer, escola_layer, layer_arc], initial_view_state=view_state) # type: ignore
