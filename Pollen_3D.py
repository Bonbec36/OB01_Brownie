import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter
import matplotlib
import random
from mpl_toolkits.mplot3d import Axes3D

class Particle:
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

def update_position(particle, dt):
    particle.x += particle.vx * dt
    particle.y += particle.vy * dt
    particle.z += particle.vz * dt
    #particle.trajectory.append((particle.x, particle.y, particle.z))
    if len(particle.trajectory) < 50:
        particle.trajectory.append((particle.x, particle.y, particle.z))
    else: 
        del particle.trajectory[0]
        particle.trajectory.append((particle.x, particle.y, particle.z))



def check_wall_collision(particle, wall_size):
    if particle.x - particle.radius < 0 or particle.x + particle.radius > wall_size:
        particle.vx *= -1
    if particle.y - particle.radius < 0 or particle.y + particle.radius > wall_size:
        particle.vy *= -1
    if particle.z - particle.radius < 0 or particle.z + particle.radius > wall_size:
        particle.vz *= -1

def check_particle_collision(particles):
    global nu
    for i in range(len(particles)):
        for j in range(i+1, len(particles)):
            particle1 = particles[i]
            particle2 = particles[j]
            distance = np.sqrt((particle1.x - particle2.x)**2 + (particle1.y - particle2.y)**2 + (particle1.z - particle2.z)**2)
            if distance <= particle1.radius + particle2.radius:
                angle = np.arctan2(particle2.y - particle1.y, particle2.x - particle1.x)
                v1 = np.sqrt(particle1.vx**2 + particle1.vy**2 + particle1.vz**2)
                v2 = np.sqrt(particle2.vx**2 + particle2.vy**2 + particle2.vz**2)

                theta1 = np.arctan2(particle1.vy, particle1.vx)
                theta2 = np.arctan2(particle2.vy, particle2.vx)

                phi = angle
                m1 = particle1.mass
                m2 = particle2.mass

                particle1.vx = nu*(v2 * np.cos(theta2 - phi) * np.cos(phi) + v1 * np.sin(theta1 - phi) * np.cos(phi + np.pi/2))
                particle1.vy = nu*(v2 * np.cos(theta2 - phi) * np.sin(phi) + v1 * np.sin(theta1 - phi) * np.sin(phi + np.pi/2))
                particle1.vz = nu*particle2.vz  # No change in the z-component

                particle2.vx = nu*(v1 * np.cos(theta1 - phi) * np.cos(phi) + v2 * np.sin(theta2 - phi) * np.cos(phi + np.pi/2))
                particle2.vy = nu*(v1 * np.cos(theta1 - phi) * np.sin(phi) + v2 * np.sin(theta2 - phi) * np.sin(phi + np.pi/2))
                particle2.vz = nu*particle1.vz  # No change in the z-component

def update(frame, particles, wall_size, dt):
    simulate_collision(particles, wall_size, 1, dt)
    x_values = [particle.x for particle in particles]
    y_values = [particle.y for particle in particles]
    z_values = [particle.z for particle in particles]
    #sc._offsets3d = (x_values, y_values, z_values)
    #sc.set_array(np.array([particle.get_Energie_cinetique() for particle in particles]))

    for i, scatter in enumerate(scatters):
        scatter.set_data(x_values[i], y_values[i])  # Met à jour les positions en x et y
        scatter.set_3d_properties(z_values[i])


    total_energy = sum([particle.mass * particle.get_Energie_cinetique() for particle in particles])
    #print(f"Énergie totale du système à l'étape {frame + 1}: {total_energy}")

    line.set_data(*zip(*[(x, y) for x, y, _ in particles[-1].trajectory]))
    line.set_3d_properties([z for _, _, z in particles[-1].trajectory])


    return scatters + [line]

def simulate_collision(particles, wall_size, num_steps, dt):
    for _ in range(num_steps):
        for particle in particles:
            update_position(particle, dt)
            check_wall_collision(particle, wall_size)
        check_particle_collision(particles)

if __name__ == "__main__":
    # Initial conditions
    wall_size = 10

    particles = [Particle(mass=1, radius=0.1, x=random.randint(1, 9), y=random.randint(1, 9), z=random.randint(1, 9),
                          vx=(random.randint(-100, 100)/10), vy=(random.randint(-100, 100)/10), vz=(random.randint(-100, 100)/10)) for i in range(100)]
    particles.append(Particle(mass=100, radius=0.5, x=5, y=5, z=5, vx=0, vy=0, vz=0))

    # Simulation parameters
    num_steps = 500
    dt = 0.1
    nu = 1

    # Plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(0, wall_size)
    ax.set_ylim(0, wall_size)
    ax.set_zlim(0, wall_size)

    #sc = ax.scatter([particle.x for particle in particles], [particle.y for particle in particles], [particle.z for particle in particles], s=[particle.radius*200 for particle in particles])
    scatters = [ax.plot([], [], [], 'yo')[0] if i == len(particles) - 1 else ax.plot([], [], [], 'bo')[0] for i in range(len(particles))]
    line, = ax.plot([], [], [], 'r', lw=2)

    ani = FuncAnimation(fig, update, frames=num_steps, fargs=(particles, wall_size, dt), interval=10, blit=True)
    matplotlib.rcParams['animation.ffmpeg_path'] = "ffmpeg-6.1-essentials_build\\bin\\ffmpeg.exe"
    writervideo = FFMpegWriter(fps=30, bitrate=1800)
    #ani.save("Pollen_3D_01.mp4", writer=writervideo)
    plt.show()