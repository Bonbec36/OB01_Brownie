import pygame
import random
import math



class ParticuleAlpha:
    def __init__(self, taille, position,  vitesse, hitbox):
        self.taille = taille
        self.position = position
        self.vitesse = vitesse
        self.hitbox = hitbox

    def print(self):
        print(f"Taille :  {self.taille}\nPosition : {self.position[0]}, {self.position[1]}\n"
              f"Vitesse : {self.vitesse[0]}, {self.vitesse[1]}\nHitbox : {self.hitbox}\n")
        
    def Prochaine_position(self, dt):
        self.position[0] = self.position[0] + self.vitesse[0] * dt
        self.position[1] =  self.position[1] + self.vitesse[1] * dt
        return self

    def draw(self, screen):
        pygame.draw.circle(screen, "red", pygame.Vector2(self.position[0], self.position[1]), self.taille)



SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500


# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
clock = pygame.time.Clock()
running = True
dt = 0

liste_particule_alpha = [ParticuleAlpha(10, [random.randint(50, 450), random.randint(50, 450)], [random.randint(0, 5), random.randint(0, 5)], [10]) for i in range(50)]

while running:
    pygame.time.delay(1000)
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    
    screen.fill("purple")

    for p_alpha in liste_particule_alpha:
        p_alpha.Prochaine_position(0.05)

        if p_alpha.position[0] < 0:
            p_alpha.position[0] = 0
        if p_alpha.position[0] + p_alpha.taille > SCREEN_WIDTH:
            p_alpha.position[0] = SCREEN_WIDTH - p_alpha.taille
        if p_alpha.position[1] < 0:
            p_alpha.position[1] = 0
        if p_alpha.position[1]+ p_alpha.taille > SCREEN_HEIGHT:
            p_alpha.position[1] = SCREEN_HEIGHT - p_alpha.taille
            
        p_alpha.draw(screen)

        angle = math.atan2(p_alpha.position[1] + p_alpha.taille/2 - SCREEN_HEIGHT/2, p_alpha.position[0] + p_alpha.taille/2 - SCREEN_WIDTH/2)


        if p_alpha.position[0] <= 0 or p_alpha.position[0] + p_alpha.taille >= SCREEN_WIDTH:
            angle = math.pi - angle
        if p_alpha.position[1] <= 0 or p_alpha.position[1] + p_alpha.taille >= SCREEN_HEIGHT:
            angle = -angle

        p_alpha.vitesse[0] = p_alpha.vitesse[0] * math.cos(angle)
        p_alpha.vitesse[1] = p_alpha.vitesse[1] * math.sin(angle)

        # Met à jour la position de l'objet en fonction de l'angle de rebond
        p_alpha.position[0] += p_alpha.vitesse[0] * math.cos(angle)
        p_alpha.position[1] -= p_alpha.vitesse[1] * math.sin(angle)




    pygame.display.flip()

pygame.quit()