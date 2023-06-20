import streamlit as st


def show():

    st.markdown("## Introdução")
    st.markdown("""<div style="text-align: justify;"><p>A otimização por algoritmos
    genéticos é uma abordagem eficiente para resolver problemas complexos e
    encontrar soluções ótimas. Inspirada no processo evolutivo natural, essa técnica
    utiliza conceitos como seleção, reprodução e mutação para buscar soluções cada
    vez melhores ao longo de várias gerações. No início, uma população de soluções
    candidatas é criada aleatoriamente. Em seguida, as soluções são avaliadas de
    acordo com uma função objetivo e as melhores são selecionadas para reprodução.
    Durante este processo, ocorre a combinação das características das soluções
    selecionadas e a introdução de pequenas alterações (mutações). Esse ciclo de
    seleção, reprodução e mutação é repetido várias vezes até que uma solução
    satisfatória seja encontrada.</p>
    <p>Os algoritmos genéticos têm a capacidade de explorar um espaço de soluções
    vasto e complexo, permitindo a busca de soluções ótimas em problemas de alta
    dimensionalidade e com múltiplas variáveis. Além disso, eles possuem uma abordagem
    heurística, o que significa que não garantem a solução globalmente ótima, mas
    geralmente fornecem soluções de alta qualidade em tempo razoável. Essa
    flexibilidade torna os algoritmos genéticos aplicáveis em uma ampla variedade
    de áreas, como engenharia, ciência da computação, economia e biologia,
    onde problemas de otimização são frequentes e complexos. Além disso, eles
    podem ser adaptados e combinados com outras técnicas de otimização para melhorar
    ainda mais o desempenho e a eficiência na busca de soluções. Em resumo, os
    algoritmos genéticos são uma poderosa ferramenta para otimização, proporcionando
    uma abordagem única e eficaz para resolver problemas complexos.</p></div>""",
                unsafe_allow_html=True)

    st.markdown("## Descrição do problema")
    st.markdown("""<div style="text-align: justify;"><p>Quando tratamos da alocação 
    de alunos em escolas, um desafio importante é encontrar a melhor distribuição 
    de estudantes levando em consideração não apenas a capacidade das instituições
    de ensino, mas também a distância entre a casa dos alunos e as escolas.
    A proximidade geográfica é uma preocupação frequente dos pais ao inserir suas
    crianças na educação básica.</p>
    <p>Nesse contexto, surge a necessidade de buscar uma alocação ótima de crianças
    na rede pública de ensino, com o objetivo de minimizar a distância entre a
    casa de cada aluno e a escola a qual será alocado. A ideia é encontrar uma
    solução que garanta o acesso mais conveniente e eficiente possível.</p>
    <p>Esse problema de otimização requer a utilização de métodos e técnicas que
    permitam calcular as distâncias entre a casa de cada aluno e todas as escolas
    disponíveis. A partir dessas informações, é possível buscar a alocação que
    minimize a média total das distâncias, proporcionando uma distribuição mais
    adequada.</p></div>""",
                unsafe_allow_html=True)
    st.markdown("### Premissas")
    st.markdown('''
    - Para reduzir o volume de informações processados, consideramos inicialmente
    a alocação dos alunos para um único bairro.
    - Para o cálculo da distância entre o aluno e a escola, será utilizada a
    distância linear, ou seja, sem levar em consideração a distância rodoviária.
    - Todos os dados utilizados para alocação consistirão de informações geradas
    aleatoriamente uma vez que as informações reais são protegidas pela LGPD.
    ''')
    st.markdown("### Modelagem")

    st.markdown('''<div style="text-align: justify;"><p>Nesse contexto, a modelagem
    do problema pode ser realizada utilizando vetores e matrizes. Primeiramente,
    utilizamos um vetor <b>a</b> para representar os alunos, no qual cada componente
    corresponde a um aluno específico. Conforme:</p></div>''',
                unsafe_allow_html=True)

    st.latex(
        r'''\mathbf{a} = \begin{bmatrix} a_1 \\ a_2 \\ \vdots \\ a_m \end{bmatrix}''')

    st.markdown('''<div style="text-align: justify;"><p>Da mesma forma, é utilizado
    um vetor <b>e</b> para representar as escolas, onde cada componente representa
    uma instituição de ensino. Conforme:</p></div>''',
                unsafe_allow_html=True)

    st.latex(
        r'''\mathbf{e} = \begin{bmatrix} e_1 \\ e_2 \\ \vdots \\ e_n \end{bmatrix}''')

    st.markdown('''<div style="text-align: justify;"><p>Complementarmente, é
    necessário considerar as restrições de vagas em cada escola. Para isso,
    utilizamos outro vetor <b>v</b> representando as restrições de vagas para
    cada escola, em que cada componente indica o número máximo de alunos que
    podem ser alocados em determinada instituição. Conforme:</p></div>''',
                unsafe_allow_html=True)

    st.latex(
        r'''\mathbf{v} = \begin{bmatrix} v_1 \\ v_2 \\ \vdots \\ v_n \end{bmatrix}''')

    st.markdown('''<div style="text-align: justify;"><p>Por fim, além dos vetores,
    utilizaremos a função de custo <b>distância</b> para calcular a distância
    entre cada aluno e cada escola. Sendo:</p></div>''',
                unsafe_allow_html=True)

    st.latex(r'''d_{ij} = \text{distância}(a_i, e_j)''')

    st.markdown('''<div style="text-align: justify;"><p>Utilizaremos também, uma
    matriz de distâncias obtida através do uso da função <b>distância</b> onde
    cada elemento da matriz representa o cálculo da distância entre um aluno específico
    e uma escola específica. Conforme:</p></div>''',
                unsafe_allow_html=True)

    st.latex(r'''\mathbf{D} = \begin{bmatrix}
    D_{11} & D_{12} & \ldots & D_{1n} \\
    D_{21} & D_{22} & \ldots & D_{2n} \\
    \vdots & \vdots & \ddots & \vdots \\
    D_{m1} & D_{m2} & \ldots & D_{mn}
    \end{bmatrix}
    ''')

    st.markdown('''<div style="text-align: justify;"><p>Para determinação da
    alocação dos alunos escolhemos uma matriz <b>P</b> para representar a
    distribuição. Nesta matriz as linhas representam os alunos e as colunas
    representam as escolas. Cada linha possui valor 1 na escola em que o aluno
    específico está alocado e 0 em todas as outras colunas. De tal maneira que
    a soma dos elementos de cada linha deve sempre ser 1.''',
                unsafe_allow_html=True)

    st.markdown('''<div style="text-align: justify;"><p> Por tanto, a <b>função
    objetivo</b> pode ser definida como a distância média de cada aluno em sua
    escola de alocação. E pode ser escrita como o produto interno de Frobenius
    das matrizes <b>P</b> e <b>D</b> dividido pela quantidade <b>m</b> de
    alunos:</p></div >''',
                unsafe_allow_html=True)

    st.latex(r'''\frac{\langle \mathbf{P}, \mathbf{D} \rangle_{F}}{m} = \sum_{i=1}^{m} 
             \sum_{j=1}^{n}\frac{P_{ij} \cdot D_{ij}}{m}''')

    st.markdown('''<div style="text-align: justify;"><p> Dessa forma, a modelagem
    do problema consiste em encontrar uma distribuição ideal de alunos nas
    escolas, levando em consideração as restrições de vagas nas escolas e as
    distâncias associadas a cada aluno-escola.</p></div>''',
                unsafe_allow_html=True)

# %%
