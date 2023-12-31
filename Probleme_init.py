import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib
from matplotlib.animation import PillowWriter, FFMpegWriter
import random
import time
from Fonction_brownien import *

## Paramètres de la simulation
num_steps = 40  # Nombre de pas de temps
step_size = 1  # Taille du pas
initial_position = np.array([0.0, 0.0, 0.0])  # Position initiale
x = [0, 0]
y = [0, 0]
z = [0, 0]
size = 10 #Taille de l'espace

#Activation des murs
murPresent3D = True 

while True:
    #On présente le programme

    ##On demande à l'utilisateur les différents paramètres de la simualtion
    num_steps = get_input("Entrez le nombre d'étapes ", default_value=100, value_type=int, min_value=10)
    size = get_input("Entrez la taille de l'enceinte", default_value=10, value_type=int, min_value=1, max_value=1e4)
    step_size = get_input("Entrez la taille du pas", default_value=1, value_type=int, min_value=int(size/1000), max_value=size)
    save_anim = get_input("Voulez vous enregistrer l'animation", default_value=False, value_type=bool)
    
    if save_anim:
        save_name = get_input("Entrez le nom : ", default_value=False, value_type=str)
        anim_mp4 = get_input("Voulez vous enregistrer l'animation en MP4 (sinon elle sera en .gif)", default_value=False, value_type=bool)
        fps = get_input("Entrez la valeur du fps", default_value=30, value_type=int, min_value=10, max_value=120)
    
    #On definit les différents mouvement possible
    combinaison_disp_3D = [(step_size, 0, 0), (-step_size, 0, 0), (0, step_size, 0), (0, -step_size, 0), (0, 0, step_size), (0, 0, -step_size)]

    combinaison_disp = combinaison_disp_3D

    #On prepare l'affichage
    fig_animate = plt.figure(figsize = (8,8))
    ax = fig_animate.add_subplot(projection='3d')

    line2 = ax.plot(x, y, z)


    #On défnit les limites du plan
    ax.set_xlim([-size, size])
    ax.set_ylim([-size, size])
    ax.set_zlim([-size, size])

    point = ax.scatter([0], [0], [0])
    
    #On déninit la personne
    plt.plot(x, y, z, 'r')
    plt.title("Déplacement aléatoire d'un oiseau dans l'espace")

    def animate(k): 
        """
        On définit une fonction pour faire l'animation
        """  
        combinaison_inst = combinaison_disp_3D[random.randint(0, 5)]

        if murPresent3D == True:
            """
            Si l'on est sur le bord du plan, on supprime la directions qui pourrais permettre
            de sortir du plan
            """
            if x[-1] >= size:
                comb_prov = [i for i in combinaison_disp]
                comb_prov.remove((step_size, 0, 0))
                combinaison_inst = comb_prov[random.randint(0, 4)]
            elif x[-1] <= -size:
                comb_prov = [i for i in combinaison_disp]
                comb_prov.remove((-step_size, 0, 0))
                combinaison_inst = comb_prov[random.randint(0, 4)]
            elif y[-1] >= size:
                comb_prov = [i for i in combinaison_disp]
                comb_prov.remove((0,step_size , 0))
                combinaison_inst = comb_prov[random.randint(0, 4)]
            elif y[-1] <= -size:
                comb_prov = [i for i in combinaison_disp]
                comb_prov.remove((0, -step_size, 0))
                combinaison_inst = comb_prov[random.randint(0, 4)]
            elif z[-1] >= size:
                comb_prov = [i for i in combinaison_disp]
                comb_prov.remove((0, 0, step_size))
                combinaison_inst = comb_prov[random.randint(0, 4)]
            elif z[-1] <= -size:
                comb_prov = [i for i in combinaison_disp]
                comb_prov.remove((0, 0, -step_size))
                combinaison_inst = comb_prov[random.randint(0, 4)]
            else : 
                combinaison_inst = combinaison_disp[random.randint(0, 5)]
        else:
            combinaison_inst = combinaison_disp[random.randint(0, 5)]

        #On actualise la position
        x.append(x[-1] + combinaison_inst[0])
        y.append(y[-1] + combinaison_inst[1])
        z.append(z[-1] + combinaison_inst[2])
        plt.plot(x, y, z, 'r')
        point._offsets3d = (x[-1:], y[-1:], z[-1:])

        return x, y, z, point
    
    
    #On fait l'animation
    ani = animation.FuncAnimation(fig_animate, animate, frames=num_steps, blit=False, interval=100)

    if save_anim:
            """
            Si l'utilisateur a choisi l'option de sauvegarde, on enregistre l'animation en fichier MP4 ou en Gif
            """
            if anim_mp4:
                matplotlib.rcParams['animation.ffmpeg_path'] = "ffmpeg-6.1-essentials_build\\bin\\ffmpeg.exe"
                writervideo = FFMpegWriter(fps=fps, bitrate=1800)
                ani.save(f"{save_name}.mp4", writer=writervideo, progress_callback=progress_callback)
            else:
                ani.save(f"{save_name}.gif", dpi=300, progress_callback=progress_callback, writer=PillowWriter(fps=fps))

    #On affiche l'animation
    plt.show()

    #On donne la possibilité à l'utilisateur de refaire une autre simulation sans quitter le programme
    recommencer = get_input("\nVoulez vous recommencer", default_value=True, value_type=bool)

    if recommencer == False:
        break
    else:
        print("\n\n")