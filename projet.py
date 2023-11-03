import numpy as np
import matplotlib.pyplot as plt

# Paramètres de la simulation
num_steps = 1000  # Nombre de pas de temps
step_size = 0.1  # Taille du pas
initial_position = np.array([0.0, 0.0])  # Position initiale

# Générer des déplacements aléatoires
delta_x = np.random.normal(0, step_size, num_steps)
delta_y = np.random.normal(0, step_size, num_steps)

# Calculer la trajectoire
x = np.cumsum(delta_x)
y = np.cumsum(delta_y)

# Ajouter la position initiale à la trajectoire
x = np.insert(x, 0, initial_position[0])
y = np.insert(y, 0, initial_position[1])

# Afficher la trajectoire
plt.figure(figsize=(8, 6))
plt.plot(x, y)
plt.title("Mouvement Brownien 2D")
plt.xlabel("Position en x")
plt.ylabel("Position en y")
plt.grid()
plt.show()

#%%
import numpy as np
import matplotlib.pyplot as plt

# Paramètres de la simulation
num_particles = 5  # Nombre de particules
num_steps = 1000  # Nombre de pas de temps
step_size = 0.1  # Taille du pas

# Initialisation des positions
initial_positions = np.zeros((num_particles, 2))  # Toutes les particules commencent à l'origine

# Générer des déplacements aléatoires pour chaque particule
delta_x = np.random.normal(0, step_size, (num_particles, num_steps))
delta_y = np.random.normal(0, step_size, (num_particles, num_steps))

# Calculer les trajectoires de chaque particule
x = np.cumsum(delta_x, axis=1)
y = np.cumsum(delta_y, axis=1)

# Ajouter les positions initiales aux trajectoires
x = np.hstack((initial_positions[:, 0][:, np.newaxis], x))
y = np.hstack((initial_positions[:, 1][:, np.newaxis], y))

# Afficher les trajectoires de chaque particule
plt.figure(figsize=(8, 6))
for i in range(num_particles):
    plt.plot(x[i], y[i], label=f'Particule {i + 1}')

plt.title("Mouvement Brownien de Multiples Particules en 2D")
plt.xlabel("Position en x")
plt.ylabel("Position en y")
plt.legend()
plt.grid()
plt.show()

#%%
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Paramètres de la simulation
num_particles = 5  # Nombre de particules
num_steps = 1000  # Nombre de pas de temps
step_size = 0.1  # Taille du pas

# Initialisation des positions
initial_positions = np.zeros((num_particles, 3))  # Toutes les particules commencent à l'origine

# Générer des déplacements aléatoires pour chaque particule
delta_x = np.random.normal(0, step_size, (num_particles, num_steps))
delta_y = np.random.normal(0, step_size, (num_particles, num_steps))
delta_z = np.random.normal(0, step_size, (num_particles, num_steps))

# Calculer les trajectoires de chaque particule
x = np.cumsum(delta_x, axis=1)
y = np.cumsum(delta_y, axis=1)
z = np.cumsum(delta_z, axis=1)

# Ajouter les positions initiales aux trajectoires
x = np.hstack((initial_positions[:, 0][:, np.newaxis], x))
y = np.hstack((initial_positions[:, 1][:, np.newaxis], y))
z = np.hstack((initial_positions[:, 2][:, np.newaxis], z))

# Afficher les trajectoires de chaque particule en 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(num_particles):
    ax.plot(x[i], y[i], z[i], label=f'Particule {i + 1}')

ax.set_title("Mouvement Brownien de Multiples Particules en 3D")
ax.set_xlabel("Position en x")
ax.set_ylabel("Position en y")
ax.set_zlabel("Position en z")
ax.legend()
plt.grid()
plt.show()
