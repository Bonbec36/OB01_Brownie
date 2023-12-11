import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import animation
from matplotlib.animation import PillowWriter, FFMpegWriter
from Fonction_brownien import *
import random
import time


## Paramètres de la simulation
num_steps = 1000  # Nombre de pas de temps
step_size = 1  # Taille du pas
initial_position = np.array([0.0, 0.0])  # Position initiale
x = [0, 0]
y = [0, 0]
x_arrive = 6 # Coordonée x de l'arrivée
y_arrive = 2 # Coordonée y de l'arrivée
size = 10 #Taille du plan

#Activation des murs
murPresent = True 

while True:

    initial_position = np.array([0.0, 0.0]) 
    x = [0, 0]
    y = [0, 0]

    #On présente le programe

    ##On demande à l'utilisateur les différents paramètres de la simualtion
    num_steps = get_input("Entrez le nombre d'étapes ", default_value=1000, value_type=int, min_value=10)
    size = get_input("Entrez la taille de l'enceinte", default_value=10, value_type=int, min_value=1, max_value=1e4)
    step_size = get_input("Entrez la taille du pas", default_value=1, value_type=int, min_value=int(size/1000), max_value=size)
    x_arrive = get_input("Entrez la position x de sa maison", default_value=6, value_type=int, min_value=-size, max_value=size)
    y_arrive = get_input("Entrez la position y de sa maison", default_value=2, value_type=int, min_value=-size, max_value=size)
    save_anim = get_input("Voulez vous enregistrer l'animation", default_value=False, value_type=bool)
    
    if save_anim:
        save_name = get_input("Entrez le nom : ", default_value=False, value_type=str)
        anim_mp4 = get_input("Voulez vous enregistrer l'animation en MP4 (sinon elle sera en .gif)", default_value=False, value_type=bool)
        fps = get_input("Entrez la valeur du fps", default_value=30, value_type=int, min_value=10, max_value=120)
    

    #On definit les différents mouvement possible
    combinaison_disp_2D = [(step_size, 0), (-step_size, 0), (0, step_size), (0, -step_size)]

    combinaison_disp = combinaison_disp_2D

    #On prepare l'affichage
    fig_animate, ax = plt.subplots()

    line2 = ax.plot(x, y)

    #On défnit les limites du plan
    ax.set_xlim([-size, size])
    ax.set_ylim([-size, size])

    #On déninit la personne
    point = plt.scatter(0, 0, 100, 'b')

    #On montre la positions d'arrivé avec un tulpe
    pos_arrive = (x_arrive, y_arrive)
    arrive = plt.scatter(pos_arrive[0], pos_arrive[1], 100, 'g')
    plt.plot(x, y, 'r')

    #On commence un chrono pour mesurer le mit pour rentrer chez soi
    start_time = time.time()

    def animate(z):
        """
        On définit une fonction pour faire l'animation
        """  
        combinaison_inst = ()
        
        if murPresent == True:
            """
            Si l'on est sur le bord du plan, on supprime la directions qui pourrais permettre
            de sortir du plan
            """
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
        
        #On actualise la position
        x.append(x[-1] + combinaison_inst[0])
        y.append(y[-1] + combinaison_inst[1])

        point.set_offsets([x[-1], y[-1]])
        plt.plot(x, y, 'r')
        plt.title("Déplacement aléatoire d'une personne dans le plan")

        if x[-1] == pos_arrive[0] and y[-1] == pos_arrive[1]:
            """
            Si la personnne est rentré chez elle, on arrete l'animation et on donne le temps 
            qu'elle a mis pour rentrer
            """
            ani.event_source.stop()
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Temps d'exécution : {execution_time:.6f} secondes")

        
        return x, y, point

    #On fait l'animation
    ani = animation.FuncAnimation(fig_animate, animate, frames=num_steps, blit=False, interval=100)

    ax.set_facecolor('#d3d3d3')
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
    
