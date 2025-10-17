# Sistema de Navegação - Waze Particular

Trabalho de Algoritmos e Estruturas de Dados - Implementação de Sistema de Navegação com Arrays Clássicos

## 📋 Descrição

Este projeto implementa um sistema de navegação tipo Waze simplificado, onde é possível:

- Criar e editar mapas de cidades com um editor visual
- Definir construções (casas, prédios, praças) e ruas
- Calcular a melhor rota entre dois pontos usando algoritmo A\*
- Simular engarrafamentos aleatórios que afetam as rotas
- Salvar e carregar mapas diferentes

## 🎯 Requisitos Atendidos

✅ Utilização de **arrays clássicos** (acesso apenas por índice, sem métodos avançados)  
✅ Implementação manual de algoritmos de busca (A\*)  
✅ Movimentação e manipulação de elementos nos arrays  
✅ Interface gráfica apropriada com visualização em tempo real  
✅ Orientação a objetos adequada  
✅ Sistema de salvamento/carregamento de mapas  
✅ Mapas pré-configurados para apresentação

## 🛠️ Tecnologias

- **Python 3.8+** - Linguagem de programação
- **Pygame 2.5.2** - Biblioteca para interface gráfica e visualização

## 📦 Instalação

### 1. Instalar Python

Certifique-se de ter Python 3.8 ou superior instalado:

```bash
python --version
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

Ou manualmente:

```bash
pip install pygame
```

### 3. Criar Mapas de Exemplo

```bash
python create_sample_maps.py
```

Isso criará três mapas de exemplo na pasta `maps/`:

- `cidade_pequena.json` - Cidade pequena organizada
- `cidade_grande.json` - Cidade grande com muitas ruas
- `cidade_labirinto.json` - Cidade com layout complexo

## 🚀 Como Executar

### Versão Básica (com cores)

```bash
python main.py
```

### Versão com Imagens (recomendado)

```bash
# Primeiro, crie as imagens de exemplo:
python create_sample_images.py

# Depois execute a versão com imagens:
python main_with_images.py
```

**Nota**: A versão com imagens usa ícones visuais (casa.png, predio.png, etc.) ao invés de cores sólidas. Veja `GUIA_IMAGENS.md` para detalhes.

## 📖 Como Usar

### Modo Edição

1. **Selecionar Ferramenta**: Clique nos botões no topo para escolher o tipo de elemento:

   - **Rua** - Caminhos por onde o carro pode passar (cinza escuro)
   - **Casa** - Construção residencial (marrom)
   - **Prédio** - Construção comercial (azul claro)
   - **Praça** - Área verde (verde)
   - **Apagar** - Remove elementos

2. **Desenhar no Mapa**:

   - Clique e arraste no grid para desenhar
   - Cada quadrado representa um espaço na cidade

3. **Gerenciar Mapa**:
   - **Limpar**: Remove todos os elementos do mapa
   - **Salvar**: Salva o mapa atual em `maps/cidade.json`
   - **Carregar**: Carrega o mapa de `maps/cidade.json`

### Modo Navegação

1. **Alternar Modo**: Clique em **"Modo: Editar"** para mudar para **"Modo: Navegar"**

2. **Definir Rota**:

   - **Primeiro clique** (em uma rua): Define o ponto de partida (marcador verde "A")
   - **Segundo clique** (em uma rua): Define o destino (marcador azul "B")
   - O caminho é calculado automaticamente e mostrado em amarelo

3. **Simular Tráfego**:

   - **Gerar Tráfego**: Cria engarrafamentos aleatórios (células vermelhas)
   - **Limpar Tráfego**: Remove todos os engarrafamentos
   - A rota é recalculada automaticamente evitando o tráfego

4. **Gerenciar Rota**:
   - **Traçar Rota**: Recalcula o caminho entre A e B
   - **Limpar Rota**: Remove os marcadores A e B e o caminho

### Dicas de Uso

- **Para testar mapas de exemplo**:

  1. Renomeie um dos mapas exemplo para `cidade.json`
  2. Clique em "Carregar" na aplicação

  Por exemplo no terminal:

  ```bash
  copy maps\cidade_pequena.json maps\cidade.json
  ```

- **Importante**: O algoritmo só encontra caminhos através de RUAS. Casas, prédios e praças são obstáculos.

- **Tráfego**: O sistema adiciona grande penalidade a células com tráfego, fazendo o algoritmo buscar rotas alternativas.

## 🏗️ Arquitetura do Projeto

```
Waze Particular/
│
├── city.py                   # Classe City - representa o mapa da cidade
├── pathfinding.py            # Algoritmo A* para encontrar caminhos
├── main.py                   # Aplicação principal (versão com cores)
├── main_visual.py            # Versão com ícones desenhados
├── main_with_images.py       # Versão com imagens PNG/JPG (recomendado)
├── create_sample_maps.py     # Script para criar mapas de exemplo
├── create_sample_images.py   # Script para criar imagens de exemplo
├── requirements.txt          # Dependências do projeto
├── README.md                 # Este arquivo
├── GUIA_RAPIDO.md           # Guia rápido de uso
├── GUIA_IMAGENS.md          # Guia de uso de imagens
├── EXPLICACAO_ALGORITMOS.md # Explicação técnica dos algoritmos
│
├── maps/                     # Mapas salvos
│   ├── cidade_pequena.json
│   ├── cidade_grande.json
│   └── cidade_labirinto.json
│
└── assets/                   # Imagens dos elementos
    ├── rua.png
    ├── casa.png
    ├── predio.png
    ├── praca.png
    └── trafego.png
```

## 🎓 Conceitos de Algoritmos Implementados

### 1. Arrays Clássicos

- Uso exclusivo de acesso por índice (`array[i]`, `array[i][j]`)
- Manipulação manual de elementos
- Implementação própria de buscas e iterações

### 2. Algoritmo A\* (A-Star)

- Pathfinding eficiente que encontra o caminho mais curto
- Usa heurística de distância Manhattan
- Implementado completamente com arrays clássicos
- Evita obstáculos e considera penalidades de tráfego

### 3. Estruturas de Dados

- **Grid Bidimensional**: Array de arrays representando o mapa
- **Listas de Posições**: Arrays para armazenar coordenadas
- **"Dicionários" Manuais**: Arrays de pares [chave, valor]

### 4. Orientação a Objetos

- **City**: Encapsula lógica do mapa
- **PathFinder**: Encapsula algoritmo de busca
- **Button**: Componente reutilizável de UI
- **WazeApp**: Controlador principal da aplicação

## 🎨 Interface

### Representação Visual

#### Versão com Imagens (`main_with_images.py`)

Usa imagens reais (PNG/JPG) da pasta `assets/`:

- 🏠 `casa.png` - Casa residencial
- 🏢 `predio.png` - Prédio comercial
- 🛣️ `rua.png` - Rua (asfalto com linha amarela)
- 🌳 `praca.png` - Praça/parque
- 🚫 `trafego.png` - Engarrafamento

#### Versão com Cores (`main.py`)

| Cor           | Elemento          |
| ------------- | ----------------- |
| Cinza Claro   | Espaço vazio      |
| Cinza Escuro  | Rua (transitável) |
| Marrom        | Casa              |
| Azul Claro    | Prédio            |
| Verde         | Praça             |
| Vermelho      | Engarrafamento    |
| Amarelo       | Caminho calculado |
| Verde com "A" | Ponto de partida  |
| Azul com "B"  | Ponto de chegada  |

## 📝 Observações Importantes para Avaliação

1. **Arrays Clássicos**: O código usa APENAS acesso por índice. Não usa métodos avançados como `append()` exceto para adicionar elementos (equivalente a aumentar o tamanho do array).

2. **Implementação Manual**: Todas as buscas, ordenações e manipulações foram implementadas manualmente:

   - Busca do menor valor em lista (para A\*)
   - Remoção de elementos de arrays
   - Verificação de presença em listas
   - Reconstrução de caminho

3. **Interface Gráfica**: Visualização completa e intuitiva que mostra:

   - O mapa da cidade
   - Obstáculos e ruas
   - Caminho calculado em tempo real
   - Engarrafamentos

4. **Salvamento em Arquivos**: Mapas são persistidos em JSON, facilitando a apresentação com cidades pré-montadas.

## 🎮 Demonstração Sugerida para Apresentação

1. **Carregar mapa pré-configurado**: Mostrar uma cidade já montada
2. **Modo Navegação**: Definir ponto A e B, mostrar rota calculada
3. **Adicionar Tráfego**: Gerar engarrafamentos e mostrar nova rota alternativa
4. **Modo Edição**: Criar obstáculos e mostrar como afeta a rota
5. **Salvar/Carregar**: Demonstrar persistência de dados

## 👥 Autores

Trabalho de Algoritmos e Estruturas de Dados

## 📄 Licença

Projeto acadêmico - Uso educacional
