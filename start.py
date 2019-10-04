import pygame, sys, time, math
from pygame.math import Vector2
from planet import Body
from itertools import permutations
import logging

class Game():

    def __init__(self):
        #config
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        self.tps_max = 2000.0

        pygame.init()
        self.screen = pygame.display.set_mode((1880,1020))
        self.tps_clock = pygame.time.Clock()
        self.tps_delta = 0.0

        bodies_amount = 4
        self.player1 = Body(self, (280, 250),(0,0), 10, 10, (255,255,0))
        self.player2 = Body(self, (300, 300),(0,0), 20, 20, (0,0,255))
        self.player3 = Body(self, (400, 640),(0,0), 30, 30, (255,0,255))
        self.player4 = Body(self, (100, 900),(0,0),400, 40, (0,255,0))

        self.bodies = [getattr(self, f"player{i+1}") for i in range(bodies_amount)]

        logging.info('Printing list of bodies: ' + str(self.bodies))


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)

            self.tps_delta += self.tps_clock.tick()/ 1000.0
            while self.tps_delta > 1 / self.tps_max:
                self.tick()
                self.tps_delta -= 1 / self.tps_max

            self.screen.fill((0,0,0))
            self.draw()
            pygame.display.flip()
            self.cal_force()
            # time.sleep(1.5)


    def tick(self):
        logging.info('tick func exec')
        for i in self.bodies:
            i.tick()

    def draw(self):
        logging.info('draw func exec')
        for i in self.bodies:
            logging.info(str(i) + 'Printing')
            i.draw()

    def cal_force(self):
        logging.info('cal_force function exec!')
        forces = []
        vectors = []
        logging.info('length of bodies: ' + str(len(self.bodies)))

        for i in self.bodies:
            for j in self.bodies:
                a = math.sqrt(((i.y - j.y)**2) +((i.x - j.x)**2))
                if a == 0:
                    continue
                else:
                    print(a)
                    if a < 100:
                        force = i.mass * j.mass * 0.005 / a
                    else:
                        force = i.mass * j.mass * 0.0005 / a
                    forces.append(force)

        for i in self.bodies:
            for j in self.bodies:
                vector = Vector2((i.x - j.x),(i.y - j.y))
                if vector == Vector2(0,0):
                    continue
                else:
                    vectors.append(vector)

        forces_seq = [forces[i:i+len(self.bodies)-1] for i in range(0, len(forces),len(self.bodies)-1)]
        vectores_seq = [vectors[i:i+len(self.bodies)-1] for i in range(0, len(vectors),len(self.bodies)-1)]
        collabo = zip(forces_seq, vectores_seq)

        temp = []
        for j,k in collabo:
            collabo2 = zip(j,k)
            for a,b in collabo2:
                temp.append((a,b))
        logging.info(temp)

        forces_arr = []

        for i in range(len(temp)):
            a = temp[i][0] * temp[i][1]
            forces_arr.append(a)

        logging.info('Vectors before adding',forces_arr)

        vectors_arr = []

        for i in range(0,len(forces_arr)-1,len(self.bodies)-1):
            a = forces_arr[i] + forces_arr[i+1]
            vectors_arr.append(a)

        logging.info('Vectors after adding',vectors_arr)

        j = 0

        for i in self.bodies:
            if(j <= len(self.bodies)-1):
                logging.info('Applaying', vectors_arr[j], 'to', i)
                i.add_force(vectors_arr[j]/i.mass)
                j += 1
            else:
                j = 0
                break

if __name__ == "__main__":
    Game()
