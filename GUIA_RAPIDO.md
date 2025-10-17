# 🚀 Guia Rápido de Instalação e Uso

## Instalação em 3 Passos

### 1️⃣ Instalar Python
Se ainda não tem Python instalado:
- Baixe de: https://www.python.org/downloads/
- Marque a opção "Add Python to PATH" durante instalação

### 2️⃣ Instalar Pygame
Abra o terminal (PowerShell ou CMD) e execute:
```bash
pip install pygame
```

### 3️⃣ Executar o Programa
No mesmo terminal, navegue até a pasta do projeto e execute:
```bash
python main.py
```

## 🎮 Uso Básico

### Primeiro Uso - Criar um Mapa

1. **Execute o programa**: `python main.py`

2. **Desenhe ruas**:
   - Clique no botão "Rua" (já selecionado por padrão)
   - Clique e arraste no grid para criar ruas (cinza escuro)
   - Crie uma rede de ruas conectadas

3. **Adicione construções**:
   - Clique em "Casa", "Prédio" ou "Praça"
   - Clique nos espaços vazios para adicionar construções

4. **Salve seu mapa**:
   - Clique no botão "Salvar"
   - O mapa será salvo em `maps/cidade.json`

### Testando a Navegação

1. **Mude para modo navegação**:
   - Clique no botão "Modo: Editar" para mudar para "Modo: Navegar"

2. **Defina a rota**:
   - Clique em uma **RUA** para definir o ponto de partida (A)
   - Clique em outra **RUA** para definir o destino (B)
   - O caminho aparecerá automaticamente em amarelo

3. **Simule tráfego**:
   - Clique em "Gerar Tráfego"
   - Veja a rota mudar para evitar engarrafamentos!

### Usar Mapas Pré-Configurados

1. **Criar mapas de exemplo**:
   ```bash
   python create_sample_maps.py
   ```

2. **Copiar um mapa para testar**:
   ```bash
   # No Windows PowerShell:
   copy maps\cidade_pequena.json maps\cidade.json
   
   # No CMD:
   copy maps\cidade_pequena.json maps\cidade.json
   
   # No Linux/Mac:
   cp maps/cidade_pequena.json maps/cidade.json
   ```

3. **Carregar no programa**:
   - Execute `python main.py`
   - Clique no botão "Carregar"

## 🎨 Legenda de Cores

| Cor | Significado |
|-----|-------------|
| 🔲 Cinza Claro | Espaço vazio |
| ⬛ Cinza Escuro | **Rua** (por onde o carro passa) |
| 🟫 Marrom | Casa |
| 🟦 Azul Claro | Prédio |
| 🟩 Verde | Praça |
| 🟥 Vermelho | **Engarrafamento** |
| 🟨 Amarelo | **Caminho calculado** |
| 🟢 Verde "A" | **Ponto de partida** |
| 🔵 Azul "B" | **Ponto de chegada** |

## ⚠️ Problemas Comuns

### "pygame não encontrado"
**Solução**: Instale o pygame:
```bash
pip install pygame
```

### "Nenhum caminho encontrado"
**Causas possíveis**:
- Ponto A ou B não está em uma rua
- Não há caminho de ruas conectando A e B
- Há tráfego bloqueando todos os caminhos

**Solução**: 
- Certifique-se de clicar apenas em ruas (cinza escuro)
- Verifique se as ruas estão conectadas
- Clique em "Limpar Tráfego" e tente novamente

### O programa não inicia
**Solução**: Verifique se está na pasta correta:
```bash
# Ver arquivos na pasta atual
dir     # Windows
ls      # Linux/Mac

# Deve ver: main.py, city.py, pathfinding.py, etc.
```

## 💡 Dicas

1. **Desenhar rápido**: Mantenha o mouse pressionado e arraste para desenhar várias células
2. **Testar algoritmo**: Crie obstáculos e veja o caminho se adaptar
3. **Tráfego realista**: Gere tráfego várias vezes para ver diferentes rotas alternativas
4. **Mapas complexos**: Use o cidade_labirinto.json para testar o algoritmo A* em cenários difíceis

## 📞 Estrutura do Projeto

```
Waze Particular/
├── main.py                 ← Execute este arquivo
├── city.py
├── pathfinding.py
├── create_sample_maps.py   ← Execute para criar exemplos
├── requirements.txt
├── README.md
├── GUIA_RAPIDO.md         ← Você está aqui
└── maps/                   ← Mapas salvos aqui
    ├── cidade.json         ← Mapa padrão ao carregar
    ├── cidade_pequena.json
    ├── cidade_grande.json
    └── cidade_labirinto.json
```

## 🎓 Para a Apresentação

1. Execute `python create_sample_maps.py` para ter mapas prontos
2. Copie o mapa desejado para `cidade.json`
3. Execute `python main.py`
4. Demonstre:
   - Carregamento de mapa
   - Definição de rota A → B
   - Geração de tráfego e rota alternativa
   - Edição do mapa (adicionar obstáculos)
   - Salvamento

Boa sorte na apresentação! 🎉

