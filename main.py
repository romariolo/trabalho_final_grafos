import sys
import networkx as nx

# -----------------------------------------------------------------------------
# ETAPA 0: REPRESENTAÇÃO DO GRAFO E LEITURA DO ARQUIVO
# -----------------------------------------------------------------------------
def ler_grafo_de_arquivo(nome_arquivo):
    """
    Lê a matriz de adjacências do grafo de um arquivo.
    O arquivo deve conter na primeira linha o número de vértices,
    seguido pelas linhas da matriz (pesos das arestas).
    """
    try:
        with open(nome_arquivo, 'r') as f:
            num_vertices = int(f.readline())
            grafo = [list(map(int, l.strip().split())) for l in f]
            print("Grafo lido com sucesso!")
            print(f"Número de vértices: {num_vertices}\n")
            return grafo
    except (FileNotFoundError, ValueError) as e:
        print(f"Erro ao ler o arquivo: {e}")
        return None

# -----------------------------------------------------------------------------
# ETAPA I: ÁRVORE GERADORA MÍNIMA (AGM) – ALGORITMO DE PRIM
# -----------------------------------------------------------------------------
def algoritmo_prim(grafo):
    """
    Constrói a Árvore Geradora Mínima (AGM) do grafo usando o algoritmo de Prim.
    A AGM conecta todos os vértices com o menor custo total sem formar ciclos.
    """
    print("Iniciando a Etapa I: Construção da Árvore Geradora Mínima...")
    num_vertices = len(grafo)
    parent, key, mst_set = [None]*num_vertices, [sys.maxsize]*num_vertices, [False]*num_vertices
    key[0], parent[0] = 0, -1
    
    for _ in range(num_vertices):
        u = -1
        min_key = sys.maxsize
        for i in range(num_vertices):
            if not mst_set[i] and key[i] < min_key:
                min_key, u = key[i], i
        if u == -1:
            break
        mst_set[u] = True
        for v in range(num_vertices):
            if grafo[u][v] > 0 and not mst_set[v] and grafo[u][v] < key[v]:
                key[v], parent[v] = grafo[u][v], u

    # Lista das arestas da AGM no formato (pai, filho, peso)
    agm_arestas = [(parent[i], i, grafo[parent[i]][i]) for i in range(1, num_vertices)]
    custo_total = sum(p for _, _, p in agm_arestas)
    print("AGM construída!")
    return agm_arestas, custo_total

# -----------------------------------------------------------------------------
# ETAPA II: IDENTIFICAÇÃO DOS VÉRTICES DE GRAU ÍMPAR NA AGM
# -----------------------------------------------------------------------------
def encontrar_vertices_grau_impar(agm_arestas, num_vertices):
    """
    Identifica os vértices da AGM que possuem grau ímpar.
    Isso é necessário para garantir que o grafo final tenha ciclo Euleriano.
    """
    print("Iniciando a Etapa II: Identificação dos Vértices de Grau Ímpar...")
    graus = [0] * num_vertices
    for u, v, _ in agm_arestas:
        graus[u] += 1
        graus[v] += 1
    vertices_impares = [i for i, grau in enumerate(graus) if grau % 2 != 0]
    print(f"Vértices de grau ímpar (conjunto I): {vertices_impares}\n")
    return vertices_impares

# -----------------------------------------------------------------------------
# ETAPA III: EMPARELHAMENTO PERFEITO DE CUSTO MÍNIMO NOS VÉRTICES ÍMPARES
# -----------------------------------------------------------------------------
def encontrar_emparelhamento_perfeito(vertices_impares, grafo_original):
    """
    Realiza o emparelhamento perfeito mínimo entre os vértices de grau ímpar.
    Isso adiciona arestas para que todos os vértices tenham grau par.
    """
    print("Iniciando a Etapa III: Emparelhamento Perfeito de Custo Mínimo...")
    subgrafo = nx.Graph()
    for i in range(len(vertices_impares)):
        for j in range(i + 1, len(vertices_impares)):
            u, v = vertices_impares[i], vertices_impares[j]
            subgrafo.add_edge(u, v, weight=grafo_original[u][v])
    
    emparelhamento_nx = nx.min_weight_matching(subgrafo)
    arestas_emparelhamento = [(u, v, grafo_original[u][v]) for u, v in emparelhamento_nx]
    custo_emparelhamento = sum(p for _, _, p in arestas_emparelhamento)
    print("Emparelhamento encontrado!")
    return arestas_emparelhamento, custo_emparelhamento

# -----------------------------------------------------------------------------
# ETAPA IV: CRIAÇÃO DO MULTIGRAFO EULERIANO
# -----------------------------------------------------------------------------
def criar_multigrafo_euleriano(agm_arestas, arestas_emparelhamento, num_vertices):
    """
    Combina as arestas da AGM e do emparelhamento para formar um multigrafo Euleriano,
    onde todos os vértices possuem grau par, condição para existir ciclo Euleriano.
    """
    print("Iniciando a Etapa IV: União das Arestas e Criação do Multigrafo H...")
    multigrafo_adj = [[] for _ in range(num_vertices)]
    todas_as_arestas = agm_arestas + arestas_emparelhamento
    for u, v, _ in todas_as_arestas:
        multigrafo_adj[u].append(v)
        multigrafo_adj[v].append(u)
    print("Multigrafo H criado com sucesso.\n")
    return multigrafo_adj

# -----------------------------------------------------------------------------
# ETAPA V: ENCONTRAR CICLO EULERIANO NO MULTIGRAFO
# -----------------------------------------------------------------------------
def encontrar_ciclo_euleriano(multigrafo_adj):
    """
    Encontra um ciclo Euleriano que percorre todas as arestas do multigrafo exatamente uma vez.
    """
    print("Iniciando a Etapa V: Encontrando o Ciclo Euleriano...")
    adj_copia = [vizinhos[:] for vizinhos in multigrafo_adj]
    pilha, ciclo = [], []
    pilha.append(0)
    
    while pilha:
        vertice_atual = pilha[-1]
        if adj_copia[vertice_atual]:
            proximo_vizinho = adj_copia[vertice_atual].pop(0)
            adj_copia[proximo_vizinho].remove(vertice_atual)
            pilha.append(proximo_vizinho)
        else:
            ciclo.append(pilha.pop())
            
    ciclo_final = ciclo[::-1]
    print(f"Ciclo Euleriano encontrado: {ciclo_final}\n")
    return ciclo_final

# -----------------------------------------------------------------------------
# ETAPA VI: SHORTCUTTING - CRIAÇÃO DO CICLO HAMILTONIANO APROXIMADO
# -----------------------------------------------------------------------------
def criar_ciclo_hamiltoniano(ciclo_euleriano, grafo_original):
    """
    Transforma o ciclo Euleriano em um ciclo Hamiltoniano aproximado,
    "pulando" vértices já visitados (shortcutting), para visitar cada vértice exatamente uma vez.
    Calcula também o custo total do ciclo.
    """
    print("Iniciando a Etapa VI: Criando o Ciclo Hamiltoniano (Shortcutting)...")
    
    visitados = set()
    caminho_hamiltoniano = []
    for vertice in ciclo_euleriano:
        if vertice not in visitados:
            visitados.add(vertice)
            caminho_hamiltoniano.append(vertice)
            
    ciclo_hamiltoniano_final = caminho_hamiltoniano + [caminho_hamiltoniano[0]]
    
    custo_total = 0
    print("\nCalculando o custo da rota final...")
    for i in range(len(ciclo_hamiltoniano_final) - 1):
        u = ciclo_hamiltoniano_final[i]
        v = ciclo_hamiltoniano_final[i+1]
        peso = grafo_original[u][v]
        custo_total += peso
        print(f"  Custo da aresta ({u}, {v}): {peso}")
    
    return ciclo_hamiltoniano_final, custo_total

# -----------------------------------------------------------------------------
# FUNÇÃO PRINCIPAL
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    arquivo_entrada = "grafo_exemplo.txt"
    matriz_adjacencias = ler_grafo_de_arquivo(arquivo_entrada)
    
    if matriz_adjacencias:
        num_vertices_total = len(matriz_adjacencias)

        agm_arestas, custo_agm = algoritmo_prim(matriz_adjacencias)
        print(f"Arestas: {agm_arestas}")
        print(f"Custo total da AGM: {custo_agm}\n")

        vertices_impares = encontrar_vertices_grau_impar(agm_arestas, num_vertices_total)
        
        arestas_emparelhamento, custo_emparelhamento = encontrar_emparelhamento_perfeito(vertices_impares, matriz_adjacencias)
        print("Novas arestas do emparelhamento:")
        for u, v, peso in arestas_emparelhamento:
            print(f"  Aresta: ({u}, {v}), Peso: {peso}")
        print(f"Custo do Emparelhamento: {custo_emparelhamento}\n")

        multigrafo_h = criar_multigrafo_euleriano(agm_arestas, arestas_emparelhamento, num_vertices_total)
        
        ciclo_euleriano = encontrar_ciclo_euleriano(multigrafo_h)
        
        ciclo_final, custo_final = criar_ciclo_hamiltoniano(ciclo_euleriano, matriz_adjacencias)
        
        print("\n" + "="*40)
        print("      RESULTADO FINAL DO ALGORITMO")
        print("="*40)
        print(f"O ciclo Hamiltoniano aproximado é: {ciclo_final}")
        print(f"Custo total do ciclo: {custo_final}")
        print("="*40)
