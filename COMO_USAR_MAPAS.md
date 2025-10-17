# 🗺️ Como Usar os Mapas Pré-Criados

## 📋 Mapas Disponíveis

Você já tem **3 mapas prontos** na pasta `maps/`:

1. **`cidade_pequena.json`** - Cidade organizada e fácil de navegar
2. **`cidade_grande.json`** - Cidade densa com muitas ruas
3. **`cidade_labirinto.json`** - Cidade complexa para testar o algoritmo A*

---

## 🚀 Método 1: Usar o Script Automático (MAIS FÁCIL)

### Passo a Passo:

1. **Execute o script de escolha**:
   ```bash
   python escolher_mapa.py
   ```

2. **Escolha o número do mapa**:
   ```
   Mapas disponíveis:
     1. cidade_grande
     2. cidade_labirinto
     3. cidade_pequena
     0. Cancelar
   
   Digite o número do mapa que deseja usar: 1
   ```

3. **Execute a aplicação**:
   ```bash
   python main.py
   ```

4. **Clique em "Carregar"** no programa

✅ **Pronto!** O mapa escolhido será carregado!

---

## 🚀 Método 2: Copiar Manualmente

### Windows (PowerShell ou CMD):

```bash
# Para usar a cidade pequena:
copy maps\cidade_pequena.json maps\cidade.json

# Para usar a cidade grande:
copy maps\cidade_grande.json maps\cidade.json

# Para usar o labirinto:
copy maps\cidade_labirinto.json maps\cidade.json
```

### Linux/Mac:

```bash
# Para usar a cidade pequena:
cp maps/cidade_pequena.json maps/cidade.json

# Para usar a cidade grande:
cp maps/cidade_grande.json maps/cidade.json

# Para usar o labirinto:
cp maps/cidade_labirinto.json maps/cidade.json
```

**Depois execute**:
```bash
python main.py
```
E clique em **"Carregar"** na aplicação.

---

## 📖 Descrição dos Mapas

### 🏘️ Cidade Pequena (`cidade_pequena.json`)

**Características:**
- ✅ Ruas bem organizadas em grid
- ✅ Poucas construções
- ✅ Fácil de navegar
- ✅ **Ideal para demonstrações básicas**

**Estrutura:**
- Ruas horizontais nas linhas 3, 7, 11
- Ruas verticais nas colunas 5, 10, 15
- Casas, prédios e praças distribuídos
- Ótimo para testar funcionalidades

**Use quando:**
- Quer mostrar o básico do sistema
- Precisa de rotas simples
- Está testando pela primeira vez

---

### 🏙️ Cidade Grande (`cidade_grande.json`)

**Características:**
- ✅ Grid denso de ruas
- ✅ Muitas construções
- ✅ Várias rotas alternativas possíveis
- ✅ **Ideal para demonstrar tráfego**

**Estrutura:**
- Ruas horizontais densas (linhas 2, 5, 8, 11, 14)
- Ruas verticais densas (colunas 3, 7, 11, 15, 19)
- Muitas casas e prédios
- Ótimo para mostrar rotas alternativas

**Use quando:**
- Quer demonstrar engarrafamentos
- Precisa de múltiplas rotas
- Quer mostrar o sistema completo

---

### 🌀 Cidade Labirinto (`cidade_labirinto.json`)

**Características:**
- ✅ Layout complexo tipo labirinto
- ✅ Caminhos difíceis de encontrar
- ✅ Testa o algoritmo A* intensamente
- ✅ **Ideal para impressionar!**

**Estrutura:**
- Ruas formando padrão de labirinto
- Muitos becos e caminhos indiretos
- Construções estrategicamente posicionadas
- O algoritmo A* realmente brilha aqui

**Use quando:**
- Quer impressionar na apresentação
- Precisa mostrar a eficiência do A*
- Quer desafiar o algoritmo

---

## 🎯 Dica para Apresentação

### Sequência Recomendada:

1. **Inicie com Cidade Pequena**
   - Mostre as funcionalidades básicas
   - Demonstre edição simples
   - Calcule uma rota direta

2. **Avance para Cidade Grande**
   - Mostre o tráfego
   - Demonstre rotas alternativas
   - Mostre recálculo automático

3. **Finalize com Cidade Labirinto**
   - Impressione com rotas complexas
   - Mostre a eficiência do A*
   - Demonstre que sempre encontra o caminho

---

## ⚡ Comandos Rápidos

### Setup Rápido para Apresentação:

```bash
# 1. Criar todos os mapas
python create_sample_maps.py

# 2. Criar as imagens
python create_sample_images.py

# 3. Escolher mapa inicial
python escolher_mapa.py
# (escolha 3 para cidade pequena)

# 4. Executar
python main.py
```

### Durante a Apresentação:

Para trocar de mapa **sem fechar o programa**:

1. **Desenhe seu mapa** no modo edição
2. Clique em **"Salvar"** (salva como cidade.json)
3. **OU** use o terminal para copiar outro mapa:
   ```bash
   copy maps\cidade_grande.json maps\cidade.json
   ```
4. Clique em **"Carregar"** no programa

---

## 🔍 Verificar Mapas Disponíveis

Para ver quais mapas você tem:

### Windows:
```bash
dir maps\*.json
```

### Linux/Mac:
```bash
ls maps/*.json
```

---

## 🛠️ Criar Seus Próprios Mapas

1. **Execute a aplicação**:
   ```bash
   python main.py
   ```

2. **Modo Edição** - Desenhe sua cidade

3. **Salve com nome customizado**:
   - O botão "Salvar" sempre salva como `cidade.json`
   - Para salvar com outro nome, copie depois:
     ```bash
     copy maps\cidade.json maps\minha_cidade.json
     ```

4. **Use depois**:
   ```bash
   copy maps\minha_cidade.json maps\cidade.json
   ```

---

## ❓ Problemas Comuns

### "Arquivo não encontrado"
**Causa**: Mapas não foram criados  
**Solução**: 
```bash
python create_sample_maps.py
```

### "Erro ao carregar mapa"
**Causa**: Arquivo `cidade.json` não existe  
**Solução**:
```bash
copy maps\cidade_pequena.json maps\cidade.json
```

### "Mapa vazio ao carregar"
**Causa**: O arquivo pode estar corrompido  
**Solução**: Recrie os mapas
```bash
python create_sample_maps.py
```

---

## 📝 Estrutura de um Arquivo de Mapa

Os mapas são salvos em formato JSON:

```json
{
  "name": "Cidade Pequena",
  "width": 20,
  "height": 15,
  "grid": [
    [0, 0, 1, 0, 0, ...],
    [0, 2, 1, 3, 0, ...],
    ...
  ]
}
```

**Legenda:**
- `0` = Vazio
- `1` = Rua
- `2` = Casa
- `3` = Prédio
- `4` = Praça
- `5` = Tráfego (não salvo nos mapas base)

---

## 🎓 Para a Apresentação

### Preparação (5 minutos antes):

```bash
# Terminal 1:
python create_sample_maps.py
python create_sample_images.py
python escolher_mapa.py
# Escolha: 3 (cidade pequena)

# Terminal 2:
python main.py
```

### Durante a apresentação:

1. ✅ **Carregar** - mostre cidade pequena
2. ✅ **Navegar** - trace uma rota
3. ✅ **Tráfego** - gere engarrafamentos
4. ✅ **Rota alternativa** - mostre recálculo
5. ✅ **Trocar mapa** - carregue cidade grande
6. ✅ **Complexidade** - carregue labirinto

---

**Agora você está pronto para usar todos os mapas!** 🎉

Escolha o método que preferir e boa apresentação! 🚀

