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

# Cores (fallback caso imagens não carreguem)
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

class Message:
    
    def __init__(self, text, duration=3000, msg_type="info"):
        self.text = text
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
        self.msg_type = msg_type
        self.active = True

        if msg_type == "success":
            self.bg_color = (46, 125, 50)  # Verde
            self.text_color = COLOR_WHITE
        elif msg_type == "error":
            self.bg_color = (211, 47, 47)  # Vermelho
            self.text_color = COLOR_WHITE
        elif msg_type == "warning":
            self.bg_color = (255, 152, 0)  # Laranja
            self.text_color = COLOR_BLACK
        else: 
            self.bg_color = (33, 150, 243)  # Azul
            self.text_color = COLOR_WHITE
    
    def update(self):
        """Atualiza o estado da mensagem"""
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.active = False
        return self.active
    
    def draw(self, screen, font, y_position):
        """Desenha a mensagem na tela"""
        if not self.active:
            return
        
        # Calcula tempo restante para fade out
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        remaining = self.duration - elapsed
        
        # Efeito de fade out nos últimos 500ms
        alpha = 255
        if remaining < 500:
            alpha = int((remaining / 500) * 255)
        
        # Renderiza o texto
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        
        # Dimensões do pop-up
        padding = 20
        popup_width = text_rect.width + padding * 2
        popup_height = text_rect.height + padding
        popup_x = (screen.get_width() - popup_width) // 2
        popup_y = y_position
        
        # Cria superfície com transparência
        popup_surface = pygame.Surface((popup_width, popup_height))
        popup_surface.set_alpha(alpha)
        popup_surface.fill(self.bg_color)
        
        # Desenha sombra
        shadow_surface = pygame.Surface((popup_width + 4, popup_height + 4))
        shadow_surface.set_alpha(alpha // 3)
        shadow_surface.fill((0, 0, 0))
        screen.blit(shadow_surface, (popup_x + 2, popup_y + 2))
        
        # Desenha popup
        screen.blit(popup_surface, (popup_x, popup_y))
        
        # Desenha borda
        border_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        pygame.draw.rect(border_surface, (*COLOR_BLACK, alpha), 
                        (0, 0, popup_width, popup_height), 3)
        screen.blit(border_surface, (popup_x, popup_y))
        
        # Desenha texto
        text_with_alpha = pygame.Surface(text_rect.size, pygame.SRCALPHA)
        text_surface.set_alpha(alpha)
        screen.blit(text_surface, (popup_x + padding, popup_y + padding // 2))

class ImageLoader:
    
    def __init__(self, cell_size):
        """Inicializa o carregador de imagens"""
        self.cell_size = cell_size
        self.images = {}
        self.assets_dir = "assets"
        
        # Cria diretório de assets se não existir
        if not os.path.exists(self.assets_dir):
            os.makedirs(self.assets_dir)
        
        # Mapeamento de tipos para nomes de arquivo
        self.image_files = {
            City.STREET: "street.png",
            City.HOUSE: "casa.png",
            City.BUILDING: "predio.png",
            City.PARK: "praca.png",
            City.TRAFFIC: "trafego.png"
        }
        
        # Carrega todas as imagens
        self.load_images()
    
    def load_images(self):
        """Carrega todas as imagens disponíveis"""
        for cell_type, filename in self.image_files.items():
            filepath = os.path.join(self.assets_dir, filename)
            
            if os.path.exists(filepath):
                try:
                    # Carrega e redimensiona a imagem
                    image = pygame.image.load(filepath)
                    image = pygame.transform.scale(image, (self.cell_size, self.cell_size))
                    self.images[cell_type] = image
                    print(f"Imagem carregada: {filename}")
                except Exception as e:
                    print(f"Erro ao carregar {filename}: {e}")
                    self.images[cell_type] = None
            else:
                self.images[cell_type] = None
    
    def get_image(self, cell_type):
        """Retorna a imagem para um tipo de célula"""
        return self.images.get(cell_type, None)
    
    def has_image(self, cell_type):
        """Verifica se há imagem para um tipo de célula"""
        return cell_type in self.images and self.images[cell_type] is not None

class Button:
    
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
    
    def __init__(self):
        """Inicializa a aplicação"""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Sistema de Navegação - Waze com Imagens")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        
        # Carregador de imagens
        self.image_loader = ImageLoader(CELL_SIZE)
        
        # Estado da aplicação
        self.city = City(GRID_WIDTH, GRID_HEIGHT, "Minha Cidade")
        self.pathfinder = PathFinder(self.city)
        self.current_tool = City.STREET
        self.mode = "EDIT" 
        
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
        
        # Sistema de mensagens
        self.messages = []
        
        # Mostra status das imagens
        self.print_image_status()
    
    def add_message(self, text, msg_type="info", duration=3000):
        """Adiciona uma nova mensagem à tela"""
        self.messages.append(Message(text, duration, msg_type))
    
    def print_image_status(self):
        """Imprime o status do carregamento de imagens"""
        print("\n" + "=" * 50)
        print("STATUS DAS IMAGENS")
        print("=" * 50)
        
        image_names = {
            City.STREET: "Rua",
            City.HOUSE: "Casa",
            City.BUILDING: "Prédio",
            City.PARK: "Praça",
            City.TRAFFIC: "Tráfego"
        }
        
        for cell_type, name in image_names.items():
            if self.image_loader.has_image(cell_type):
                print(f"[OK] {name}: Imagem carregada")
            else:
                filename = self.image_loader.image_files[cell_type]
                print(f"[--] {name}: Usando cor (coloque {filename} na pasta assets/)")
        
        print("=" * 50 + "\n")
    
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
    
    def draw_cell_with_color(self, rect, cell_type):
        """Desenha célula com cor (fallback)"""
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
        
        pygame.draw.rect(self.screen, color, rect)
        
        # Adiciona textura de rua
        if cell_type == City.STREET:
            center_x = rect.centerx
            center_y = rect.centery
            for i in range(3):
                dash_x = center_x - 10 + i * 10
                pygame.draw.line(self.screen, COLOR_YELLOW,
                               (dash_x, center_y), (dash_x + 5, center_y), 1)
    
    def draw_grid(self):
        """Desenha o grid da cidade"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                cell_type = self.city.get_cell(x, y)
                
                # Cria retângulo da célula
                rect = pygame.Rect(
                    self.grid_offset_x + x * CELL_SIZE,
                    self.grid_offset_y + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
                
                # Tenta desenhar com imagem, senão usa cor
                image = self.image_loader.get_image(cell_type)
                if image:
                    self.screen.blit(image, rect)
                else:
                    self.draw_cell_with_color(rect, cell_type)
                
                # Desenha borda do grid
                pygame.draw.rect(self.screen, COLOR_GRID, rect, 1)
        
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
                    pygame.draw.circle(self.screen, COLOR_BLACK, (center_x, center_y), 8, 2)
                    
                    # Desenha seta indicando direção se não for o último
                    if i < len(self.path) - 1:
                        next_pos = self.path[i + 1]
                        next_x, next_y = next_pos[0], next_pos[1]
                        
                        # Calcula direção
                        dx = next_x - x
                        dy = next_y - y
                        
                        # Desenha seta pequena
                        arrow_size = 5
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
            
            # Overlay semi-transparente verde
            s = pygame.Surface((CELL_SIZE, CELL_SIZE))
            s.set_alpha(180)
            s.fill(COLOR_START)
            self.screen.blit(s, rect)
            
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
            
            # Overlay semi-transparente azul
            s = pygame.Surface((CELL_SIZE, CELL_SIZE))
            s.set_alpha(180)
            s.fill(COLOR_END)
            self.screen.blit(s, rect)
            
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
            info_text = f"Rota: {path_length} metros | A({self.start_pos[0]},{self.start_pos[1]}) -> B({self.end_pos[0]},{self.end_pos[1]})"
            text = self.small_font.render(info_text, True, COLOR_BLACK)
            self.screen.blit(text, (530, info_y))
        
        # Instruções
        y_pos = WINDOW_HEIGHT - 80
        
        if self.mode == "EDIT":
            instructions = [
                "MODO EDICAO - Clique no mapa para colocar elementos",
                "Use os botoes para escolher: Rua, Casa, Predio, Praca ou Apagar"
            ]
        else:
            instructions = [
                "MODO NAVEGACAO - Clique em uma RUA para definir:",
                "Primeiro clique = Ponto A (partida) | Segundo clique = Ponto B (chegada)"
            ]
        
        for i in range(len(instructions)):
            text = self.small_font.render(instructions[i], True, COLOR_BLACK)
            self.screen.blit(text, (10, y_pos + i * 25))
        
        # Desenha mensagens (pop-ups)
        self.draw_messages()
    
    def draw_messages(self):
        """Desenha todas as mensagens ativas"""
        # Remove mensagens inativas
        self.messages = [msg for msg in self.messages if msg.update()]
        
        # Desenha mensagens ativas (de baixo para cima)
        y_start = 150
        spacing = 10
        
        for i in range(len(self.messages)):
            msg = self.messages[i]
            y_pos = y_start + i * (50 + spacing)
            msg.draw(self.screen, self.font, y_pos)
    
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
                    self.add_message("Mapa limpo com sucesso!", "success")
                
                elif self.btn_save.handle_event(event):
                    filename = "maps/cidade.json"
                    self.city.save_to_file(filename)
                    print(f"Mapa salvo em {filename}")
                    self.add_message("Mapa salvo com sucesso!", "success")
                
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
                        self.add_message(f"Mapa '{loaded_city.name}' carregado!", "success")
                    else:
                        self.add_message("Erro ao carregar mapa!", "error")
                
                elif self.btn_mode.handle_event(event):
                    if self.mode == "EDIT":
                        self.mode = "NAVIGATE"
                        self.btn_mode.text = "Modo: Navegar"
                        self.add_message("Modo Navegacao ativado", "info")
                    else:
                        self.mode = "EDIT"
                        self.btn_mode.text = "Modo: Editar"
                        self.add_message("Modo Edicao ativado", "info")
                
                elif self.btn_traffic.handle_event(event):
                    self.city.generate_random_traffic(5)
                    self.add_message("Engarrafamentos gerados!", "warning")
                    # Recalcula rota se já existe
                    if self.start_pos and self.end_pos:
                        old_path_length = len(self.path) if self.path else 0
                        self.path = self.pathfinder.find_path(self.start_pos, self.end_pos)
                        if self.path:
                            new_path_length = len(self.path)
                            if new_path_length != old_path_length:
                                self.add_message("Rota alternativa calculada!", "info", 2000)
                        else:
                            self.add_message("Nenhum caminho disponivel!", "error")
                
                elif self.btn_clear_traffic.handle_event(event):
                    self.city.clear_all_traffic()
                    self.add_message("Trafego limpo!", "success")
                    # Recalcula rota se já existe
                    if self.start_pos and self.end_pos:
                        self.path = self.pathfinder.find_path(self.start_pos, self.end_pos)
                        if self.path:
                            self.add_message("Rota recalculada!", "info", 2000)
                
                elif self.btn_find_path.handle_event(event):
                    if self.start_pos and self.end_pos:
                        self.path = self.pathfinder.find_path(self.start_pos, self.end_pos)
                        if self.path is None:
                            print("Nenhum caminho encontrado!")
                            self.add_message("Nenhum caminho encontrado!", "error", 4000)
                        else:
                            self.add_message(f"Rota encontrada: {len(self.path)} metros", "success")
                    else:
                        self.add_message("Defina os pontos A e B primeiro!", "warning")
                
                elif self.btn_clear_route.handle_event(event):
                    self.start_pos = None
                    self.end_pos = None
                    self.path = None
                    self.add_message("Rota limpa!", "info")
                
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
                                    self.add_message("Ponto A definido!", "success", 2000)
                                elif self.end_pos is None:
                                    self.end_pos = cell
                                    # Calcula caminho automaticamente
                                    self.path = self.pathfinder.find_path(self.start_pos, self.end_pos)
                                    if self.path is None:
                                        print("Nenhum caminho encontrado!")
                                        self.add_message("Nenhum caminho encontrado!", "error", 4000)
                                    else:
                                        self.add_message(f"Rota calculada: {len(self.path)} metros", "success", 3000)
                                else:
                                    # Reinicia
                                    self.start_pos = cell
                                    self.end_pos = None
                                    self.path = None
                                    self.add_message("Ponto A redefinido!", "info", 2000)
                            else:
                                self.add_message("Clique apenas em RUAS!", "warning", 2500)
            
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
    app = WazeApp()
    app.run()

if __name__ == "__main__":
    main()


