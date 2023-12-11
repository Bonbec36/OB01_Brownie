import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
import matplotlib
from Fonction_brownien import *
import random


## Definition de la classe Particule. Une classe est un object auquel on peux donner des propriétés et fonctions internes.


class Particle:
    """
    Toutes les particules possèdent une masse, un rayon, une postion (x et y), une vitesse (vx et vy), une trajectoire,
    qui est l'historique de leurs postions et une couleur pour l'affichage. De plus elles ont une fonction qui permet d'
    obtenir leur énergie cinétique.
    """
    def __init__(self, mass, radius, x, y, vx, vy, color):
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.trajectory = [] 
        self.color = color
        
    def get_Energie_cinetique(self):
        return 0.5*self.mass*np.sqrt(self.vx**2+self.vy**2)**2
    

##Les différentes fonctions____________________________________________________________________________________________

def update_position(particle, dt):
    """
    Cette fonction permet de passer d'un instant t à un instant t+1, grace à sa postion et sa vitesse à l'instant t.
    """
    particle.x += particle.vx * dt
    particle.y += particle.vy * dt
    particle.trajectory.append((particle.x, particle.y)) 

def check_wall_collision(particle, wall_size):
    """
    Cette fonction permet de prendre en compte les limites de l'enceinte. Si une particule touche un bord, elle est renvoyée
    selon la loi de la réflexion.
    """
    if particle.x - particle.radius < 0 or particle.x + particle.radius > wall_size:
        particle.vx *= -1
    if particle.y - particle.radius < 0 or particle.y + particle.radius > wall_size:
        particle.vy *= -1

def check_particle_collision(particles):
    """
    On parcourt chaque particule. Pour chaque particule, on verifie sa potion par rapport à chacune des autres particules. Ensuite
    si deux particules se supperposent, on modifie leur vitesse selon la loi des collisions élastiques.
    """
    for i in range(len(particles)):
        for j in range(i+1, len(particles)):
            particle1 = particles[i]
            particle2 = particles[j]
            distance = np.sqrt((particle1.x - particle2.x)**2 + (particle1.y - particle2.y)**2)
            if distance <= particle1.radius + particle2.radius:
                angle = np.arctan2(particle2.y - particle1.y, particle2.x - particle1.x)
                v1 = np.sqrt(particle1.vx**2 + particle1.vy**2)
                v2 = np.sqrt(particle2.vx**2 + particle2.vy**2)

                theta1 = np.arctan2(particle1.vy, particle1.vx)
                theta2 = np.arctan2(particle2.vy, particle2.vx)

                phi = angle
                m1 = particle1.mass
                m2 = particle2.mass

                particle1.vx = ((v1 * np.cos(theta1 - phi) * (m1 - m2) + 2 * m2 * v2 * np.cos(theta2 - phi)) / (m1 + m2)) * np.cos(phi) + v1 * np.sin(theta1 - phi) * np.cos(phi + np.pi / 2)
                particle1.vy = ((v1 * np.cos(theta1 - phi) * (m1 - m2) + 2 * m2 * v2 * np.cos(theta2 - phi)) / (m1 + m2)) * np.sin(phi) + v1 * np.sin(theta1 - phi) * np.sin(phi + np.pi / 2)

                particle2.vx = ((v2 * np.cos(theta2 - phi) * (m2 - m1) + 2 * m1 * v1 * np.cos(theta1 - phi)) / (m1 + m2)) * np.cos(phi) + v2 * np.sin(theta2 - phi) * np.cos(phi + np.pi / 2)
                particle2.vy = ((v2 * np.cos(theta2 - phi) * (m2 - m1) + 2 * m1 * v1 * np.cos(theta1 - phi)) / (m1 + m2)) * np.sin(phi) + v2 * np.sin(theta2 - phi) * np.sin(phi + np.pi / 2)

def update(frame, particles, wall_size, dt):
    """
    A chaque instant, on simule les collisions du systeme, puis on actualise les positions de toutes les particules. On peut
    aussi calculer l'energie totale du systeme et se rendre compte qu'elle est constante (mouvement sochastique). 
    """
    simulate_collision(particles, wall_size, 1, dt)
    x_values = [particle.x for particle in particles]
    y_values = [particle.y for particle in particles]
    sc.set_offsets(np.array([x_values, y_values]).T)

    total_energy = sum([particle.mass * particle.get_Energie_cinetique() for particle in particles])
    #print(f"Énergie totale du système à l'étape {frame + 1}: {total_energy}")

    line.set_data(*zip(*particles[-1].trajectory))
    
    return sc, line

def simulate_collision(particles, wall_size, num_steps, dt):
    """
    Afin de simuler les collisions, on actualise la postions, puis on verifie les collisions avec les murs, puis les collisions entre
    les particules.
    """
    for _ in range(num_steps):
        for particle in particles:
            update_position(particle, dt)
            check_wall_collision(particle, wall_size)
        check_particle_collision(particles)


if __name__ == "__main__":

    ## Parametre par default de la simulation
    wall_size = 20
    T = 20
    taille_groupement_h20 = 0.05
    nb_groupement_h20 = 200
    k_visualisation = 1e-6 #3e-6
    num_steps = 100
    dt = 0.1
    save_anim = False
    facteur = 1000

    while True:
        ## On présente le programme
        print("Bienvenue sur la simulation d'un pollen en 2D\n",
                    "Veuillez choisir vos paramètres : \n",
                    "-Taille de l'enceinte (entier) (en micron)\n", 
                    "-La température (decimal)(en °C)\n", 
                    "-Taille des groupements H2O (decimal)(en micron)\n", 
                    "-Nombre de groupement H2O (entier)\n", 
                    "-La constrante de visualisation (decimal)\n", 
                    "-Le delta t (decimal)(en seconde)\n", 
                    "-Enregistrement de l'animation (bool)\n")
        
        ##On demande à l'utilisateur les différents paramètres de la simualtion
        wall_size = get_input("Entrez la valeur de la taille de l'enceine", default_value=20, value_type=int, min_value=0)
        T = get_input("Entrez la valeur de la température", default_value=20, value_type=float, min_value=-273.15)
        taille_groupement_h20 = get_input("Entrez la taille des groupements", default_value=0.05, value_type=float, min_value=0.01, max_value=wall_size)
        nb_groupement_h20 = get_input("Entrez le nombre des groupements", default_value=200, value_type=int, min_value=10, max_value=5000)
        facteur = get_input("Entrez le nombre facteur", default_value=1000, value_type=int, min_value=1, max_value=1e6)
        k_visualisation = get_input("Entrez la konstante de visualisation", default_value=1e-6, value_type=float, min_value=1e-20, max_value=1e20)
        num_steps  = get_input("Entrez le nombre d'étapes", default_value=100, value_type=int, min_value=10, max_value=5000)
        dt = get_input("Entrez le delta t", default_value=0.1, value_type=float, min_value=1e-6, max_value=10)
        save_anim = get_input("Voulez vous enregistrer l'animation", default_value=False, value_type=bool)
        
        if save_anim:
            save_name = get_input("Entrez le nom : ", default_value=False, value_type=str)
            anim_mp4 = get_input("Voulez vous enregistrer l'animation en MP4 (sinon elle sera en .gif)", default_value=False, value_type=bool)
            fps = get_input("Entrez la valeur du fps", default_value=30, value_type=int, min_value=10, max_value=120)
        
        
        ##Grace aux paramètres choisis, nous déterminons les paramètres suivant :
        e_c_moy_h20 = 3*(1.38e-23)*(273.15+T)/2
        nb_molecule_h20 = (wall_size**2*taille_groupement_h20)*(1e-15)*(6.022e23)/(18e-3)
        nb_h20_par_groupement = nb_molecule_h20/nb_groupement_h20
        e_c_moy_groupement_h20 = nb_molecule_h20*e_c_moy_h20/nb_groupement_h20
        masse_groupement_h20 = nb_molecule_h20 * 18e-3/(6.022e23*(nb_groupement_h20))
        vitesse_moyenne_groument_h20 = np.sqrt(2*e_c_moy_groupement_h20/masse_groupement_h20)
        vitesse_moyenne_h20 = np.sqrt(2*e_c_moy_h20*6.022e23/18e-3) * 1e6 * k_visualisation
        vitesse_moyenne_groument_h20_MICRO = vitesse_moyenne_groument_h20*1e6

        #On cree une liste de particules
        particles = []

        #On calcule la vitesse moyenne des groupements H2O
        for i in range(nb_groupement_h20):
            v = np.random.normal(vitesse_moyenne_h20, 0.1*vitesse_moyenne_h20, facteur)
            theta = np.random.uniform(0, 2*np.pi, facteur)

            vx_g = (v@np.cos(theta))/facteur
            vy_g = (v@np.sin(theta))/facteur

            #On ajoute les particules d'eau
            particles.append(Particle(mass=masse_groupement_h20, radius=0.05, x=random.randint(1,wall_size - 1),  y=random.randint(1,wall_size -1), vx = vx_g, vy = vy_g, color="blue"))
        
        
        #On ajoute le grain de pollen
        particles.append(Particle(mass=1e-9*k_visualisation, radius=2.3, x=wall_size/2, y=wall_size/2, vx=0, vy=0, color='#2EFF00')) #20 à 55 μm taille moyenne d'un grain de pollen

        #On donne les paramètres pour affciher l'animation
        fig, ax = plt.subplots()
        ax.set_xlim(0, wall_size)
        ax.set_ylim(0, wall_size)
        plt.title("Modelisation d'un grain de pollen dans un fluide (2D)")
        ax.set_aspect('equal', adjustable='box')

        #On affiche les points et la trajectoire du pollen
        sc = ax.scatter([particle.x for particle in particles], [particle.y for particle in particles], s=[particle.radius*200 for particle in particles], c=[particle.color for particle in particles])
        line, = ax.plot([], [], '#2EFF00', lw=2)

        #On cree une animation
        ani = FuncAnimation(fig, update, frames=num_steps, fargs=(particles, wall_size, dt), interval=10, blit=True)

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
        