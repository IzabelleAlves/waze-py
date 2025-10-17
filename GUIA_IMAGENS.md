# 🖼️ Guia de Uso de Imagens

Este guia explica como usar imagens personalizadas no sistema de navegação.

## 📁 Estrutura de Pastas

```
Waze Particular/
├── assets/              ← Pasta para suas imagens
│   ├── street.png
│   ├── casa.png
│   ├── predio.png
│   ├── praca.png
│   └── trafego.png
├── main_with_images.py  ← Versão com suporte a imagens
└── ...
```

## 🚀 Início Rápido

### Opção 1: Usar Imagens Geradas Automaticamente

Se você não tem imagens prontas, execute este comando para criar imagens simples:

```bash
python create_sample_images.py
```

Isso criará automaticamente 5 imagens na pasta `assets/`.

### Opção 2: Usar Suas Próprias Imagens

1. **Crie a pasta assets** (se não existir):
   ```bash
   mkdir assets
   ```

2. **Coloque suas imagens** na pasta `assets/` com estes nomes EXATOS:
   - `casa.png` ou `casa.jpg` - Imagem de uma casa
   - `predio.png` ou `predio.jpg` - Imagem de um prédio
   - `street.png` ou `rua.jpg` - Imagem de uma rua
   - `praca.png` ou `praca.jpg` - Imagem de uma praça/parque
   - `trafego.png` ou `trafego.jpg` - Imagem de tráfego/engarrafamento

3. **Execute a aplicação**:
   ```bash
   python main_with_images.py
   ```

## 📐 Especificações das Imagens

### Tamanho Recomendado
- **40x40 pixels** - Tamanho padrão das células
- O sistema redimensiona automaticamente, mas imagens 40x40 ficam perfeitas

### Formatos Suportados
- PNG (recomendado)
- JPG
- GIF
- BMP

### Nomes dos Arquivos

| Arquivo | Representa | Descrição |
|---------|-----------|-----------|
| `street.png` | Rua | Caminho por onde o carro passa (cinza com linha amarela) |
| `casa.png` | Casa | Construção residencial (casa pequena) |
| `predio.png` | Prédio | Construção comercial (prédio alto) |
| `praca.png` | Praça | Área verde/parque (árvores, grama) |
| `trafego.png` | Engarrafamento | Símbolo de trânsito/bloqueio (vermelho) |

## 🎨 Dicas para Criar/Escolher Imagens

### Casa
- Pode ser uma casa vista de cima
- Pode ser uma foto de telhado
- Cores sugeridas: marrom, bege, vermelho (telhado)

### Prédio
- Pode ser um prédio visto de cima
- Pode mostrar janelas
- Cores sugeridas: cinza, azul, branco

### Rua
- Asfalto cinza escuro
- Pode ter linha amarela no meio
- Evite muitos detalhes (fica pequeno)

### Praça
- Verde com árvores
- Pode ter bancos, fonte
- Cores: verde, marrom (árvores)

### Tráfego
- Símbolo de alerta (triângulo vermelho)
- Pode ser um "X" vermelho
- Pode ser carros parados

## 🔍 Onde Encontrar Imagens Gratuitas

### Sites de Ícones Gratuitos
1. **Flaticon** - https://www.flaticon.com
   - Busque: "house icon", "building icon", "road icon", "park icon"
   
2. **Icons8** - https://icons8.com
   - Busque: "house", "building", "street", "park"
   
3. **Freepik** - https://www.freepik.com
   - Busque: "city icons top view"

### Editores Online para Redimensionar
1. **Pixlr** - https://pixlr.com/editor/
2. **PhotoPea** - https://www.photopea.com/
3. No Windows: Paint (Redimensionar para 40x40)

## 💡 Exemplo de Uso

### 1. Gerar Imagens Automáticas
```bash
# Cria imagens simples na pasta assets
python create_sample_images.py

# Executa aplicação com imagens
python main_with_images.py
```

### 2. Usar Imagens Personalizadas
```bash
# Baixe imagens da internet e salve como:
# assets/casa.png
# assets/predio.png
# assets/street.png
# assets/praca.png
# assets/trafego.png

# Execute
python main_with_images.py
```

## 🔧 Sistema de Fallback

Se uma imagem não for encontrada, o sistema automaticamente usa **cores sólidas** como backup:

| Tipo | Cor de Fallback |
|------|-----------------|
| Rua | Cinza escuro |
| Casa | Marrom |
| Prédio | Azul claro |
| Praça | Verde |
| Tráfego | Vermelho |

Ao iniciar `main_with_images.py`, você verá no console quais imagens foram carregadas:

```
==================================================
STATUS DAS IMAGENS
==================================================
[OK] Rua: Imagem carregada
[OK] Casa: Imagem carregada
[--] Prédio: Usando cor (coloque predio.png na pasta assets/)
[OK] Praça: Imagem carregada
[OK] Tráfego: Imagem carregada
==================================================
```

## 🎯 Comparação das Versões

### `main.py` - Versão com Cores
- Usa apenas cores sólidas
- Mais leve
- Não precisa de imagens

### `main_visual.py` - Versão com Ícones Desenhados
- Desenha ícones simples com formas geométricas
- Visual melhorado
- Não precisa de arquivos externos

### `main_with_images.py` - Versão com Imagens Reais
- Carrega imagens PNG/JPG da pasta `assets/`
- Visual mais realista
- Você pode usar suas próprias imagens
- Sistema de fallback para cores se imagem não existir

## 📝 Checklist

- [ ] Pasta `assets/` criada
- [ ] Imagem `street.png` adicionada (ou gerada)
- [ ] Imagem `casa.png` adicionada (ou gerada)
- [ ] Imagem `predio.png` adicionada (ou gerada)
- [ ] Imagem `praca.png` adicionada (ou gerada)
- [ ] Imagem `trafego.png` adicionada (ou gerada)
- [ ] Executado `python main_with_images.py`
- [ ] Verificado status das imagens no console

## ❓ Resolução de Problemas

### "Usando cor (coloque X.png na pasta assets/)"
**Problema**: Imagem não foi encontrada  
**Solução**: 
1. Verifique se o arquivo existe em `assets/X.png`
2. Verifique se o nome está correto (minúsculas, sem espaços)
3. Execute `python create_sample_images.py` para gerar imagens automáticas

### Imagem aparece distorcida
**Problema**: Imagem tem proporção diferente de 1:1  
**Solução**: Redimensione a imagem para 40x40 pixels usando um editor

### Imagem não aparece
**Problema**: Formato não suportado ou arquivo corrompido  
**Solução**: 
1. Converta para PNG
2. Verifique se o arquivo abre normalmente em um visualizador de imagens
3. Execute `python create_sample_images.py` e substitua a imagem problemática

## 🎨 Exemplo de Código para Criar Suas Próprias Imagens

Se você sabe programação, pode criar imagens customizadas:

```python
import pygame

pygame.init()

# Cria uma superfície de 40x40
img = pygame.Surface((40, 40))

# Pinta de azul
img.fill((0, 100, 200))

# Adiciona detalhes...
pygame.draw.circle(img, (255, 255, 0), (20, 20), 10)

# Salva
pygame.image.save(img, "assets/minha_imagem.png")

pygame.quit()
```

## 📚 Recursos Adicionais

- Tutorial Pygame: https://www.pygame.org/docs/
- Converter imagens online: https://image.online-convert.com/convert-to-png
- Redimensionar imagens: https://www.iloveimg.com/resize-image

---

**Divirta-se customizando seu sistema de navegação!** 🚗🗺️


