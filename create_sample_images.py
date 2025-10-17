# -*- coding: utf-8 -*-
"""
Script para criar imagens de exemplo simples usando Pygame
Caso você não tenha imagens prontas, este script cria imagens básicas
"""

import pygame
import os

# Tamanho das imagens
SIZE = 40

def create_street_image(size):
    """Cria imagem de rua"""
    surface = pygame.Surface((size, size))
    # Cinza escuro - apenas cor sólida, sem tracejados
    surface.fill((80, 80, 80))
    
    return surface

def create_house_image(size):
    """Cria imagem de casa"""
    surface = pygame.Surface((size, size))
    surface.fill((210, 105, 30))  # Marrom
    
    # Telhado (triângulo vermelho)
    red = (180, 50, 50)
    pygame.draw.polygon(surface, red, [
        (size // 2, 5),
        (5, size // 2 - 5),
        (size - 5, size // 2 - 5)
    ])
    
    # Parede (retângulo bege)
    beige = (245, 222, 179)
    pygame.draw.rect(surface, beige, (8, size // 2 - 5, size - 16, size // 2))
    
    # Porta (retângulo marrom escuro)
    dark_brown = (101, 67, 33)
    door_width = 8
    door_height = 12
    door_x = size // 2 - door_width // 2
    door_y = size - 8
    pygame.draw.rect(surface, dark_brown, (door_x, door_y, door_width, door_height))
    
    # Janela
    window_color = (135, 206, 235)  # Azul claro
    pygame.draw.rect(surface, window_color, (10, size // 2, 6, 6))
    pygame.draw.rect(surface, window_color, (size - 16, size // 2, 6, 6))
    
    return surface

def create_building_image(size):
    """Cria imagem de prédio"""
    surface = pygame.Surface((size, size))
    surface.fill((100, 149, 237))  # Azul claro
    
    # Corpo do prédio (cinza)
    gray = (150, 150, 180)
    pygame.draw.rect(surface, gray, (5, 5, size - 10, size - 10))
    
    # Janelas (grid 3x4)
    window_color = (255, 255, 200)  # Amarelo claro
    for row in range(4):
        for col in range(3):
            x = 8 + col * 9
            y = 7 + row * 7
            pygame.draw.rect(surface, window_color, (x, y, 5, 5))
    
    # Borda preta
    pygame.draw.rect(surface, (0, 0, 0), (5, 5, size - 10, size - 10), 2)
    
    return surface

def create_park_image(size):
    """Cria imagem de praça/parque"""
    surface = pygame.Surface((size, size))
    surface.fill((34, 139, 34))  # Verde
    
    # Grama mais clara
    light_green = (50, 205, 50)
    surface.fill(light_green)
    
    # Árvores (círculos verdes escuros)
    dark_green = (0, 100, 0)
    pygame.draw.circle(surface, dark_green, (12, 12), 6)
    pygame.draw.circle(surface, dark_green, (size - 12, 12), 6)
    pygame.draw.circle(surface, dark_green, (12, size - 12), 6)
    pygame.draw.circle(surface, dark_green, (size - 12, size - 12), 6)
    
    # Troncos (pequenos retângulos marrons)
    brown = (101, 67, 33)
    pygame.draw.rect(surface, brown, (10, 15, 4, 6))
    pygame.draw.rect(surface, brown, (size - 14, 15, 4, 6))
    pygame.draw.rect(surface, brown, (10, size - 15, 4, 6))
    pygame.draw.rect(surface, brown, (size - 14, size - 15, 4, 6))
    
    return surface

def create_traffic_image(size):
    """Cria imagem de tráfego/engarrafamento"""
    surface = pygame.Surface((size, size))
    # Fundo de rua
    surface.fill((80, 80, 80))
    
    # Símbolo de alerta (triângulo vermelho com X)
    red = (220, 20, 60)
    
    # Triângulo de alerta
    pygame.draw.polygon(surface, red, [
        (size // 2, 8),
        (8, size - 8),
        (size - 8, size - 8)
    ])
    
    # Borda preta do triângulo
    pygame.draw.polygon(surface, (0, 0, 0), [
        (size // 2, 8),
        (8, size - 8),
        (size - 8, size - 8)
    ], 2)
    
    # X preto dentro
    black = (0, 0, 0)
    center_x = size // 2
    center_y = size // 2 + 3
    pygame.draw.line(surface, black, 
                    (center_x - 6, center_y - 6), 
                    (center_x + 6, center_y + 6), 3)
    pygame.draw.line(surface, black, 
                    (center_x + 6, center_y - 6), 
                    (center_x - 6, center_y + 6), 3)
    
    return surface

def main():
    """Cria todas as imagens de exemplo"""
    pygame.init()
    
    # Cria diretório assets
    if not os.path.exists("assets"):
        os.makedirs("assets")
        print("Pasta 'assets' criada.")
    
    print("\nCriando imagens de exemplo...")
    print("=" * 50)
    
    # Cria cada imagem
    images = {
        "street.png": create_street_image(SIZE),
        "casa.png": create_house_image(SIZE),
        "predio.png": create_building_image(SIZE),
        "praca.png": create_park_image(SIZE),
        "trafego.png": create_traffic_image(SIZE)
    }
    
    # Salva as imagens
    for filename, surface in images.items():
        filepath = os.path.join("assets", filename)
        pygame.image.save(surface, filepath)
        print(f"[OK] Criada: {filepath}")
    
    print("=" * 50)
    print("\nImagens criadas com sucesso!")
    print("\nVoce pode substituir estas imagens por suas proprias imagens.")
    print("Coloque arquivos PNG de 40x40 pixels na pasta 'assets/' com os nomes:")
    print("  - street.png")
    print("  - casa.png")
    print("  - predio.png")
    print("  - praca.png")
    print("  - trafego.png")
    print("\nExecute 'python main_with_images.py' para ver o resultado!")
    
    pygame.quit()

if __name__ == "__main__":
    main()


