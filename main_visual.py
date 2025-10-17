# -*- coding: utf-8 -*-
"""
Sistema de Navegação tipo Waze - Versão com Visual Aprimorado
Trabalho de Algoritmos e Estruturas de Dados
"""

import pygame
import sys
import os
from city import City
from pathfinding import PathFinder

# Inicializa Pygame
pygame.init()

# Constantes
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
CELL_SIZE = 40
GRID_WIDTH = 20
GRID_HEIGHT = 15

# Cores
COLOR_EMPTY = (200, 200, 200)
COLOR_STREET = (80, 80, 80)
COLOR_HOUSE = (210, 105, 30)
COLOR_BUILDING = (100, 149, 237)
COLOR_PARK = (34, 139, 34)
COLOR_TRAFFIC = (220, 20, 60)
COLOR_PATH = (255, 215, 0)
COLOR_START = (50, 205, 50)
COLOR_END = (30, 144, 255)
COLOR_GRID = (120, 120, 120)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BUTTON = (70, 130, 180)
COLOR_BUTTON_HOVER = (100, 160, 210)
COLOR_YELLOW = (255, 255, 0)

class Button:
    """Classe para botões da interface"""
    
    def __init__(self, x, y, width, height, text, color=COLOR_BUTTON):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = COLOR_BUTTON_HOVER
        self.is_hovered = False
    
    def draw(self, screen, font):
        """Desenha o botão"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, COLOR_BLACK, self.rect, 2)
        
        text_surface = font.render(self.text, True, COLOR_WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        """Trata eventos do botão"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class WazeApp:
    """Aplicação principal"""
    
    def __init__(self):
        """Inicializa a aplicação"""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Sistema de Navegação - Waze Particular (Visual)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        self.icon_font = pygame.font.Font(None, 28)  # Para ícones/símbolos
        
        # Estado da aplicação
        self.city = City(GRID_WIDTH, GRID_HEIGHT, "Minha Cidade")
        self.pathfinder = PathFinder(self.city)
        self.current_tool = City.STREET
        self.mode = "EDIT"  # EDIT ou NAVIGATE
        
        # Navegação
        self.start_pos = None
        self.end_pos = None
        self.path = None
        
        # Offset para centralizar o grid
        self.grid_offset_x = 50
        self.grid_offset_y = 100
        
        # Criar botões
        self.create_buttons()
        
        # Criar diretório para mapas
        if not os.path.exists("maps"):
            os.makedirs("maps")
    
    def create_buttons(self):
        """Cria todos os botões da interface"""
        self.buttons = []
        
        # Botões de ferramentas (modo edição)
        btn_y = 10
        btn_spacing = 85
        
        self.btn_street = Button(10, btn_y, 80, 30, "Rua")
        self.btn_house = Button(10 + btn_spacing, btn_y, 80, 30, "Casa")
        self.btn_building = Button(10 + btn_spacing * 2, btn_y, 80, 30, "Prédio")
        self.btn_park = Button(10 + btn_spacing * 3, btn_y, 80, 30, "Praça")
        self.btn_erase = Button(10 + btn_spacing * 4, btn_y, 80, 30, "Apagar")
        
        # Botões de ação
        self.btn_clear = Button(10 + btn_spacing * 5, btn_y, 80, 30, "Limpar")
        self.btn_save = Button(10 + btn_spacing * 6, btn_y, 80, 30, "Salvar")
        self.btn_load = Button(10 + btn_spacing * 7, btn_y, 80, 30, "Carregar")
        
        # Botão de modo
        self.btn_mode = Button(10 + btn_spacing * 8, btn_y, 120, 30, "Modo: Editar")
        
        # Botões de navegação
        self.btn_traffic = Button(10, btn_y + 50, 120, 30, "Gerar Tráfego")
        self.btn_clear_traffic = Button(140, btn_y + 50, 120, 30, "Limpar Tráfego")
        self.btn_find_path = Button(270, btn_y + 50, 120, 30, "Traçar Rota")
        self.btn_clear_route = Button(400, btn_y + 50, 120, 30, "Limpar Rota")
        
        self.buttons = [
            self.btn_street, self.btn_house, self.btn_building, self.btn_park,
            self.btn_erase, self.btn_clear, self.btn_save, self.btn_load,
            self.btn_mode, self.btn_traffic, self.btn_clear_traffic,
            self.btn_find_path, self.btn_clear_route
        ]
    
    def get_cell_from_mouse(self, mouse_pos):
        """Converte posição do mouse para célula do grid"""
        mx, my = mouse_pos
        x = (mx - self.grid_offset_x) // CELL_SIZE
        y = (my - self.grid_offset_y) // CELL_SIZE
        
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            return [x, y]
        return None
    
    def draw_cell_icon(self, x, y, cell_type):
        """Desenha ícone/símbolo na célula"""
        center_x = self.grid_offset_x + x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.grid_offset_y + y * CELL_SIZE + CELL_SIZE // 2
        
        if cell_type == City.HOUSE:
            # Desenha casa simplificada
            # Telhado (triângulo)
            points = [
                (center_x, center_y - 12),
                (center_x - 10, center_y - 2),
                (center_x + 10, center_y - 2)
            ]
            pygame.draw.polygon(self.screen, COLOR_BLACK, points)
            # Corpo da casa (retângulo)
            house_rect = pygame.Rect(center_x - 8, center_y - 2, 16, 12)
            pygame.draw.rect(self.screen, COLOR_BLACK, house_rect, 2)
            # Porta
            door_rect = pygame.Rect(center_x - 3, center_y + 3, 6, 7)
            pygame.draw.rect(self.screen, COLOR_BLACK, door_rect)
            
        elif cell_type == City.BUILDING:
            # Desenha prédio simplificado
            # Corpo principal
            building_rect = pygame.Rect(center_x - 10, center_y - 10, 20, 20)
            pygame.draw.rect(self.screen, COLOR_BLACK, building_rect, 2)
            # Janelas (grid 2x3)
            for wy in range(3):
                for wx in range(2):
                    window_x = center_x - 7 + wx * 8
                    window_y = center_y - 8 + wy * 6
                    window_rect = pygame.Rect(window_x, window_y, 4, 4)
                    pygame.draw.rect(self.screen, COLOR_BLACK, window_rect)
            
        elif cell_type == City.PARK:
            # Desenha árvore simplificada
            # Copa (círculo verde escuro)
            pygame.draw.circle(self.screen, (0, 100, 0), (center_x, center_y - 5), 8)
            # Tronco
            trunk_rect = pygame.Rect(center_x - 2, center_y + 3, 4, 8)
            pygame.draw.rect(self.screen, (101, 67, 33), trunk_rect)
            
        elif cell_type == City.TRAFFIC:
            # Desenha símbolo de trânsito
            # X vermelho
            pygame.draw.line(self.screen, (139, 0, 0), 
                           (center_x - 8, center_y - 8), 
                           (center_x + 8, center_y + 8), 4)
            pygame.draw.line(self.screen, (139, 0, 0), 
                           (center_x + 8, center_y - 8), 
                           (center_x - 8, center_y + 8), 4)
            # Círculo ao redor
            pygame.draw.circle(self.screen, (139, 0, 0), (center_x, center_y), 12, 2)
    
    def draw_grid(self):
        """Desenha o grid da cidade"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                cell_type = self.city.get_cell(x, y)
                
                # Determina cor baseado no tipo
                color = COLOR_EMPTY
                if cell_type == City.STREET:
                    color = COLOR_STREET
                elif cell_type == City.HOUSE:
                    color = COLOR_HOUSE
                elif cell_type == City.BUILDING:
                    color = COLOR_BUILDING
                elif cell_type == City.PARK:
                    color = COLOR_PARK
                elif cell_type == City.TRAFFIC:
                    color = COLOR_TRAFFIC
                
                # Desenha célula
                rect = pygame.Rect(
                    self.grid_offset_x + x * CELL_SIZE,
                    self.grid_offset_y + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, COLOR_GRID, rect, 1)
                
                # Adiciona textura de rua
                if cell_type == City.STREET:
                    # Linha tracejada amarela no meio da rua
                    center_x = self.grid_offset_x + x * CELL_SIZE + CELL_SIZE // 2
                    center_y = self.grid_offset_y + y * CELL_SIZE + CELL_SIZE // 2
                    
                    # Linha horizontal tracejada
                    for i in range(3):
                        dash_x = center_x - 10 + i * 10
                        pygame.draw.line(self.screen, COLOR_YELLOW,
                                       (dash_x, center_y), (dash_x + 5, center_y), 1)
                
                # Desenha ícones para construções
                if cell_type in [City.HOUSE, City.BUILDING, City.PARK, City.TRAFFIC]:
                    self.draw_cell_icon(x, y, cell_type)
        
        # Desenha caminho se existe
        if self.path is not None:
            for i in range(len(self.path)):
                pos = self.path[i]
                x, y = pos[0], pos[1]
                
                # Não desenha sobre start e end
                is_start = self.start_pos and x == self.start_pos[0] and y == self.start_pos[1]
                is_end = self.end_pos and x == self.end_pos[0] and y == self.end_pos[1]
                
                if not is_start and not is_end:
                    center_x = self.grid_offset_x + x * CELL_SIZE + CELL_SIZE // 2
                    center_y = self.grid_offset_y + y * CELL_SIZE + CELL_SIZE // 2
                    
                    # Desenha círculo no caminho
                    pygame.draw.circle(self.screen, COLOR_PATH, (center_x, center_y), 8)
                    
                    # Desenha seta indicando direção se não for o último
                    if i < len(self.path) - 1:
                        next_pos = self.path[i + 1]
                        next_x, next_y = next_pos[0], next_pos[1]
                        
                        # Calcula direção
                        dx = next_x - x
                        dy = next_y - y
                        
                        # Desenha seta pequena
                        arrow_size = 6
                        if dx > 0:  # Direita
                            pygame.draw.polygon(self.screen, COLOR_BLACK, [
                                (center_x + arrow_size, center_y),
                                (center_x, center_y - 3),
                                (center_x, center_y + 3)
                            ])
                        elif dx < 0:  # Esquerda
                            pygame.draw.polygon(self.screen, COLOR_BLACK, [
                                (center_x - arrow_size, center_y),
                                (center_x, center_y - 3),
                                (center_x, center_y + 3)
                            ])
                        elif dy > 0:  # Baixo
                            pygame.draw.polygon(self.screen, COLOR_BLACK, [
                                (center_x, center_y + arrow_size),
                                (center_x - 3, center_y),
                                (center_x + 3, center_y)
                            ])
                        elif dy < 0:  # Cima
                            pygame.draw.polygon(self.screen, COLOR_BLACK, [
                                (center_x, center_y - arrow_size),
                                (center_x - 3, center_y),
                                (center_x + 3, center_y)
                            ])
        
        # Desenha ponto de partida
        if self.start_pos is not None:
            x, y = self.start_pos[0], self.start_pos[1]
            rect = pygame.Rect(
                self.grid_offset_x + x * CELL_SIZE,
                self.grid_offset_y + y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(self.screen, COLOR_START, rect)
            pygame.draw.rect(self.screen, COLOR_BLACK, rect, 3)
            
            # Desenha "A"
            text = self.font.render("A", True, COLOR_BLACK)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
        
        # Desenha ponto de chegada
        if self.end_pos is not None:
            x, y = self.end_pos[0], self.end_pos[1]
            rect = pygame.Rect(
                self.grid_offset_x + x * CELL_SIZE,
                self.grid_offset_y + y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(self.screen, COLOR_END, rect)
            pygame.draw.rect(self.screen, COLOR_BLACK, rect, 3)
            
            # Desenha "B"
            text = self.font.render("B", True, COLOR_WHITE)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
    
    def draw_ui(self):
        """Desenha interface do usuário"""
        # Desenha botões
        for button in self.buttons:
            button.draw(self.screen, self.small_font)
        
        # Destaca ferramenta atual no modo edição
        if self.mode == "EDIT":
            if self.current_tool == City.STREET:
                pygame.draw.rect(self.screen, COLOR_WHITE, self.btn_street.rect, 3)
            elif self.current_tool == City.HOUSE:
                pygame.draw.rect(self.screen, COLOR_WHITE, self.btn_house.rect, 3)
            elif self.current_tool == City.BUILDING:
                pygame.draw.rect(self.screen, COLOR_WHITE, self.btn_building.rect, 3)
            elif self.current_tool == City.PARK:
                pygame.draw.rect(self.screen, COLOR_WHITE, self.btn_park.rect, 3)
            elif self.current_tool == City.EMPTY:
                pygame.draw.rect(self.screen, COLOR_WHITE, self.btn_erase.rect, 3)
        
        # Informações da rota
        if self.path is not None and self.start_pos and self.end_pos:
            info_y = 50
            path_length = len(self.path)
            info_text = f"Rota: {path_length} células | A({self.start_pos[0]},{self.start_pos[1]}) → B({self.end_pos[0]},{self.end_pos[1]})"
            text = self.small_font.render(info_text, True, COLOR_BLACK)
            self.screen.blit(text, (530, info_y))
        
        # Instruções
        y_pos = WINDOW_HEIGHT - 80
        
        if self.mode == "EDIT":
            instructions = [
                "MODO EDIÇÃO - Clique no mapa para colocar elementos",
                "Use os botões para escolher: Rua, Casa, Prédio, Praça ou Apagar"
            ]
        else:
            instructions = [
                "MODO NAVEGAÇÃO - Clique em uma RUA para definir:",
                "Primeiro clique = Ponto A (partida) | Segundo clique = Ponto B (chegada)"
            ]
        
        for i in range(len(instructions)):
            text = self.small_font.render(instructions[i], True, COLOR_BLACK)
            self.screen.blit(text, (10, y_pos + i * 25))
    
    def handle_events(self):
        """Trata eventos"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Eventos de botões
            for button in self.buttons:
                button.handle_event(event)
            
            # Cliques em botões
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Botões de ferramentas
                if self.btn_street.handle_event(event):
                    self.current_tool = City.STREET
                    self.mode = "EDIT"
                elif self.btn_house.handle_event(event):
                    self.current_tool = City.HOUSE
                    self.mode = "EDIT"
                elif self.btn_building.handle_event(event):
                    self.current_tool = City.BUILDING
                    self.mode = "EDIT"
                elif self.btn_park.handle_event(event):
                    self.current_tool = City.PARK
                    self.mode = "EDIT"
                elif self.btn_erase.handle_event(event):
                    self.current_tool = City.EMPTY
                    self.mode = "EDIT"
                
                # Botões de ação
                elif self.btn_clear.handle_event(event):
                    self.city.clear()
                    self.start_pos = None
                    self.end_pos = None
                    self.path = None
                
                elif self.btn_save.handle_event(event):
                    filename = "maps/cidade.json"
                    self.city.save_to_file(filename)
                    print(f"Mapa salvo em {filename}")
                
                elif self.btn_load.handle_event(event):
                    filename = "maps/cidade.json"
                    loaded_city = City.load_from_file(filename)
                    if loaded_city:
                        self.city = loaded_city
                        self.pathfinder = PathFinder(self.city)
                        self.start_pos = None
                        self.end_pos = None
                        self.path = None
                        print(f"Mapa carregado de {filename}")
                
                elif self.btn_mode.handle_event(event):
                    if self.mode == "EDIT":
                        self.mode = "NAVIGATE"
                        self.btn_mode.text = "Modo: Navegar"
                    else:
                        self.mode = "EDIT"
                        self.btn_mode.text = "Modo: Editar"
                
                elif self.btn_traffic.handle_event(event):
                    self.city.generate_random_traffic(5)
                    # Recalcula rota se já existe
                    if self.start_pos and self.end_pos:
                        self.path = self.pathfinder.find_path(self.start_pos, self.end_pos)
                
                elif self.btn_clear_traffic.handle_event(event):
                    self.city.clear_all_traffic()
                    # Recalcula rota se já existe
                    if self.start_pos and self.end_pos:
                        self.path = self.pathfinder.find_path(self.start_pos, self.end_pos)
                
                elif self.btn_find_path.handle_event(event):
                    if self.start_pos and self.end_pos:
                        self.path = self.pathfinder.find_path(self.start_pos, self.end_pos)
                        if self.path is None:
                            print("Nenhum caminho encontrado!")
                
                elif self.btn_clear_route.handle_event(event):
                    self.start_pos = None
                    self.end_pos = None
                    self.path = None
                
                # Clique no grid
                else:
                    cell = self.get_cell_from_mouse(event.pos)
                    if cell is not None:
                        x, y = cell[0], cell[1]
                        
                        if self.mode == "EDIT":
                            # Modo edição - coloca elemento
                            self.city.set_cell(x, y, self.current_tool)
                        else:
                            # Modo navegação - define start/end
                            if self.city.is_walkable(x, y):
                                if self.start_pos is None:
                                    self.start_pos = cell
                                    self.end_pos = None
                                    self.path = None
                                elif self.end_pos is None:
                                    self.end_pos = cell
                                    # Calcula caminho automaticamente
                                    self.path = self.pathfinder.find_path(self.start_pos, self.end_pos)
                                    if self.path is None:
                                        print("Nenhum caminho encontrado!")
                                else:
                                    # Reinicia
                                    self.start_pos = cell
                                    self.end_pos = None
                                    self.path = None
            
            # Desenhar enquanto arrasta (modo edição)
            if event.type == pygame.MOUSEMOTION and self.mode == "EDIT":
                if pygame.mouse.get_pressed()[0]:  # Botão esquerdo pressionado
                    cell = self.get_cell_from_mouse(event.pos)
                    if cell is not None:
                        x, y = cell[0], cell[1]
                        self.city.set_cell(x, y, self.current_tool)
        
        return True
    
    def run(self):
        """Loop principal"""
        running = True
        while running:
            running = self.handle_events()
            
            # Desenha
            self.screen.fill(COLOR_WHITE)
            self.draw_grid()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

def main():
    """Função principal"""
    app = WazeApp()
    app.run()

if __name__ == "__main__":
    main()

