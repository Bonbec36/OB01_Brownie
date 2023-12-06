import random
import matplotlib.pyplot as plt
import numpy as np

def simulation_lancer_pieces(nombre_lancers):
    positions = []
    solde = 0
    
    for _ in range(nombre_lancers):
        if random.choice(['pile', 'face']) == 'pile':
            solde += 1
        else:
            solde -= 1
        positions.append(solde)
    
    return positions

# Définir le nombre de lancers
nombre_lancers = 300

# Effectuer la simulation
positions = simulation_lancer_pieces(nombre_lancers)

# Graphique 
x = np.arange(0, len(positions), 1)
y = np.array(positions)
plt.plot(x, y)
plt.axhline(0, color='black', linewidth=2, linestyle='--')  # Ajouter la ligne y=0 en noir plus foncé
plt.xlabel('Nombre de lancers')
plt.ylabel('Solde obtenu')
plt.title('Simulation lancers de pièces (pile ou face)')
plt.ylim(-15, 30)  
plt.grid(True)

# Sauvegarder l'image avant de l'afficher
#plt.savefig("lancer.png", format="png", dpi=800)

# Afficher la figure
plt.show()


