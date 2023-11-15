import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Paramètres des ellipses
num_points = 5
a_values = np.random.uniform(2, 4, num_points)  # Demi-grand axe
b_values = np.random.uniform(1, 2, num_points)  # Demi-petit axe

# Fonction paramétrique pour l'ellipse en 3D
def parametric_equation_3d(t, a, b):
    x = a * np.cos(t)
    y = b * np.sin(t)
    z = 0.5 * np.sin(t)  # Composante en z pour créer une spirale en 3D
    return x, y, z

# Initialisation de la figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatters = [ax.plot([], [], [], 'bo')[0] for _ in range(num_points)]  # Utiliser plot pour créer les scatter plots en 3D

# Fonction de mise à jour de l'animation
def update(frame):
    t = 0.1 * frame  # Paramètre de la courbe paramétrique
    for i, scatter in enumerate(scatters):
        a = a_values[i]
        b = b_values[i]
        x, y, z = parametric_equation_3d(t, a, b)
        scatter.set_data(x, y)  # Met à jour les positions en x et y
        scatter.set_3d_properties(z)  # Met à jour la composante en z
    return scatters

# Paramètres de l'animation
num_frames = 100
ani = FuncAnimation(fig, update, frames=num_frames, blit=True)

ax.set_xlim(-max(a_values), max(a_values))
ax.set_ylim(-max(b_values), max(b_values))
ax.set_zlim(-1, 1)
ax.set_title(f"Animation de {num_points} scatters suivant des courbes paramétriques elliptiques en 3D")

plt.show()
