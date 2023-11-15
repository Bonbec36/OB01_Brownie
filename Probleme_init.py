import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import PillowWriter
import random
import time

"""

# Paramètres de la simulation
num_steps = 1000  # Nombre de pas de temps
step_size = 1  # Taille du pas
initial_position = np.array([0.0, 0.0])  # Position initiale
x = [0, 0]
y = [0, 0]

combinaison_disp_2D = [(1, 0), (-1, 0), (0, 1), (0, -1)]
combinaison_disp_3D = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

combinaison_disp = combinaison_disp_2D

fig_animate, ax = plt.subplots()

line2 = ax.plot(x, y)

size = 10

ax.set_xlim([-size, size])
ax.set_ylim([-size, size])

point = plt.scatter(0, 0, 100, 'b')
pos_arrive = (6, -4)
arrive = plt.scatter(pos_arrive[0], pos_arrive[1], 100, 'g')
plt.plot(x, y, 'r')


murPresent = True

def animate(z):  
    combinaison_inst = ()
    
    if murPresent == True:
        if x[-1] >= size:
            comb_prov = [i for i in combinaison_disp]
            comb_prov.remove((1, 0))
            combinaison_inst = comb_prov[random.randint(0, 2)]
        elif x[-1] <= -size:
            comb_prov = [i for i in combinaison_disp]
            comb_prov.remove((-1, 0))
            combinaison_inst = comb_prov[random.randint(0, 2)]
        elif y[-1] >= size:
            comb_prov = [i for i in combinaison_disp]
            comb_prov.remove((0, 1))
            combinaison_inst = comb_prov[random.randint(0, 2)]
        elif y[-1] <= -size:
            comb_prov = [i for i in combinaison_disp]
            comb_prov.remove((0, -1))
            combinaison_inst = comb_prov[random.randint(0, 2)]
        else : 
            combinaison_inst = combinaison_disp[random.randint(0, 3)]
    else:
        combinaison_inst = combinaison_disp[random.randint(0, 3)]
    
    x.append(x[-1] + combinaison_inst[0])
    y.append(y[-1] + combinaison_inst[1])

    #time.sleep(0.5)
    point.set_offsets([x[-1], y[-1]])
    plt.plot(x, y, 'r')


    if x[-1] == pos_arrive[0] and y[-1] == pos_arrive[1]:
        anim.event_source.stop()

    
    return x, y, point

anim = animation.FuncAnimation(fig_animate, animate, frames=num_steps, blit=False, interval=100)

ax.set_facecolor('#d3d3d3')
plt.show()

"""

num_steps = 40  # Nombre de pas de temps
step_size = 1  # Taille du pas
initial_position = np.array([0.0, 0.0, 0.0])  # Position initiale
x = [0, 0]
y = [0, 0]
z = [0, 0]

combinaison_disp_3D = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

combinaison_disp = combinaison_disp_3D


fig_animate = plt.figure(figsize = (8,8))
ax = fig_animate.add_subplot(projection='3d')

line2 = ax.plot(x, y, z)

size = 10

ax.set_xlim([-size, size])
ax.set_ylim([-size, size])
ax.set_zlim([-size, size])

point = ax.scatter([0], [0], [0])
#pos_arrive = (6, -4)
#arrive = plt.scatter(pos_arrive[0], pos_arrive[1], 100, 'g')
   

plt.plot(x, y, z, 'r')

def animate(k): 
    combinaison_inst = combinaison_disp_3D[random.randint(0, 5)]
    x.append(x[-1] + combinaison_inst[0])
    y.append(y[-1] + combinaison_inst[1])
    z.append(z[-1] + combinaison_inst[2])
    plt.plot(x, y, z, 'r')
    point._offsets3d = (x[-1:], y[-1:], z[-1:])

    return x, y, z, point

anim = animation.FuncAnimation(fig_animate, animate, frames=num_steps, blit=False, interval=100)
#anim.save("Test_01.gif", dpi=300, writer=PillowWriter(fps=25))

plt.show()