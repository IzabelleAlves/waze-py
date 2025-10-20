# -*- coding: utf-8 -*-
"""
Classe City - Representa uma cidade com seu mapa bidimensional
"""

import json

class City:

    EMPTY = 0
    STREET = 1
    HOUSE = 2
    BUILDING = 3
    PARK = 4
    TRAFFIC = 5  
    
    CELL_NAMES = {
        0: "Vazio",
        1: "Rua",
        2: "Casa",
        3: "Prédio",
        4: "Praça",
        5: "Engarrafamento"
    }
    
    def __init__(self, width, height, name="Cidade"):
        self.width = width
        self.height = height
        self.name = name
        
        self.grid = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(self.EMPTY)
            self.grid.append(row)
        
        self.traffic_positions = []
    
    def set_cell(self, x, y, cell_type):
        if 0 <= y < self.height and 0 <= x < self.width:
            self.grid[y][x] = cell_type
            return True
        return False
    
    def get_cell(self, x, y):
        """Obtém o tipo de uma célula"""
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.grid[y][x]
        return None
    
    def is_walkable(self, x, y):
        """Verifica se uma célula é transitável (rua)"""
        if 0 <= y < self.height and 0 <= x < self.width:
            cell_type = self.grid[y][x]
            return cell_type == self.STREET
        return False
    
    def add_traffic(self, x, y):
        """Adiciona engarrafamento em uma posição"""
        if self.get_cell(x, y) == self.STREET:
            self.set_cell(x, y, self.TRAFFIC)

            pos = [x, y]
            self.traffic_positions.append(pos)
            return True
        return False
    
    def remove_traffic(self, x, y):
        """Remove engarrafamento de uma posição"""
        if self.get_cell(x, y) == self.TRAFFIC:
            self.set_cell(x, y, self.STREET)
            i = 0
            while i < len(self.traffic_positions):
                pos = self.traffic_positions[i]
                if pos[0] == x and pos[1] == y:
                    new_traffic = []
                    for j in range(len(self.traffic_positions)):
                        if j != i:
                            new_traffic.append(self.traffic_positions[j])
                    self.traffic_positions = new_traffic
                    break
                i += 1
            return True
        return False
    
    def clear_all_traffic(self):
        """Remove todos os engarrafamentos"""
        for i in range(len(self.traffic_positions)):
            pos = self.traffic_positions[i]
            x, y = pos[0], pos[1]
            if self.get_cell(x, y) == self.TRAFFIC:
                self.set_cell(x, y, self.STREET)
        
        self.traffic_positions = []
    
    def generate_random_traffic(self, num_traffic):
        import random
        
        # Primeiro limpa tráfego existente
        self.clear_all_traffic()
        
        # Encontra todas as posições de ruas usando arrays clássicos
        street_positions = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == self.STREET:
                    street_positions.append([x, y])
        
        count = 0
        attempts = 0
        max_attempts = num_traffic * 10
        
        while count < num_traffic and attempts < max_attempts:
            if len(street_positions) > 0:
                idx = random.randint(0, len(street_positions) - 1)
                pos = street_positions[idx]
                x, y = pos[0], pos[1]
                
                if self.add_traffic(x, y):
                    count += 1
            
            attempts += 1
    
    def clear(self):
        """Limpa o mapa inteiro"""
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = self.EMPTY
        self.clear_all_traffic()
    
    def save_to_file(self, filename):
        data = {
            'name': self.name,
            'width': self.width,
            'height': self.height,
            'grid': self.grid
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        return True
    
    @staticmethod
    def load_from_file(filename):
        """Carrega um mapa de arquivo JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            city = City(data['width'], data['height'], data['name'])
            city.grid = data['grid']
            
            return city
        except Exception as e:
            print(f"Erro ao carregar arquivo: {e}")
            return None

