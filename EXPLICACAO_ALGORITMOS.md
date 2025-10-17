# 📚 Explicação dos Algoritmos e Estruturas de Dados

Este documento explica os conceitos de Algoritmos e Estruturas de Dados implementados no projeto.

## 🎯 Arrays Clássicos

### O que são?
Arrays clássicos são estruturas de dados homogêneas (todos elementos do mesmo tipo) com:
- Tamanho definido
- Acesso por índice (posição)
- Elementos contíguos na memória

### Como foram usados no projeto?

#### 1. **Grid Bidimensional** (`city.py`)
```python
# Array de arrays representando o mapa
self.grid = []
for i in range(height):
    row = []
    for j in range(width):
        row.append(self.EMPTY)
    self.grid.append(row)
```

**Explicação**: 
- Criamos um array principal com `height` linhas
- Cada linha é um array com `width` colunas
- Acesso: `self.grid[linha][coluna]` - apenas por índice!

#### 2. **Lista de Posições** (`city.py`)
```python
self.traffic_positions = []  # Array de coordenadas [x, y]
```

**Explicação**: 
- Array que armazena arrays de 2 elementos [x, y]
- Cada posição é acessada por índice: `self.traffic_positions[i]`
- Para processar: usamos loops com índice manual

#### 3. **"Dicionários" Manuais** (`pathfinding.py`)
```python
g_score = []  # Array de pares [chave, valor]
# Exemplo: [["5,3", 10], ["7,2", 15], ...]
```

**Explicação**: 
- Simulamos dicionários com arrays de pares
- Cada elemento é `[chave, valor]`
- Busca manual percorrendo todo o array

### Restrições Seguidas
✅ **SIM**: Acesso por índice (`array[i]`)  
✅ **SIM**: Uso de `len()` para tamanho  
✅ **SIM**: Iteração manual com `for i in range(len(array))`  
✅ **SIM**: Adicionar elementos com `append()` (equivale a expandir array)  

❌ **NÃO**: Métodos avançados como `.find()`, `.filter()`, `.map()`  
❌ **NÃO**: Compreensões de lista (list comprehensions)  
❌ **NÃO**: Slicing avançado  
❌ **NÃO**: Estruturas especiais (set, dict nativo, etc.)  

## 🔍 Algoritmo A* (A-Star)

### O que é?
A* é um algoritmo de busca em grafos que encontra o **caminho mais curto** entre dois pontos.

### Como funciona?

#### Conceitos Principais

1. **Função de Custo f(n) = g(n) + h(n)**
   - `g(n)` = custo real do início até o nó atual
   - `h(n)` = estimativa (heurística) do nó atual até o destino
   - `f(n)` = custo total estimado

2. **Heurística - Distância Manhattan**
```python
def heuristic(self, pos1, pos2):
    return abs(x1 - x2) + abs(y1 - y2)
```
**Por quê?** Em um grid onde só podemos mover vertical/horizontal (não diagonal), a distância Manhattan é perfeita.

3. **Listas Open e Closed**
   - **Open List**: Nós a explorar
   - **Closed List**: Nós já explorados

### Passo a Passo do A*

```
1. Adiciona ponto inicial à Open List
2. Enquanto Open List não estiver vazia:
   a. Seleciona nó com menor f(n) da Open List
   b. Se é o destino → reconstrói caminho e retorna
   c. Move nó para Closed List
   d. Para cada vizinho:
      - Se já foi explorado (Closed) → ignora
      - Calcula custo tentativo
      - Se caminho é melhor → atualiza custos e pai
3. Se Open List esvaziar → não há caminho
```

### Implementação no Projeto

```python
# Encontra nó com menor f_score
current = open_list[0]
for i in range(1, len(open_list)):
    if f_score[i] < f_score[current]:
        current = open_list[i]
```

**Nota**: Aqui fazemos busca linear porque:
- Não podemos usar heap (estrutura avançada)
- É implementação manual com arrays clássicos
- Complexidade: O(n) por iteração

### Penalidade de Tráfego
```python
cost = 1
if self.city.get_cell(neighbor[0], neighbor[1]) == self.city.TRAFFIC:
    cost = 10  # Penalidade alta!
```

**Resultado**: O algoritmo "evita" células com tráfego porque o custo fica muito alto.

## 🚗 Busca de Vizinhos

### Exploração do Grid
```python
def get_neighbors(self, pos):
    neighbors = []
    directions = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # ↑ → ↓ ←
    
    for i in range(len(directions)):
        new_x = x + directions[i][0]
        new_y = y + directions[i][1]
        
        if self.city.is_walkable(new_x, new_y):
            neighbors.append([new_x, new_y])
    
    return neighbors
```

**Explicação**:
- Verifica 4 direções (norte, leste, sul, oeste)
- Só adiciona se for RUA (walkable)
- Retorna array de posições válidas

## 🔄 Reconstrução do Caminho

### Como funciona?
Depois que A* encontra o destino, precisamos reconstruir o caminho de volta.

```python
# Durante A*: guardamos "de onde viemos"
came_from[vizinho] = nó_atual

# No final: percorremos de trás para frente
path = []
temp = destino
while temp is not None:
    path.append(temp)
    temp = came_from[temp]

# Invertemos para ficar início → fim
reversed_path = []
for i in range(len(path) - 1, -1, -1):
    reversed_path.append(path[i])
```

## 📊 Complexidade Computacional

### Algoritmo A*

- **Tempo**: O(b^d) onde:
  - b = fator de ramificação (4 vizinhos)
  - d = profundidade da solução
  
  **No pior caso**: O(n²) onde n = número de células

- **Espaço**: O(n) - armazena nós em open/closed lists

### Operações no Projeto

| Operação | Complexidade | Explicação |
|----------|--------------|------------|
| `get_cell(x, y)` | O(1) | Acesso direto por índice |
| `set_cell(x, y, value)` | O(1) | Atribuição direta |
| `find_path(start, end)` | O(n²) | A* no pior caso |
| `get_neighbors(pos)` | O(1) | 4 verificações constantes |
| Busca em lista | O(n) | Percorre array inteiro |
| `generate_random_traffic()` | O(n²) | Percorre todo grid |

## 🎲 Geração de Tráfego Aleatório

### Algoritmo
```python
def generate_random_traffic(self, num_traffic):
    # 1. Encontra todas as ruas
    street_positions = []
    for y in range(self.height):
        for x in range(self.width):
            if self.grid[y][x] == self.STREET:
                street_positions.append([x, y])
    
    # 2. Seleciona aleatoriamente
    count = 0
    while count < num_traffic:
        idx = random.randint(0, len(street_positions) - 1)
        pos = street_positions[idx]
        if self.add_traffic(pos[0], pos[1]):
            count += 1
```

**Complexidade**: O(n²) - percorre todo grid

## 💾 Salvamento/Carregamento

### Persistência de Dados

```python
# Salvamento
data = {
    'name': self.name,
    'width': self.width,
    'height': self.height,
    'grid': self.grid  # Array bidimensional inteiro
}
json.dump(data, file)

# Carregamento
data = json.load(file)
city.grid = data['grid']  # Restaura array
```

**Vantagens**:
- JSON é texto legível
- Fácil de editar manualmente
- Portável entre sistemas

## 🎨 Orientação a Objetos

### Classes Implementadas

#### 1. **City**
```python
class City:
    - Atributos: width, height, name, grid, traffic_positions
    - Métodos: set_cell, get_cell, is_walkable, add_traffic, ...
    - Responsabilidade: Gerenciar estado do mapa
```

#### 2. **PathFinder**
```python
class PathFinder:
    - Atributos: city (referência)
    - Métodos: find_path, heuristic, get_neighbors
    - Responsabilidade: Algoritmo de busca
```

#### 3. **Button** (UI)
```python
class Button:
    - Atributos: rect, text, color, is_hovered
    - Métodos: draw, handle_event
    - Responsabilidade: Componente de interface
```

#### 4. **WazeApp** (Controlador)
```python
class WazeApp:
    - Atributos: screen, city, pathfinder, mode, ...
    - Métodos: run, handle_events, draw_grid, draw_ui
    - Responsabilidade: Controle principal da aplicação
```

### Princípios OO Aplicados

✅ **Encapsulamento**: Dados e métodos juntos em classes  
✅ **Abstração**: Interface pública esconde implementação  
✅ **Responsabilidade Única**: Cada classe tem um propósito  
✅ **Composição**: WazeApp "tem um" City e PathFinder  

## 🧪 Testando o Algoritmo

### Casos de Teste Sugeridos

1. **Caminho Simples**
   - Cidade com ruas em linha reta
   - Verificar se encontra o caminho direto

2. **Caminho com Obstáculos**
   - Bloquear caminho direto com prédios
   - Verificar se contorna obstáculos

3. **Caminho com Tráfego**
   - Adicionar engarrafamentos
   - Verificar se escolhe rota alternativa mais longa mas sem tráfego

4. **Sem Caminho**
   - Destino completamente bloqueado
   - Deve retornar `None`

5. **Labirinto**
   - Cidade complexa (use cidade_labirinto.json)
   - Testa eficiência do A*

## 📖 Referências

### Conceitos Estudados

1. **Arrays**: Estrutura de dados fundamental
2. **Algoritmo A***: Busca informada em grafos
3. **Heurística**: Função de estimativa
4. **Grafos Implícitos**: Grid como grafo
5. **Pathfinding**: Encontrar caminhos
6. **Complexidade**: Big O notation

### Materiais Complementares

- [Visualização do A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- Livro: "Introduction to Algorithms" (CLRS)
- Artigo original do A*: Hart, Nilsson & Raphael (1968)

---

## 💡 Questões para Discussão

1. **Por que usar Manhattan e não Euclidiana?**
   - Em grid 4-direções, Manhattan é admissível e consistente
   - Euclidiana subestimaria distância real

2. **Por que não usar Dijkstra?**
   - Dijkstra é A* sem heurística (h=0)
   - A* é mais eficiente com heurística boa

3. **Como melhorar performance?**
   - Usar heap para open_list (não permitido aqui)
   - Bidirectional A* (busca dos dois lados)
   - Jump Point Search (otimização para grids)

4. **Arrays vs. Listas Ligadas?**
   - Arrays: acesso O(1), inserção/remoção O(n)
   - Listas: acesso O(n), inserção/remoção O(1)
   - Aqui: acesso é mais importante que inserção

---

**Implementado com ❤️ para aprender Algoritmos e Estruturas de Dados**

