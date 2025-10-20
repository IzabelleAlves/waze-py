class PathFinder:
    def __init__(self, city):
        self.city = city
    
    def heuristic(self, pos1, pos2):
        x1, y1 = pos1[0], pos1[1]
        x2, y2 = pos2[0], pos2[1]
        return abs(x1 - x2) + abs(y1 - y2)
    
    def get_neighbors(self, pos):
        """Retorna vizinhos válidos de uma posição (4-direções)"""
        x, y = pos[0], pos[1]
        neighbors = []
        
        # Direções: cima, direita, baixo, esquerda
        directions = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        
        for i in range(len(directions)):
            direction = directions[i]
            dx, dy = direction[0], direction[1]
            new_x = x + dx
            new_y = y + dy
            
            # Verifica se é transitável (rua)
            if self.city.is_walkable(new_x, new_y):
                neighbors.append([new_x, new_y])
        
        return neighbors
    
    def find_path(self, start, end):
        
        # Verifica se start e end são válidos
        if not self.city.is_walkable(start[0], start[1]):
            return None
        if not self.city.is_walkable(end[0], end[1]):
            return None
        
        # Arrays para A* 
        open_list = [] 
        closed_list = [] 
        
        # Dicionários implementados como arrays de pares [key, value]
        g_score = []  # Custo do início até o nó
        f_score = []  # g_score + heurística
        came_from = []  # Para reconstruir o caminho
        
        # Funções auxiliares para trabalhar com "dicionários" como arrays
        def set_score(score_array, pos, value):
            """Define valor no array de scores"""
            key = str(pos[0]) + "," + str(pos[1])
            # Procura se já existe
            for i in range(len(score_array)):
                if score_array[i][0] == key:
                    score_array[i][1] = value
                    return
            # Se não existe, adiciona
            score_array.append([key, value])
        
        def get_score(score_array, pos, default=999999):
            """Obtém valor do array de scores"""
            key = str(pos[0]) + "," + str(pos[1])
            for i in range(len(score_array)):
                if score_array[i][0] == key:
                    return score_array[i][1]
            return default
        
        def set_came_from(pos, from_pos):
            """Define de onde veio"""
            key = str(pos[0]) + "," + str(pos[1])
            # Procura se já existe
            for i in range(len(came_from)):
                if came_from[i][0] == key:
                    came_from[i][1] = from_pos
                    return
            came_from.append([key, from_pos])
        
        def get_came_from(pos):
            """Obtém de onde veio"""
            key = str(pos[0]) + "," + str(pos[1])
            for i in range(len(came_from)):
                if came_from[i][0] == key:
                    return came_from[i][1]
            return None
        
        def pos_in_list(pos, pos_list):
            """Verifica se posição está na lista"""
            for i in range(len(pos_list)):
                p = pos_list[i]
                if p[0] == pos[0] and p[1] == pos[1]:
                    return True
            return False
        
        def remove_from_list(pos, pos_list):
            """Remove posição da lista"""
            new_list = []
            for i in range(len(pos_list)):
                p = pos_list[i]
                if not (p[0] == pos[0] and p[1] == pos[1]):
                    new_list.append(p)
            return new_list
        
        # Inicialização
        open_list.append(start)
        set_score(g_score, start, 0)
        set_score(f_score, start, self.heuristic(start, end))
        
        # Loop principal do A*
        while len(open_list) > 0:
            # Encontra nó com menor f_score na open_list
            current = open_list[0]
            current_f = get_score(f_score, current)
            
            for i in range(1, len(open_list)):
                pos = open_list[i]
                f = get_score(f_score, pos)
                if f < current_f:
                    current = pos
                    current_f = f
            
            # Se chegou ao destino, reconstrói o caminho
            if current[0] == end[0] and current[1] == end[1]:
                path = []
                temp = current
                while temp is not None:
                    path.append(temp)
                    temp = get_came_from(temp)
                
                # Inverte o caminho (estava de trás para frente)
                reversed_path = []
                for i in range(len(path) - 1, -1, -1):
                    reversed_path.append(path[i])
                
                return reversed_path
            
            # Move current de open para closed
            open_list = remove_from_list(current, open_list)
            closed_list.append(current)
            
            # Explora vizinhos
            neighbors = self.get_neighbors(current)
            for i in range(len(neighbors)):
                neighbor = neighbors[i]
                
                # Ignora se já foi explorado
                if pos_in_list(neighbor, closed_list):
                    continue
                
                # Calcula custo tentativo
                # Adiciona penalidade para engarrafamentos
                cost = 1
                if self.city.get_cell(neighbor[0], neighbor[1]) == self.city.TRAFFIC:
                    cost = 10  # Penalidade alta para tráfego
                
                tentative_g = get_score(g_score, current) + cost
                
                # Se não está na open_list, adiciona
                if not pos_in_list(neighbor, open_list):
                    open_list.append(neighbor)
                elif tentative_g >= get_score(g_score, neighbor):
                    # Se o caminho não é melhor, ignora
                    continue
                
                # Este é o melhor caminho até agora
                set_came_from(neighbor, current)
                set_score(g_score, neighbor, tentative_g)
                set_score(f_score, neighbor, tentative_g + self.heuristic(neighbor, end))
        
        # Não encontrou caminho
        return None

