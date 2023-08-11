"""
 This code example is in the public domain. 
 http://www.botnroll.com

 Description:  
 This program detects automatic start and does the automatic end on the RoboParty Fun Challenge.

"""

import time
from one import BnrOneA

one = BnrOneA(0, 0)    # declaration of object variable to control the Bot'n Roll ONE A

counter = 0 
challenge_time = 90   # challenge time

estado = 0
media = 0.0
sensor = [0] * 8

def setup():
    on = 1
    off = 0
    one.stop()                      # stop motors
    initialize_timer()              # configures the interrupt timer for the end of the challenge
    one.lcd1("FUN CHALLENGE")       # print on LCD line 1
    one.lcd2("READY TO START..")    # print on LCD line 2
    one.obstacle_emitters(off)      # deactivate obstacles IR emitters
    time.sleep(4)                   # time to stabilize IR sensors (DO NOT REMOVE!!!)
    start = 0
    while(not start):
        start = automatic_start()

    TIMSK1 |= (1 << OCIE1A)         # enable timer compare interrupt
    one.obstacle_emmitters(on)      # deactivate obstacles IR emitters

def automatic_start():
    active = one.read_ir_sensors()          # read IR sensors
    result = False
    if not active:                          # If not active
        tempo_A = time.time()               # read time
        while not active:                   # while not active
            active = one.read_ir_sensors()  # read actual IR sensors state
            elapsed_time = time.time() - tempo_A
            if elapsed_time > 0.050:        # if not active for more than 50ms
                result = True               # start Race
                break
    return result


def initialize_timer():
    #set timer1 interrupt at 1Hz


def ISR(TIMER1_COMPA_vect):                 # timer1 interrupt 1Hz
  
    if (counter >= challenge_time):
        one.lcd2("END OF CHALLENGE")        # print on LCD line 2
        while(True)                         # does not allow anything else to be done after the challenge ends
            one.brake(100, 100)             # Stop motors with torque
            # place code here, to stop any additional actuators... 
    else:
        one.lcd2(counter)                   # print the challenge time on LCD line 2
        counter += 1


def loop():
    media = 0
    #para ler os sensores de linha
    for i in range(8) 
        sensor[i] = one.readAdc(i)
        media += (sensor[i] / 8)

    # sensor[0] é o valor do sensor 0
    # sensor[1] é o valor do sensor 1
    # ...
    # media é o valor médio dos 8 sensores de linha

    # Este exemplo é baseado numa máquina de estados.
    # Cada estado simboliza uma tarefa diferente que o robô tem que fazer,
    # seja andar para a frente ou andar para trás.
    # Os 'if' no fim de cada estado simbolizam as condições 
    # que fazem com que o robô altere a tarefa que está a fazer.
    # Por exemplo se o robô estiver na tarefa de ir em frente e se detectar um obstáculo,
    # altera o seu estado/tarefa para andar para trás

    if(estado == 0): #anda para a frente até detetar linha de meio campo ou sensores obstaculos
        one.move(80, 80)
        # se detetar algum obstáculo, altera a tarefa para andar para trás
        if(one.obstacleSensors() > 0):
            estado = 1

        # se detetar uma media dos sensores acima de 900 (todos os sensores a preto), altera a tarefa para andar para trás
        if(media > 900):
            estado = 1

    elif(estado == 1): # anda para tras até os sensores estarem na parte branca
        one.move(-80, -80)
        # se detetar uma media dos sensores abaixo de 100 (todos os sensores a branca), 
        # altera a tarefa para andar para trás mas fica à espera que o robô seja levantado
        if(media < 100):
            estado = 2

    elif(estado == 2): #anda para trás até ser levantado
        one.move(-80, -80)
        # se detetar uma media dos sensores acima de 900 (todos os sensores a preto), altera a tarefa para andar para a frente
        # o que significa que o robô foi levantado
        if(media > 900):
            estado = 3
        
    elif(estado == 3): # anda para a frente até os sensores estarem na parte branca (robô ser pousado na pista)
        one.move(80, 80)
        # se detetar uma media dos sensores abaixo de 100 (todos os sensores a branca), 
        # altera a tarefa para andar para a frente mas fica à espera que o robô detete um obstáculo ou a linha de meio campo
        if(media < 100):
            estado = 0


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
