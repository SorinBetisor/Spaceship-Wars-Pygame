import pygame
import os #operating system
pygame.font.init() #initializeaza bibloteca font pentru text din pygame
pygame.mixer.init()#initilializeaza biblioteca pentru sunet din pygame

WIDTH,HEIGHT = 900,500 #rezolutia
WIN = pygame.display.set_mode((WIDTH,HEIGHT)) #porneste fereastra

pygame.display.set_caption("Caunter Strik Local Ofensiv") #da numele ferestrei

WHITE= (255,255,255) #codul rgb pentru culoarea alba
BLACK= (0,0,0) #rgb negru
RED=(255,0,0) #rosu
YELLOW=(255,255,0) #galben

BORDER = pygame.Rect(WIDTH//2 -5, 0, 10, HEIGHT) #delimitatorul de la mij ecranului

BULLET_HIT_SOUND=pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3')) #loading la sunet pentru cand nimereste
BULLET_FIRE_SOUND=pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3')) #sunat pentru fire

YELLOW_HIT = pygame.USEREVENT +1 #custom user event pentru hit +1 +2 defineste eventul ca id [just a number]
RED_HIT = pygame.USEREVENT +2

FPS = 60
VEL = 5  #Velocity (viteza cu care se misca personajul)
BULLET_VEL = 7 #vel pentru projectiles
MAX_BULLETS = 4 #nr maxim de proiectile pe jucator

HEALTH_FONT= pygame.font.SysFont('comicsans', 40) #defining fontul pentru text cu fontul si marimea ca argument
WINNER_FONT= pygame.font.SysFont('comicsanc',100) #font pentru castig

SPACESHIP_WIDTH, SPACESHIP_HEIGHT= 55,44 #dimensiunile pentru personaje

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join(
    'Assets','spaceship_yellow.png')) #importeaza imaginea pentru naveta galbena, cu pathul catre imagine ca argument
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90) #face resize la imagine, cu dimensiunile ca argument +rotatia

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join(
    'Assets','spaceship_red.png'))
RED_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)) ,270)

SPACE= pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')), (WIDTH,HEIGHT)) #Backgroundul + resizing

def draw_window(red, yellow, red_bullets, yellow_bullets,red_health,yellow_health): #functia pentru a desena pe windowul jocului
    #WIN.fill(WHITE) #da ferestrei o culoare de background
    WIN.blit(SPACE,(0,0)) #deseneaza backgroundul la 0 0
    pygame.draw.rect(WIN, BLACK, BORDER ) #desenarea la delimitatorul de la mij ecranului

    red_health_text= HEALTH_FONT.render('Viata: '+str(red_health),1,WHITE) #variabila pentru render la text
    yellow_health_text=HEALTH_FONT.render('Viata: '+str(yellow_health),1,WHITE)
    WIN.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10,10)) #deseneaza textul pentru viata la marginea din dreapta
    WIN.blit(yellow_health_text,(10,10)) #pentru marginea din stanga


    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))      #deseneaza imaginea pe ecran, cu pozitia lui ca argument
    WIN.blit(RED_SPACESHIP,(red.x, red.y))                # *pozitia este definita in functia main ca argumente a red,yellow
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)  #deseneaza proiectilele

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)
    pygame.display.update()  #updateaza displayul jocului [cu culoarea alba]



def yellow_handle_movement(keys_pressed, yellow):  #FUNCTIE PT MISCAREA 1 PERSONAJ (GALBEN) +borders
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #STANGA si verifica sa nu iasa din ecran
        yellow.x-= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #DREAPTA si verifica sa nu atinga delimitatorul
        yellow.x+= VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #SUS + verificare ecran
        yellow.y-= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT -15: #JOS + verificare ecran [- pentru perfectiune]
        yellow.y+= VEL

def red_handle_movement(keys_pressed, red):  #FUNCTIE PT MISCAREA 2 PERSONAJ (ROSU) +borders
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #STANGA + delimitator 
        red.x-= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #DREAPTA +border
        red.x+= VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #SUS +border
        red.y-= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT -15: #JOS +border
        red.y+= VEL

def handle_bullets(yellow_bullets,red_bullets,yellow,red): #functia p/u miscare si collide proiectile
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL #se misca spre dreapta cu bullet_vel
        if red.colliderect(bullet): #functie in pygame care verifica collide intre red si proiectilul impuscat de yellow [merge doar cu rectangles]
            pygame.event.post(pygame.event.Event(RED_HIT)) #verifica daca jucatorul rosu a fost lovit dupa custom event
            yellow_bullets.remove(bullet) #daca sa atinge sa se stearga
        elif bullet.x > WIDTH:  #verifica daca iese din ecran
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL 
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x<0:
            red_bullets.remove(bullet)

def draw_winner(text): #functia pentru a desena text la castig
    draw_text = WINNER_FONT.render(text,1,WHITE) #variabila pentru render la textul de castig
    WIN.blit(draw_text,(WIDTH//2 - draw_text.get_width()/2, HEIGHT//2 - draw_text.get_height()/2)) #deseneaza si pozitioneaza textul
    pygame.display.update() #updateaza displayul
    pygame.time.delay(5000) #delay cu 5000 ms

def main(): #functia main
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) #introduce un patrat care va reprezenta fiecare personaj
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = [] # listele pentru proiectile

    red_health=10
    yellow_health=10 #variabilele [neconstante] pentru viata jucatorului

    clock = pygame.time.Clock() #controleaza viteza lui while (cu FPSU) [C cu litera mare]
    run = True
    while run:
        clock.tick(FPS) #FPS
        for event in pygame.event.get(): #verifica actiunile/eventele din joaca
            if event.type == pygame.QUIT: #eventul pentru iesire
                run=False
                pygame.quit() 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS: #verifica daca butonul pentru 
             #impuscat este apasat si daca nu se depaseste numarul maxim de proiectile permise pe ecran
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5) #plasarea proiectilelor [x,y]
                    yellow_bullets.append(bullet)                                        #argumentele 10 , 5 sunt pentru marimea proiectilului
                    BULLET_FIRE_SOUND.play()#porneste sunetul

                if event.key == pygame.K_RCTRL and len(red_bullets)< MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)  
                    BULLET_FIRE_SOUND.play() #porneste sunetul
            if event.type == RED_HIT: #scade variabila pentru viata in caz ca a fost nimerit
                red_health-=1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health-=1
                BULLET_HIT_SOUND.play()

        winner_text=""     #verifica castigatorul
        if red_health<=0:
            winner_text="Galben castiga!"
        
        if yellow_health<=0:
            winner_text="Rosu castiga!"
        
        if winner_text !="":
            draw_winner(winner_text)
            break

        keys_pressed= pygame.key.get_pressed() #verifica care key de pe tastatura este apasat
        yellow_handle_movement(keys_pressed, yellow) #calling the function for movement [yellow]
        red_handle_movement(keys_pressed, red) #functia pt miscare rosu
        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health) #calling the function for drawing the rectangles
        handle_bullets(yellow_bullets,red_bullets,yellow,red) #functia pt miscare proiectil +collide

    #pygame.quit() 
    main()



if __name__ == "__main__":  #important pentru a tine aprins
    main()