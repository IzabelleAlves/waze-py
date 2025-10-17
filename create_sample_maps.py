# -*- coding: utf-8 -*-
"""
Script para criar mapas de exemplo
"""

from city import City
import os

def create_small_city():
    """Cria uma cidade pequena de exemplo"""
    city = City(20, 15, "Cidade Pequena")
    
    # Cria ruas horizontais
    for x in range(20):
        city.set_cell(x, 3, City.STREET)
        city.set_cell(x, 7, City.STREET)
        city.set_cell(x, 11, City.STREET)
    
    # Cria ruas verticais
    for y in range(15):
        city.set_cell(5, y, City.STREET)
        city.set_cell(10, y, City.STREET)
        city.set_cell(15, y, City.STREET)
    
    # Adiciona casas
    city.set_cell(2, 1, City.HOUSE)
    city.set_cell(3, 1, City.HOUSE)
    city.set_cell(7, 1, City.HOUSE)
    city.set_cell(8, 1, City.HOUSE)
    city.set_cell(12, 1, City.HOUSE)
    city.set_cell(13, 1, City.HOUSE)
    city.set_cell(17, 1, City.HOUSE)
    city.set_cell(18, 1, City.HOUSE)
    
    city.set_cell(2, 5, City.HOUSE)
    city.set_cell(3, 5, City.HOUSE)
    city.set_cell(7, 5, City.HOUSE)
    city.set_cell(8, 5, City.HOUSE)
    city.set_cell(12, 5, City.HOUSE)
    city.set_cell(13, 5, City.HOUSE)
    city.set_cell(17, 5, City.HOUSE)
    city.set_cell(18, 5, City.HOUSE)
    
    city.set_cell(2, 9, City.HOUSE)
    city.set_cell(3, 9, City.HOUSE)
    city.set_cell(7, 9, City.HOUSE)
    city.set_cell(8, 9, City.HOUSE)
    city.set_cell(12, 9, City.HOUSE)
    city.set_cell(13, 9, City.HOUSE)
    city.set_cell(17, 9, City.HOUSE)
    city.set_cell(18, 9, City.HOUSE)
    
    # Adiciona prédios
    city.set_cell(6, 1, City.BUILDING)
    city.set_cell(6, 2, City.BUILDING)
    city.set_cell(11, 1, City.BUILDING)
    city.set_cell(11, 2, City.BUILDING)
    city.set_cell(16, 1, City.BUILDING)
    city.set_cell(16, 2, City.BUILDING)
    
    city.set_cell(6, 5, City.BUILDING)
    city.set_cell(6, 6, City.BUILDING)
    city.set_cell(11, 5, City.BUILDING)
    city.set_cell(11, 6, City.BUILDING)
    city.set_cell(16, 5, City.BUILDING)
    city.set_cell(16, 6, City.BUILDING)
    
    # Adiciona praças
    city.set_cell(2, 13, City.PARK)
    city.set_cell(3, 13, City.PARK)
    city.set_cell(2, 14, City.PARK)
    city.set_cell(3, 14, City.PARK)
    
    city.set_cell(12, 13, City.PARK)
    city.set_cell(13, 13, City.PARK)
    city.set_cell(12, 14, City.PARK)
    city.set_cell(13, 14, City.PARK)
    
    return city

def create_big_city():
    """Cria uma cidade grande de exemplo"""
    city = City(20, 15, "Cidade Grande")
    
    # Grid de ruas mais denso
    # Ruas horizontais
    for x in range(20):
        city.set_cell(x, 2, City.STREET)
        city.set_cell(x, 5, City.STREET)
        city.set_cell(x, 8, City.STREET)
        city.set_cell(x, 11, City.STREET)
        city.set_cell(x, 14, City.STREET)
    
    # Ruas verticais
    for y in range(15):
        city.set_cell(3, y, City.STREET)
        city.set_cell(7, y, City.STREET)
        city.set_cell(11, y, City.STREET)
        city.set_cell(15, y, City.STREET)
        city.set_cell(19, y, City.STREET)
    
    # Preenche com construções
    for y in range(15):
        for x in range(20):
            cell = city.get_cell(x, y)
            if cell != City.STREET:
                # Alterna entre casas e prédios
                if (x + y) % 3 == 0:
                    city.set_cell(x, y, City.BUILDING)
                else:
                    city.set_cell(x, y, City.HOUSE)
    
    # Adiciona algumas praças estratégicas
    city.set_cell(1, 0, City.PARK)
    city.set_cell(1, 1, City.PARK)
    city.set_cell(9, 0, City.PARK)
    city.set_cell(9, 1, City.PARK)
    city.set_cell(17, 0, City.PARK)
    city.set_cell(17, 1, City.PARK)
    
    city.set_cell(1, 12, City.PARK)
    city.set_cell(1, 13, City.PARK)
    city.set_cell(9, 12, City.PARK)
    city.set_cell(9, 13, City.PARK)
    city.set_cell(17, 12, City.PARK)
    city.set_cell(17, 13, City.PARK)
    
    return city

def create_maze_city():
    """Cria uma cidade com layout de labirinto"""
    city = City(20, 15, "Cidade Labirinto")
    
    # Cria padrão de labirinto
    # Bordas
    for x in range(20):
        city.set_cell(x, 0, City.STREET)
        city.set_cell(x, 14, City.STREET)
    
    for y in range(15):
        city.set_cell(0, y, City.STREET)
        city.set_cell(19, y, City.STREET)
    
    # Ruas internas criando labirinto
    for y in range(2, 13, 2):
        for x in range(2, 18, 2):
            city.set_cell(x, y, City.STREET)
    
    # Conectores
    city.set_cell(2, 1, City.STREET)
    city.set_cell(2, 3, City.STREET)
    city.set_cell(6, 1, City.STREET)
    city.set_cell(6, 3, City.STREET)
    city.set_cell(10, 1, City.STREET)
    city.set_cell(10, 3, City.STREET)
    city.set_cell(14, 1, City.STREET)
    city.set_cell(14, 3, City.STREET)
    city.set_cell(18, 1, City.STREET)
    city.set_cell(18, 3, City.STREET)
    
    city.set_cell(4, 5, City.STREET)
    city.set_cell(4, 7, City.STREET)
    city.set_cell(8, 5, City.STREET)
    city.set_cell(8, 7, City.STREET)
    city.set_cell(12, 5, City.STREET)
    city.set_cell(12, 7, City.STREET)
    city.set_cell(16, 5, City.STREET)
    city.set_cell(16, 7, City.STREET)
    
    city.set_cell(2, 9, City.STREET)
    city.set_cell(2, 11, City.STREET)
    city.set_cell(6, 9, City.STREET)
    city.set_cell(6, 11, City.STREET)
    city.set_cell(10, 9, City.STREET)
    city.set_cell(10, 11, City.STREET)
    city.set_cell(14, 9, City.STREET)
    city.set_cell(14, 11, City.STREET)
    city.set_cell(18, 9, City.STREET)
    city.set_cell(18, 13, City.STREET)
    
    # Preenche espaços vazios com construções
    for y in range(15):
        for x in range(20):
            cell = city.get_cell(x, y)
            if cell != City.STREET:
                if (x * y) % 5 == 0:
                    city.set_cell(x, y, City.BUILDING)
                elif (x * y) % 7 == 0:
                    city.set_cell(x, y, City.PARK)
                else:
                    city.set_cell(x, y, City.HOUSE)
    
    return city

def main():
    """Cria todos os mapas de exemplo"""
    if not os.path.exists("maps"):
        os.makedirs("maps")
    
    # Cria e salva cidade pequena
    city1 = create_small_city()
    city1.save_to_file("maps/cidade_pequena.json")
    print("Criado: maps/cidade_pequena.json")
    
    # Cria e salva cidade grande
    city2 = create_big_city()
    city2.save_to_file("maps/cidade_grande.json")
    print("Criado: maps/cidade_grande.json")
    
    # Cria e salva cidade labirinto
    city3 = create_maze_city()
    city3.save_to_file("maps/cidade_labirinto.json")
    print("Criado: maps/cidade_labirinto.json")
    
    print("\nMapas de exemplo criados com sucesso!")
    print("Use o botão 'Carregar' na aplicação para carregar cidade.json")
    print("(Renomeie um dos arquivos acima para cidade.json para testá-los)")

if __name__ == "__main__":
    main()

