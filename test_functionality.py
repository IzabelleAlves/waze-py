# -*- coding: utf-8 -*-
"""
Script de teste para verificar funcionalidades
Execute este script para testar se tudo está funcionando corretamente
"""

from city import City
from pathfinding import PathFinder

def test_city_creation():
    """Testa criação de cidade"""
    print("Testando criação de cidade...")
    city = City(10, 10, "Cidade Teste")
    assert city.width == 10
    assert city.height == 10
    assert city.name == "Cidade Teste"
    print("[OK] Criacao de cidade OK")
    return city

def test_cell_operations(city):
    """Testa operações com células"""
    print("\nTestando operações com células...")
    
    # Testa set_cell
    city.set_cell(5, 5, City.STREET)
    assert city.get_cell(5, 5) == City.STREET
    
    city.set_cell(3, 3, City.HOUSE)
    assert city.get_cell(3, 3) == City.HOUSE
    
    city.set_cell(7, 7, City.BUILDING)
    assert city.get_cell(7, 7) == City.BUILDING
    
    print("[OK] Operacoes com celulas OK")

def test_walkable(city):
    """Testa verificação de células transitáveis"""
    print("\nTestando células transitáveis...")
    
    city.set_cell(2, 2, City.STREET)
    city.set_cell(3, 3, City.HOUSE)
    
    assert city.is_walkable(2, 2) == True
    assert city.is_walkable(3, 3) == False
    
    print("[OK] Verificacao de celulas transitaveis OK")

def test_traffic(city):
    """Testa sistema de tráfego"""
    print("\nTestando sistema de tráfego...")
    
    # Adiciona tráfego
    city.set_cell(4, 4, City.STREET)
    city.add_traffic(4, 4)
    assert city.get_cell(4, 4) == City.TRAFFIC
    
    # Remove tráfego
    city.remove_traffic(4, 4)
    assert city.get_cell(4, 4) == City.STREET
    
    # Testa geração aleatória
    city.clear()
    for x in range(10):
        city.set_cell(x, 5, City.STREET)
    
    city.generate_random_traffic(3)
    
    # Conta tráfegos
    traffic_count = 0
    for y in range(10):
        for x in range(10):
            if city.get_cell(x, y) == City.TRAFFIC:
                traffic_count += 1
    
    assert traffic_count > 0
    print(f"[OK] Sistema de trafego OK (gerados {traffic_count} engarrafamentos)")

def test_pathfinding():
    """Testa algoritmo de pathfinding"""
    print("\nTestando algoritmo A*...")
    
    # Cria cidade com caminho simples
    city = City(10, 10, "Teste Pathfinding")
    
    # Cria ruas horizontais
    for x in range(10):
        city.set_cell(x, 5, City.STREET)
    
    # Cria ruas verticais conectando
    for y in range(10):
        city.set_cell(5, y, City.STREET)
    
    # Testa pathfinding
    pathfinder = PathFinder(city)
    path = pathfinder.find_path([0, 5], [9, 5])
    
    assert path is not None
    assert len(path) == 10  # Caminho direto de (0,5) até (9,5)
    print(f"[OK] Caminho simples encontrado: {len(path)} celulas")
    
    # Testa caminho com obstaculo
    city.set_cell(5, 5, City.HOUSE)  # Bloqueia interseccao
    path2 = pathfinder.find_path([0, 5], [9, 5])
    
    assert path2 is not None
    assert len(path2) == 10  # Ainda deve encontrar caminho direto (nao precisa da interseccao)
    print(f"[OK] Caminho com obstaculo encontrado: {len(path2)} celulas")
    
    # Testa caminho impossivel
    city.clear()
    city.set_cell(0, 0, City.STREET)
    city.set_cell(9, 9, City.STREET)
    # Nao ha conexao entre (0,0) e (9,9)
    
    path3 = pathfinder.find_path([0, 0], [9, 9])
    assert path3 is None
    print("[OK] Caminho impossivel detectado corretamente")
    
    # Testa caminho complexo
    city.clear()
    # Cria labirinto simples
    for x in range(10):
        city.set_cell(x, 0, City.STREET)
        city.set_cell(x, 9, City.STREET)
    for y in range(10):
        city.set_cell(0, y, City.STREET)
        city.set_cell(9, y, City.STREET)
    city.set_cell(5, 5, City.STREET)
    for y in range(6):
        city.set_cell(5, y, City.STREET)
    for y in range(5, 10):
        city.set_cell(5, y, City.STREET)
    
    path4 = pathfinder.find_path([0, 0], [9, 9])
    assert path4 is not None
    print(f"[OK] Caminho complexo encontrado: {len(path4)} celulas")

def test_save_load():
    """Testa salvamento e carregamento"""
    print("\nTestando salvamento e carregamento...")
    
    import os
    
    # Cria cidade de teste
    city1 = City(5, 5, "Cidade Salva")
    city1.set_cell(0, 0, City.STREET)
    city1.set_cell(1, 1, City.HOUSE)
    city1.set_cell(2, 2, City.BUILDING)
    
    # Salva
    test_file = "maps/test_city.json"
    city1.save_to_file(test_file)
    assert os.path.exists(test_file)
    print("[OK] Salvamento OK")
    
    # Carrega
    city2 = City.load_from_file(test_file)
    assert city2 is not None
    assert city2.name == "Cidade Salva"
    assert city2.width == 5
    assert city2.height == 5
    assert city2.get_cell(0, 0) == City.STREET
    assert city2.get_cell(1, 1) == City.HOUSE
    assert city2.get_cell(2, 2) == City.BUILDING
    print("[OK] Carregamento OK")
    
    # Limpa arquivo de teste
    os.remove(test_file)
    print("[OK] Arquivo de teste removido")

def main():
    """Executa todos os testes"""
    print("=" * 50)
    print("TESTES DE FUNCIONALIDADE")
    print("=" * 50)
    
    try:
        city = test_city_creation()
        test_cell_operations(city)
        test_walkable(city)
        test_traffic(city)
        test_pathfinding()
        test_save_load()
        
        print("\n" + "=" * 50)
        print(">>> TODOS OS TESTES PASSARAM! <<<")
        print("=" * 50)
        print("\nO sistema esta funcionando corretamente!")
        print("Execute 'python main.py' para usar a aplicacao.")
        
    except AssertionError as e:
        print(f"\n[ERRO] Teste falhou!")
        print(f"Detalhes: {e}")
        return False
    except Exception as e:
        print(f"\n[ERRO INESPERADO] {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()

