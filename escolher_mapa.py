# -*- coding: utf-8 -*-
"""
Script para escolher qual mapa carregar
"""

import os
import shutil

def listar_mapas():
    """Lista todos os mapas disponíveis"""
    mapas_dir = "maps"
    
    if not os.path.exists(mapas_dir):
        print("Pasta 'maps' nao encontrada!")
        return []
    
    # Lista todos os arquivos JSON na pasta maps
    mapas = []
    for arquivo in os.listdir(mapas_dir):
        if arquivo.endswith('.json') and arquivo != 'cidade.json':
            mapas.append(arquivo)
    
    return sorted(mapas)

def escolher_mapa():
    print("=" * 60)
    print("ESCOLHER MAPA PARA CARREGAR")
    print("=" * 60)
    
    mapas = listar_mapas()
    
    if not mapas:
        print("\nNenhum mapa encontrado na pasta 'maps/'")
        print("Execute 'python create_sample_maps.py' para criar mapas de exemplo.")
        return
    
    print("\nMapas disponiveis:\n")
    
    # Exibe lista numerada
    for i, mapa in enumerate(mapas, 1):
        # Remove a extensão .json para exibição
        nome = mapa.replace('.json', '')
        print(f"  {i}. {nome}")
    
    print(f"\n  0. Cancelar")
    print()
    
    # Pede escolha do usuário
    try:
        escolha = int(input("Digite o numero do mapa que deseja usar: "))
        
        if escolha == 0:
            print("\nCancelado.")
            return
        
        if escolha < 1 or escolha > len(mapas):
            print("\nOpcao invalida!")
            return
        
        # Copia o mapa escolhido para cidade.json
        mapa_escolhido = mapas[escolha - 1]
        origem = os.path.join("maps", mapa_escolhido)
        destino = os.path.join("maps", "cidade.json")
        
        shutil.copy(origem, destino)
        
        nome_mapa = mapa_escolhido.replace('.json', '')
        
        print("=" * 60)
        print(f"SUCESSO! Mapa '{nome_mapa}' copiado para cidade.json")
        print("=" * 60)
        print("\nAgora execute:")
        print("  python main.py")
        print("\nE clique no botao 'Carregar' para usar este mapa!")
        
    except ValueError:
        print("\nPor favor, digite um numero valido.")
    except Exception as e:
        print(f"\nErro ao copiar mapa: {e}")

def main():
    """Funcao principal"""
    escolher_mapa()

if __name__ == "__main__":
    main()

