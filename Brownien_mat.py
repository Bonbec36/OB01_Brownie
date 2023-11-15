import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
import random


class ParticuleAlpha:
    def __init__(self, taille, masse, position,  vitesse, hitbox):
        self.taille = taille
        self.masse = masse
        self.position = position
        self.vitesse = vitesse
        self.hitbox = hitbox

    def print(self):
        print(f"Taille :  {self.taille}\nPosition : {self.position[0]}, {self.position[1]}\n"
              f"Vitesse : {self.vitesse[0]}, {self.vitesse[1]}\nHitbox : {self.hitbox}\n")

    def get_hitbox_square(self):
        print("allo")
        
        
    def Prochaine_position(self, dt, x_min, y_min, x_max, y_max):
        if self.position[0] <= x_min or self.position[0] >= x_max:
            self.vitesse[0] = - self.vitesse[0]
        elif self.position[1] <= y_min or self.position[1] >=y_max:
            self.vitesse[1] = -self.vitesse[1]
        self.position[0] = self.position[0] + self.vitesse[0] * dt
        self.position[1] = self.position[1] + self.vitesse[1] * dt
        return self

    def detecter_collision(self, autre_particule):
        distance = np.linalg.norm(np.array(self.position) - np.array(autre_particule.position))
        rayon_total = self.taille + autre_particule.taille
        return distance < rayon_total

    def gerer_collision(self, autre_particule):
        rayon_total = self.taille + autre_particule.taille
        direction = np.array(self.position) - np.array(autre_particule.position)
        direction_normalisee = direction / np.linalg.norm(direction)
        vitesse_relative = np.array(self.vitesse) - np.array(autre_particule.vitesse)
        produit_scalaire = np.dot(vitesse_relative, direction_normalisee)
        impulsion = (2 * self.masse * autre_particule.masse * produit_scalaire) / ((self.masse + autre_particule.masse) * rayon_total)
        nouvelle_vitesse_self = np.array(self.vitesse) - impulsion * direction_normalisee
        nouvelle_vitesse_autre = np.array(autre_particule.vitesse) + impulsion * direction_normalisee

        self.vitesse = nouvelle_vitesse_self.tolist()
        autre_particule.vitesse = nouvelle_vitesse_autre.tolist()


plt.close('all')
colors = [ 'teal']

cercle1 = plt.Circle((0, 0), 0.2, color='r')


fig_animate, ax = plt.subplots()
dots = []

x_min, y_min = 0, 0
x_max, y_max = 100, 100

ax.set_xlim([0,100])
ax.set_ylim([0,100])



data=np.round(3*np.sin(np.linspace(0,6*np.pi,100))+5)

liste_particule_alpha = [ParticuleAlpha(1, 1, [random.randint(-1, 90), random.randint(-1, 90)], [random.randint(0, 500), random.randint(0, 500)], [10]) for i in range(50)]


x = [part.position[0] for part in liste_particule_alpha]
y = [part.position[1] for part in liste_particule_alpha]

points = plt.scatter(x, y, 5, 'r')

def animate(z):
    global points, x_min, y_min, x_max, y_max
    points.remove()
    #x = data[z]
    #y = data[z]
    for i, particule in enumerate(liste_particule_alpha):
        particule.Prochaine_position(0.01, x_min, y_min, x_max, y_max)
        # Vérifiez les collisions avec les autres particules
        for autre_particule in liste_particule_alpha[i+1:]:
            if particule.detecter_collision(autre_particule):
                particule.gerer_collision(autre_particule)
    
    x = [part.position[0] for part in liste_particule_alpha]
    y = [part.position[1] for part in liste_particule_alpha]
    points = plt.scatter(x, y, 5, 'r')
    return x, y

anim = animation.FuncAnimation(fig_animate, animate, frames=len(data), blit=False, interval=1)

ax.set_facecolor('#d3d3d3')
plt.show()