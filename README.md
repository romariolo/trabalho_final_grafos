

# Algoritmo de Christofides para o Problema do Caixeiro Viajante Métrico

Este projeto implementa uma solução aproximada para o Problema do Caixeiro Viajante Métrico ($\\Delta$-TSP) utilizando o **Algoritmo de Christofides**. O algoritmo é projetado para grafos completos com pesos que satisfazem a desigualdade triangular, garantindo uma solução com custo no máximo 1,5 vezes o valor ótimo.

## Índice

  * [Visão Geral](https://www.google.com/search?q=%23vis%C3%A3o-geral)
  * [Pré-requisitos](https://www.google.com/search?q=%23pr%C3%A9-requisitos)
  * [Como Usar](https://www.google.com/search?q=%23como-usar)
      * [Estrutura do Arquivo de Entrada](https://www.google.com/search?q=%23estrutura-do-arquivo-de-entrada)
      * [Executando o Programa](https://www.google.com/search?q=%23executando-o-programa)
  * [Estrutura do Projeto](https://www.google.com/search?q=%23estrutura-do-projeto)
  * [Detalhes da Implementação](https://www.google.com/search?q=%23detalhes-da-implementa%C3%A7%C3%A3o)
  * [Créditos](https://www.google.com/search?q=%23cr%C3%A9ditos)

-----

## Visão Geral

O Problema do Caixeiro Viajante (TSP) busca o ciclo de menor custo que visita cada vértice de um grafo exatamente uma vez. A variante métrica ($\\Delta$-TSP) adiciona a condição de que os pesos das arestas obedecem à desigualdade triangular.

O Algoritmo de Christofides aborda o $\\Delta$-TSP através das seguintes etapas:

1.  **Construção de uma Árvore Geradora Mínima (AGM).**
2.  **Identificação dos vértices de grau ímpar na AGM.**
3.  **Construção de um emparelhamento perfeito de custo mínimo** nos vértices de grau ímpar.
4.  **União das arestas da AGM e do emparelhamento**, formando um multigrafo Euleriano.
5.  **Determinação de um ciclo Euleriano** nesse multigrafo.
6.  **Atalho (shortcutting)** do ciclo Euleriano para obter um ciclo Hamiltoniano aproximado.

-----

## Pré-requisitos

Para rodar este código, você precisará ter o **Python 3** instalado. Além disso, a única biblioteca externa utilizada, conforme as especificações do trabalho, é o **NetworkX** para a etapa de emparelhamento perfeito de custo mínimo.

Você pode instalar o NetworkX usando `pip`:

```bash
pip install networkx
```

-----

## Como Usar

### Estrutura do Arquivo de Entrada

O programa espera um arquivo de texto (`.txt`) como entrada, que representa a matriz de adjacências do grafo.

  * A **primeira linha** deve conter um único inteiro: o número de vértices ($N$) do grafo.
  * As **próximas $N$ linhas** devem representar a matriz de adjacências, onde cada valor é o peso da aresta entre os vértices. Os pesos devem ser positivos e a matriz simétrica.

**Exemplo (`grafo_exemplo.txt`):**

```
4
0 10 15 20
10 0 35 25
15 35 0 30
20 25 30 0
```

Neste exemplo:

  * `4` indica que o grafo tem 4 vértices (0 a 3).
  * `0 10 15 20` na segunda linha representa as distâncias do vértice 0 para os vértices 0, 1, 2 e 3, respectivamente.

### Executando o Programa

1.  **Salve o código:** Certifique-se de que o arquivo Python (`christofides_algorithm.py` ou o nome que você usou) e o arquivo de entrada (`grafo_exemplo.txt`) estão no mesmo diretório.

2.  **Abra o terminal ou prompt de comando** no diretório onde os arquivos estão salvos.

3.  **Execute o script Python:**

    ```bash
    python christofides_algorithm.py
    ```

    **(Nota:** O programa está configurado para ler `grafo_exemplo.txt` por padrão, como definido na linha `arquivo_entrada = "grafo_exemplo.txt"`.)

### Saída do Programa

Ao final da execução, o programa imprimirá no console o **ciclo Hamiltoniano aproximado** encontrado pelo algoritmo e o **custo total** desse ciclo. Você verá mensagens de progresso para cada etapa do algoritmo.

**Exemplo de Saída:**

```
Grafo lido com sucesso!
Número de vértices: 4

Iniciando a Etapa I: Construção da Árvore Geradora Mínima... Pensando na conexão mais barata! 🌳
AGM construída! Conectamos tudo da forma mais econômica. 🌲

Iniciando a Etapa II: Identificação dos Vértices de Grau Ímpar... Quem tem conexão 'sobrando'? 🤔
Vértices de grau ímpar (conjunto I): [1, 2]. Vamos resolver isso! 

Iniciando a Etapa III: Emparelhamento Perfeito de Custo Mínimo... Conectando os 'solitários' com inteligência! 🤝
Emparelhamento encontrado! Os 'pares' estão conectados. 🎉

Iniciando a Etapa IV: União das Arestas e Criação do Multigrafo H... Juntando as peças do quebra-cabeça! 🧩
Multigrafo H criado com sucesso. Agora temos um mapa 'percorrível' por completo! 🗺️

Iniciando a Etapa V: Encontrando o Ciclo Euleriano... Explorando cada caminho! 🚶‍♂️
Ciclo Euleriano encontrado: [0, 1, 2, 3, 0]. Percorremos todas as arestas! 🎉

Iniciando a Etapa VI: Criando o Ciclo Hamiltoniano (Shortcutting)... A rota final está surgindo! 🚀

Calculando o custo da rota final... Quase lá! 💰
  Custo da aresta (0, 1): 10
  Custo da aresta (1, 2): 35
  Custo da aresta (2, 3): 30
  Custo da aresta (3, 0): 20
Custo total calculado. Chegamos ao fim da jornada! ✅

========================================
      RESULTADO FINAL DO ALGORITMO
========================================
O ciclo Hamiltoniano aproximado é: [0, 1, 2, 3, 0] Essa é a nossa melhor rota! 📍
Custo total do ciclo: 95. Valor da nossa aventura! 💲
========================================
```

*(Nota: Os vértices e custos na saída de exemplo podem variar dependendo do seu `grafo_exemplo.txt`.)*

-----

## Estrutura do Projeto

  * `christofides_algorithm.py`: O arquivo principal contendo a implementação do Algoritmo de Christofides.
  * `grafo_exemplo.txt`: Um exemplo de arquivo de entrada para testar o programa.

-----

## Detalhes da Implementação

Este projeto segue rigorosamente as etapas do Algoritmo de Christofides:

  * **Leitura do Grafo**: Implementação própria para ler a matriz de adjacências de um arquivo.
  * **Algoritmo de Prim**: Implementação manual do algoritmo para construir a Árvore Geradora Mínima.
  * **Vértices de Grau Ímpar**: Lógica própria para identificar os vértices com grau ímpar na AGM.
  * **Emparelhamento Perfeito de Custo Mínimo**: Utiliza a função `nx.min_weight_matching` da biblioteca **NetworkX** (única biblioteca externa permitida).
  * **Multigrafo Euleriano**: Construção manual do multigrafo a partir das arestas da AGM e do emparelhamento.
  * **Ciclo Euleriano**: Implementação manual para encontrar o ciclo Euleriano no multigrafo.
  * **Shortcutting**: Lógica própria para transformar o ciclo Euleriano em um ciclo Hamiltoniano aproximado, removendo vértices duplicados.

-----

## Créditos

**UNIVERSIDADE FEDERAL DO CEARÁ - UFC** **CAMPUS DE CRATEÚS** **DISCIPLINA:** ALGORITMOS EM GRAFOS (CRT0390)  
**PROFESSOR:** RAFAEL MARTINS BARROS

**EQUIPE:**

  * Francisco Romário Rodrigues Lopes
  * Diogo Bezerra da Costa
  * Rodolfo Rodrigues de Araujo
  * Hércules Bruno Ferreira Norte

-----
