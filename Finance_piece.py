import random
import matplotlib.pyplot as plt
import numpy as np
from Fonction_brownien import *

def simulation_lancer_pieces(nombre_lancers, gain=1):
    """
    C'est une fonction qui permet de génerer l'evolution d'un solde d'une personne qui jouerais à pile ou face.
    """

    #On cree une liste de position
    positions = []

    #On cree le solde
    solde = 0

    
    for _ in range(nombre_lancers):
        """
        A chaque lancer, on choisit aléatoirement si la piece tombe sur pile ou face et si elle tombe sur pile,
        on ajoute le gain (par default) au solde et si c'est face, on prèle le gain au solde.
        """
        if random.choice(['pile', 'face']) == 'pile':
            solde += gain
        else:
            solde -= gain
        positions.append(solde)
    
    return positions

## Paramètres de la simulation
nombre_lancers = 300
nb_simulation = 100
gain_piece = 1

## On demande les paramètres à l'utilisateur
nombre_lancers = get_input("Entrez le nombre de lancer", default_value=300, value_type=int, min_value=1)
nb_simulation = get_input("Entrez le nombre de simulation", default_value=100, value_type=int, min_value=1)
gain_piece = get_input("Entrez la valeur du gain et perte à chaque lancer", default_value=1, value_type=float)
        

## On fait la simulation et la moyenne des simualtion
positions = simulation_lancer_pieces(nombre_lancers)
positions_multiple = [simulation_lancer_pieces(nombre_lancers, gain=gain_piece) for _ in range(nb_simulation)]

moyenne_position = mean_prices = np.mean(positions_multiple, axis=0)


## On affiche les simulations 
x = np.arange(0, len(positions), 1)
y = np.array(positions)
for i in range(nb_simulation):
    #Pour chaque simulation indiviuelle, on l'affcihe en clair
    plt.plot(x, positions_multiple[i], color='deepskyblue', alpha=0.2, lw=1)

#On affiche la moyenne
plt.plot(x,moyenne_position, color='blue', label='Moyenne des simulations', lw=2)
plt.xlabel('Nombre de lancers')
plt.ylabel('Solde obtenu')
plt.title('Simulation lancers de pièces (pile ou face)')
plt.ylim(np.min(np.array(positions_multiple)) - 1, np.max(np.array(positions_multiple)) + 1)  
plt.grid(True)
plt.legend(loc='best')

# Afficher la figure
plt.show()

