"""
    
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
import matplotlib
import random

class Particle:
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

def update_position(particle, dt):
    particle.x += particle.vx * dt
    particle.y += particle.vy * dt
    particle.trajectory.append((particle.x, particle.y)) 

def check_wall_collision(particle, wall_size):
    if particle.x - particle.radius < 0 or particle.x + particle.radius > wall_size:
        particle.vx *= -1
    if particle.y - particle.radius < 0 or particle.y + particle.radius > wall_size:
        particle.vy *= -1

def check_particle_collision(particles):
    global nu
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
    simulate_collision(particles, wall_size, 1, dt)
    x_values = [particle.x for particle in particles]
    y_values = [particle.y for particle in particles]
    sc.set_offsets(np.array([x_values, y_values]).T)

    total_energy = sum([particle.mass * particle.get_Energie_cinetique() for particle in particles])
    print(f"Énergie totale du système à l'étape {frame + 1}: {total_energy}")

    line.set_data(*zip(*particles[-1].trajectory))
    
    return sc, line

def simulate_collision(particles, wall_size, num_steps, dt):
    for _ in range(num_steps):
        for particle in particles:
            update_position(particle, dt)
            check_wall_collision(particle, wall_size)
        check_particle_collision(particles)

if __name__ == "__main__":
    # Initial conditions
    wall_size = 20
    nu = 1
    
    """
    particles = [
        Particle(mass=1, radius=0.1, x=2, y=5, vx=1, vy=0.5),
        Particle(mass=1, radius=0.1, x=2, y=3, vx=-1, vy=-0.5),
        Particle(mass=1, radius=0.1, x=5, y=8, vx=-0.5, vy=-1),
        # Ajoutez autant de particules que nécessaire
    ]"""

    particles = [Particle(mass=3e-5, radius=0.05, x=random.randint(1,wall_size - 1),  y=random.randint(1,wall_size -1), vx = (random.randint(-100,100)/10), vy = (random.randint(-100,100)/10), color="blue") for i in range(200)]
    particles.append(Particle(mass=1e-3, radius=2.3, x=wall_size/2, y=wall_size/2, vx=0, vy=0, color='#2EFF00')) #20 à 55 μm taille moyenne d'un grain de pollen

    # Simulation parameters
    num_steps = 100
    dt = 0.1

    # Plotting
    fig, ax = plt.subplots()
    ax.set_xlim(0, wall_size)
    ax.set_ylim(0, wall_size)
    plt.title("Modelisation d'un grain de pollen dans un fluide (2D)")
    ax.set_aspect('equal', adjustable='box')
    sc = ax.scatter([particle.x for particle in particles], [particle.y for particle in particles], s=[particle.radius*200 for particle in particles], c=[particle.color for particle in particles])

    line, = ax.plot([], [], '#2EFF00', lw=2)

    ani = FuncAnimation(fig, update, frames=num_steps, fargs=(particles, wall_size, dt), interval=10, blit=True)
    matplotlib.rcParams['animation.ffmpeg_path'] = "ffmpeg-6.1-essentials_build\\bin\\ffmpeg.exe"
    writervideo = FFMpegWriter(fps=30, bitrate=1800)
    #ani.save("Pollen_2D.mp4", writer=writervideo)
    plt.show()

