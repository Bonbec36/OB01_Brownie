import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
import matplotlib
import random
from mpl_toolkits.mplot3d import Axes3D
from Fonction_brownien import *

## Definition de la classe Particule 3D. Une classe est un object auquel on peux donner des propriétés et fonctions internes.


class Particle3D:
    """
    Toutes les particules possèdent une masse, un rayon, une postion (x, y et z), une vitesse (vx, vy et vz), une trajectoire,
    qui est l'historique de leurs postions. De plus elles ont une fonction qui permet d'obtenir leur énergie cinétique.
    """
    def __init__(self, mass, radius, x, y, z, vx, vy, vz):
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.trajectory = [] 

    def get_Energie_cinetique(self):
        return 0.5 * self.mass * (self.vx**2 + self.vy**2 + self.vz**2)

def update_position3D(particle, dt):
    """
    Cette fonction permet de passer d'un instant t à un instant t+1, grace à sa postion et sa vitesse à l'instant t.
    """
    particle.x += particle.vx * dt
    particle.y += particle.vy * dt
    particle.z += particle.vz * dt
    if len(particle.trajectory) < 50:
        particle.trajectory.append((particle.x, particle.y, particle.z))
    else: 
        del particle.trajectory[0]
        particle.trajectory.append((particle.x, particle.y, particle.z))



def check_wall_collision3D(particle, wall_size):
    """
    Cette fonction permet de prendre en compte les limites de l'enceinte. Si une particule touche un bord, elle est renvoyée
    selon la loi de la réflexion.
    """
    if particle.x - particle.radius < 0 or particle.x + particle.radius > wall_size:
        particle.vx *= -1
    if particle.y - particle.radius < 0 or particle.y + particle.radius > wall_size:
        particle.vy *= -1
    if particle.z - particle.radius < 0 or particle.z + particle.radius > wall_size:
        particle.vz *= -1

def check_particle_collision3D(particles):
    """
    On parcourt chaque particule. Pour chaque particule, on verifie sa potion par rapport à chacune des autres particules. Ensuite
    si deux particules se supperposent, on modifie leur vitesse selon la loi des collisions élastiques.
    """
    for i in range(len(particles)):
        for j in range(i+1, len(particles)):
            particle1 = particles[i]
            particle2 = particles[j]

            distance = np.sqrt((particle1.x - particle2.x)**2 + (particle1.y - particle2.y)**2 + (particle1.z - particle2.z)**2)
            if distance <= particle1.radius + particle2.radius:
                dx = particle2.x - particle1.x
                dy = particle2.y - particle1.y
                dz = particle2.z - particle1.z

                angle = np.arctan2(dy, dx)
                phi = np.arctan2(np.sqrt(dy**2 + dx**2), dz)

                v1 = np.sqrt(particle1.vx**2 + particle1.vy**2 + particle1.vz**2)
                v2 = np.sqrt(particle2.vx**2 + particle2.vy**2 + particle2.vz**2)

                theta1 = np.arctan2(particle1.vy, particle1.vx)
                theta2 = np.arctan2(particle2.vy, particle2.vx)
                phi1 = np.arctan2(np.sqrt(particle1.vy**2 + particle1.vx**2), particle1.vz)
                phi2 = np.arctan2(np.sqrt(particle2.vy**2 + particle2.vx**2), particle2.vz)

                m1 = particle1.mass
                m2 = particle2.mass

                particle1.vx = ((v1 * np.cos(theta1 - angle) * (m1 - m2) + 2 * m2 * v2 * np.cos(theta2 - angle)) / (m1 + m2)) * np.cos(angle) + v1 * np.sin(theta1 - angle) * np.cos(angle + np.pi / 2)
                particle1.vy = ((v1 * np.cos(theta1 - angle) * (m1 - m2) + 2 * m2 * v2 * np.cos(theta2 - angle)) / (m1 + m2)) * np.sin(angle) + v1 * np.sin(theta1 - angle) * np.sin(angle + np.pi / 2)
                particle1.vz = (v1 * np.cos(phi1 - phi) * (m1 - m2) + 2 * m2 * v2 * np.cos(phi2 - phi)) / (m1 + m2) * np.sin(phi) + v1 * np.sin(phi1 - phi) * np.cos(phi)

                particle2.vx = ((v2 * np.cos(theta2 - angle) * (m2 - m1) + 2 * m1 * v1 * np.cos(theta1 - angle)) / (m1 + m2)) * np.cos(angle) + v2 * np.sin(theta2 - angle) * np.cos(angle + np.pi / 2)
                particle2.vy = ((v2 * np.cos(theta2 - angle) * (m2 - m1) + 2 * m1 * v1 * np.cos(theta1 - angle)) / (m1 + m2)) * np.sin(angle) + v2 * np.sin(theta2 - angle) * np.sin(angle + np.pi / 2)
                particle2.vz = (v2 * np.cos(phi2 - phi) * (m2 - m1) + 2 * m1 * v1 * np.cos(phi1 - phi)) / (m1 + m2) * np.sin(phi) + v2 * np.sin(phi2 - phi) * np.cos(phi)

def animate3D(frame, particles, wall_size, dt):
    """
    A chaque instant, on simule les collisions du systeme, puis on actualise les positions de toutes les particules. On peut
    aussi calculer l'energie totale du systeme et se rendre compte qu'elle est constante (mouvement sochastique). 
    """
    simulate_collision3D(particles, wall_size, 1, dt)
    x_values = [particle.x for particle in particles]
    y_values = [particle.y for particle in particles]
    z_values = [particle.z for particle in particles]
    
    for i, scatter in enumerate(scatters):
        scatter.set_data(x_values[i], y_values[i])  # Met à jour les positions en x et y
        scatter.set_3d_properties(z_values[i])


    total_energy = sum([particle.mass * particle.get_Energie_cinetique() for particle in particles])
    #print(f"Énergie totale du système à l'étape {frame + 1}: {total_energy}")


    return scatters 

def simulate_collision3D(particles, wall_size, num_steps, dt):
    """
    Afin de simuler les collisions, on actualise la postions, puis on verifie les collisions avec les murs, puis les collisions entre
    les particules.
    """
    for _ in range(num_steps):
        for particle in particles:
            update_position3D(particle, dt)
            check_wall_collision3D(particle, wall_size)
        check_particle_collision3D(particles)

if __name__ == "__main__":

    # Initial conditions
    wall_size_3D = 10
    num_steps_3D = 100
    dt_3D = 0.01
    T_3D = 20
    nb_molecule_a_3D = 300
    nb_molecule_b_3D = 100
    masse_molecule_3D = 1e-9
    facteur_3D = 1000

    while True:
        wall_size_3D = get_input("Entrez la valeur de la taille de l'enceine", default_value=80, value_type=int, min_value=0)
        T_3D = get_input("Entrez la valeur de la température", default_value=20, value_type=float, min_value=-273.15)
        num_steps_3D  = get_input("Entrez le nombre d'étapes", default_value=100, value_type=int, min_value=10, max_value=5000)
        nb_molecule_a_3D_3D  = get_input("Entrez le nombre de molécules du gaz environnant", default_value=500, value_type=int, min_value=10, max_value=5000)
        nb_molecule_b  = get_input("Entrez le nombre de molécules du gaz à diffuser", default_value=80, value_type=int, min_value=10, max_value=5000)
        facteur_3D = get_input("Entrez le nombre facteur", default_value=100, value_type=int, min_value=1, max_value=1e6)
        dt_3D = get_input("Entrez le delta t", default_value=0.5, value_type=float, min_value=1e-6, max_value=10)
        save_anim_3D = get_input("Voulez vous enregistrer l'animation", default_value=False, value_type=bool)
       

        if save_anim_3D:
            save_name_3D = get_input("Entrez le nom : ", default_value=False, value_type=str)
            anim_mp4_3D = get_input("Voulez vous enregistrer l'animation en MP4 (sinon elle sera en .gif)", default_value=False, value_type=bool)
            fps_3D = get_input("Entrez la valeur du fps", default_value=30, value_type=int, min_value=10, max_value=120)


        e_c_moy = 3*(1.38e-23)*(273.15+T_3D)/2
        vitesse_moyenne = np.sqrt(2*e_c_moy*6.022e23/18e-3)
        
        particles = []

        #On calcule la vitesse moyenne des groupements H2O
        for i in range(nb_molecule_a_3D):
            v = np.random.normal(vitesse_moyenne, 0.1*vitesse_moyenne, facteur_3D)
            theta = np.random.uniform(0, 2*np.pi, facteur_3D)
            phi = np.random.uniform(0, np.pi, facteur_3D)
            
            vx_g = np.mean((v * np.sin(phi) * np.cos(theta)) / facteur_3D)
            vy_g = np.mean((v * np.sin(phi) * np.sin(theta)) / facteur_3D)
            vz_g = np.mean((v * np.cos(phi)) / facteur_3D)



            #On cree les molécules du gaz ambiant
            particles.append(Particle3D(mass=masse_molecule_3D, radius=0.5,
                                        x=random.uniform(1, wall_size_3D - 1),
                                        y=random.uniform(1, wall_size_3D - 1),
                                        z=random.uniform(1, wall_size_3D - 1),
                                        vx=vx_g, vy=vy_g, vz=vz_g))

        for i in range(nb_molecule_b):
            v = np.random.normal(vitesse_moyenne, 0.1*vitesse_moyenne, facteur_3D)
            theta = np.random.uniform(0, 2*np.pi, facteur_3D)
            phi = np.random.uniform(0, np.pi, facteur_3D)
            
            vx_g = np.mean((v * np.sin(phi) * np.cos(theta))/ facteur_3D)
            vy_g = np.mean((v * np.sin(phi) * np.sin(theta)) / facteur_3D)
            vz_g = np.mean((v * np.cos(phi)) / facteur_3D)


            #On cree les molécules du gaz diffusé
            particles.append(Particle3D(mass=masse_molecule_3D, radius=0.5,
                                        x=random.uniform(wall_size_3D/2 - 0.2*wall_size_3D, wall_size_3D/2 +  0.2*wall_size_3D),
                                        y=random.uniform(wall_size_3D/2 - 0.2*wall_size_3D, wall_size_3D/2 +  0.2*wall_size_3D),
                                        z=random.uniform(wall_size_3D/2 - 0.2*wall_size_3D, wall_size_3D/2 +  0.2*wall_size_3D),
                                        vx=vx_g, vy=vy_g, vz=vz_g))


        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim(0, wall_size_3D)
        ax.set_ylim(0, wall_size_3D)
        ax.set_zlim(0, wall_size_3D)

        #On affiche les points et la trajectoire du pollen
        scatters = [ax.plot([], [], [], 'yo')[0] if i > nb_molecule_a_3D else ax.plot([], [], [], 'bo')[0] for i in range(len(particles))]

        #On cree une animation
        ani = FuncAnimation(fig, animate3D, frames=num_steps_3D, fargs=(particles, wall_size_3D, dt_3D), interval=10, blit=True)
        
        if save_anim_3D:
                """
                Si l'utilisateur a choisi l'option de sauvegarde, on enregistre l'animation en fichier MP4 ou en Gif
                """
                if anim_mp4_3D:
                    matplotlib.rcParams['animation.ffmpeg_path'] = "ffmpeg-6.1-essentials_build\\bin\\ffmpeg.exe"
                    writervideo = FFMpegWriter(fps=fps_3D, bitrate=1800)
                    ani.save(f"{save_name_3D}.mp4", writer=writervideo, progress_callback=progress_callback)
                else:
                    ani.save(f"{save_name_3D}.gif", dpi=300, progress_callback=progress_callback, writer=PillowWriter(fps=fps_3D))

        #On affiche l'animation
        plt.show()

        #On donne la possibilité à l'utilisateur de refaire une autre simulation sans quitter le programme
        recommencer = get_input("\nVoulez vous recommencer", default_value=True, value_type=bool)

        if recommencer == False:
            break
        else:
            print("\n\n")
