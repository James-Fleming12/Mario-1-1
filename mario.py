import pygame

# TO DO 
# koopas
# collision with enemies to eachother, enemy clipping when moving camera left and right, correct flag collision

class Goomba: 
    x, y = 0, 0
    origX, origY = 0, 0
    left = True
    deathTimer = 50
    dead = False
    velocity = 0; acceleration = 0.3

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.origX = x 
        self.origY = y

class Mushroom: 
    x, y = 0, 0
    left = False 
    velocity = 0; acceleration = 0.3

    def __init__(self, x, y): 
        self.x = x
        self.y = y 

class Block: 
    x, y  = 0, 0
    coins = 0
    hit = False; timer = 10
    pipe = False
    def __init__(self, x, y, coins, pipe): 
        self.x = x
        self.y = y
        self.coins = coins
        self.pipe = pipe

class ItemBlock(Block): 
    item = ""
    timer = 10
    hit = False
    def __init__(self, x, y, item):
        self.x = x
        self.y = y
        self.item = item

class Score: 
    x, y = 0, 0
    amount = 0
    timer = 20

    def __init__(self, x, y, amount):
        self.x = x
        self.y = y
        self.amount = amount

class Coin: 
    x, y = 0, 0
    timer = 10 
    animation = False
    def __init__(self, x, y, animation):
        self.x = x
        self.y = y
        self.animation = animation

class Pipe: 
    x, y = 0, 0
    underground = False
    def __init__(self, x, y, underground):
        self.x = x
        self.y = y
        self.height = height
        self.underground = underground

class Flag: 
    x = 0
    y = 80
    def __init__(self, x):
        self.x = x 

pygame.init()
pygame.display.set_caption("Mario")
screen = pygame.display.set_mode((1100, 720))
clock = pygame.time.Clock()
lives = 3
startScreen = True ; starttimer = 100 ; gameplay = False; gameover = False; finish = False
running = True; animation = False
enterPipe = False; exitPipe = False; dieAni = False; flagAni = False; aniIterations = 0
myFont = pygame.font.SysFont("monofetti", 90); MyFont2 = pygame.font.SysFont("monofetti", 50); MyFont3 = pygame.font.SysFont("monofetti", 150)
height = 100; state = 1 # 2 is with mushroom, 1 is without 
iFrames = 0 
moveLeft = False; moveRight = False
playerX = 150; playerY = 700-height; left = False; right = False; jump = False; down = False
velocity, acceleration, grounded = 0, 0.3, True
moveSpeed = 7; jumpIterations = 0; pipeX = 0; overPipeX = 0; overPipeY = 0
yWall = 0; yWall = 0
coinCount = 0
flag = Flag(0)
blocks = [] ; enemies = [] ; items = [] ; scores = [] ; coins = []
underground = False; underblocks = []; undercoins = []
layout = [ # 1 are blocks, 2 are goombas, 3 is block with mushroom, 4 is block with 5 coins, 5 is pipe head (continues to the bottom by itself), 6 is pipebody, 7 is flag
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 4, 3, 4, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 6, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 6, 0, 0, 0, 6, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 7, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 2, 0, 6, 0, 2, 0, 6, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
underlayout = [ # 1 are blocks, 2 are coins, 3 are pipe bodies, 4 are pipe heads
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
[1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 1],
[1, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 1],
[1, 0, 0, 2, 2, 2, 2, 2, 0, 0, 4, 1],
[1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 3, 1],
[1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 3, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def refresh(): 
    global blocks, enemies, underblocks, undercoins
    global coinCount, playerX, playerY, yWall, yWall2
    global starttimer, dieAni, animation, aniIterations 
    global state, height, gameover, startScreen, items
    blocks = []; enemies = []; underblocks = []; undercoins = []; items = []
    playerX = 150; playerY = 700-height
    coinCount = 0
    starttimer = 100 
    yWall = 0
    animation = False ; dieAni = False
    height = 100; state = 1
    if lives == 0:
        startScreen = False
        gameover = True
    for index, x in enumerate(layout): # making the layout array usable
        for index2, y in enumerate(x): 
            if y == 1: 
                temp = Block(index2*100, (index*100) - 120, 0, False)
                blocks.append(temp)
            if y == 2: 
                temp = Goomba(index2*100, (index*100) - 120)
                enemies.append(temp)
            if y == 3: 
                temp = ItemBlock(index2*100, (index*100) - 120, "Mushroom")
                blocks.insert(0, temp) # so that collision underneath the block is first, avoids issues of overlaying with other blocks
            if y == 4: 
                temp = Block(index2*100, (index*100) - 120, 5, False)
                blocks.append(temp)
            if y == 5: 
                temp = Pipe(index2*100, (index*100) - 120, False)
                blocks.append(temp)
            if y == 6: 
                temp = Block(index2*100, (index*100) - 120, 0, True)
                blocks.append(temp)
            if y == 7: 
                flag.x = index2*100
                yWall2 = flag.x + 200
    for index, x in enumerate(underlayout):
        for index2, y in enumerate(x): 
            if y == 1: 
                temp = Block(index2*100, (index*100) - 120, 0, False)
                underblocks.append(temp)
            if y == 2: 
                temp = Coin(index2*100 + 40, (index*100) - 100, True)
                undercoins.append(temp)
            if y == 3: 
                temp = Block(index2*100, (index*100) - 120, 0, True)
                underblocks.append(temp)
            if y == 4: 
                temp = Pipe(index2*100, (index*100) - 120, True)
                underblocks.append(temp)

refresh()

while running:
    if startScreen: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("black")
        leveltxt = MyFont3.render("Level - 1-1", False, "white")
        textrect = leveltxt.get_rect(center=(550, 240))
        screen.blit(leveltxt, textrect)
        livestxt = MyFont3.render("Lives: " + str(lives), False, "white")
        textrect = livestxt.get_rect(center=(550, 460))
        screen.blit(livestxt, textrect)
        starttimer -= 1
        if starttimer < 0:
            startScreen = False
            gameplay = True
    if gameover: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("darkred")
        txt = MyFont3.render("GAME OVER", False, "red")
        textrect = txt.get_rect(center=(550,360))
        screen.blit(txt, textrect)
    if finish: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
        screen.fill("black")
        txt = MyFont3.render("Level Finished", False, "white")
        textrect = txt.get_rect(center=(550, 360))
        screen.blit(txt, textrect)
    if gameplay: 
        if underground:
            screen.fill("black")
        else:
            screen.fill("lightskyblue")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT: 
                    left = True
                if event.key == pygame.K_RIGHT: 
                    right = True
                if event.key == pygame.K_UP and grounded: 
                    grounded = False
                    jump = True
                if event.key == pygame.K_DOWN:
                    down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT: 
                    left = False
                if event.key == pygame.K_DOWN:
                    down = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_UP: 
                    jump = False
        if iFrames > 0: 
            iFrames -= 1
        if playerY > 800: 
            lives -= 1
            startScreen = True
            gameplay = False
            refresh() 
        if jump: 
            jumpIterations += 1
            velocity = 10
            if jumpIterations > 25: # holding jump makes you jump more (25 is barely enough to jump 4 blocks)
                jump = False
                jumpIterations = 0
        if animation == False: 
            if left and playerX >= 0: playerX -= moveSpeed
            if right and playerX <= 1000: playerX += moveSpeed
            if underground == False: 
                if playerX > 700 and yWall2 > 1100: # right camera move margin
                    moveRight = True
                else: 
                    moveRight = False
                if playerX < 300 and yWall < 0: # left camera move margin
                    moveLeft = True
                else: 
                    moveLeft = False
                if moveLeft: 
                    playerX += moveSpeed 
                    yWall += moveSpeed
                    yWall2 += moveSpeed
                    flag.x += moveSpeed
                if moveRight: 
                    playerX -= moveSpeed
                    yWall -= moveSpeed
                    yWall2 -= moveSpeed
                    flag.x -= moveSpeed
            playerY -= velocity 
            velocity -= acceleration
        else: 
            moveLeft = False
            moveRight = False
            if enterPipe: 
                playerY += 4
                playerX = pipeX
                aniIterations += 1
                if aniIterations > 50: 
                    enterPipe = False
                    if underground: 
                        underground = False
                        exitPipe = True
                        aniIterations = 0
                        playerY = overPipeY
                    else: 
                        animation = False
                        underground = True
                        overPipeX = pipeX
                        overPipeY = playerY 
                        playerY = 0
                        playerX = 150
            if exitPipe: 
                playerY -= 4
                playerX = overPipeX
                aniIterations += 1
                if aniIterations > 50: 
                    exitPipe = False
                    animation = False
            if dieAni: 
                if aniIterations < 20: 
                    aniIterations += 1
                    if aniIterations == 20:
                        velocity = 10
                else: 
                    playerY-=velocity
                    velocity-=acceleration
                    if playerY > 780: 
                        lives -= 1
                        startScreen = True
                        gameplay = False
                        refresh() 
            if flagAni: 
                if aniIterations > 20: 
                    if playerY >= 580-height: 
                        playerY = 580-height
                        aniIterations += 1
                        if aniIterations == 40: 
                            finish = True
                            gameplay = False
                    else:
                        playerY += 4
                else:
                    aniIterations += 1
        if velocity < -2: 
            grounded = False
        tempRect = pygame.Rect(playerX, playerY, 100, height)
        if iFrames <= 0: 
            pygame.draw.rect(screen, "red", tempRect)  
        else: 
            pygame.draw.rect(screen, pygame.Color(100, 10, 10), tempRect)
        if underground == False: 
            for enemy in enemies: 
                if enemy.deathTimer >= 0: 
                    enemy.y -= enemy.velocity
                    enemy.velocity -= acceleration
                    if enemy.y > 900: 
                        enemy.deathTimer = 0
                        enemy.dead = True
                    if dieAni == False:
                        if moveRight: 
                            enemy.x -= moveSpeed
                        if moveLeft: 
                            enemy.x += moveSpeed
                    for block in blocks: 
                        if block.x + 100 > enemy.x and block.x < enemy.x + 100: 
                            if block.y + 100 > enemy.y and block.y < enemy.y + 100:
                                if abs((block.y - enemy.y)) < abs((block.x - enemy.x)):
                                    if enemy.left: 
                                        enemy.left = False
                                        enemy.x += 3
                                    else: 
                                        enemy.left = True
                                        enemy.x -= 3
                                else: 
                                    if enemy.y+50 < block.y: 
                                        enemy.y = block.y-100 
                                        enemy.velocity = 0
                    if enemy.dead == False: 
                        if enemy.left: 
                            enemy.x -= 3 
                        if enemy.left == False: 
                            enemy.x += 3
                        tempRect = pygame.Rect(enemy.x, enemy.y, 100, 100)
                        pygame.draw.rect(screen, pygame.Color(43, 29,20), tempRect) 
                        if iFrames <= 0: 
                            if enemy.x + 100 > playerX and enemy.x < playerX + 100 and dieAni == False: 
                                if enemy.y + 100 > playerY and enemy.y < playerY + height: # enemy collision
                                    distance = 100
                                    if height == 100:
                                        distance = 0
                                    if abs((enemy.y) - (playerY + distance)) > abs((enemy.x + 100) - (playerX + 100)):
                                        velocity = 10
                                        grounded = False
                                        enemy.dead = True
                                        temp = Score(enemy.x, enemy.y, 100)
                                        scores.append(temp)
                                    else:
                                        if state == 2: 
                                            state = 1
                                            height = 100 
                                            playerY += 100
                                            iFrames = 60
                                        elif state == 1 and animation == False:
                                            dieAni = True
                                            moveLeft = False
                                            moveRight = False
                                            animation = True
                                            aniIterations = 0
                    else: 
                        if enemy.deathTimer >= 0: 
                            tempRect = pygame.Rect(enemy.x, enemy.y+90, 100, 10)
                            pygame.draw.rect(screen, pygame.Color(43, 29,20), tempRect) 
                            enemy.deathTimer-=1 
            for item in items: 
                if moveRight: 
                    item.x -= moveSpeed
                if moveLeft: 
                    item.x += moveSpeed
                if item.left: 
                    item.x -= 3
                else: 
                    item.x += 3
                item.y -= item.velocity 
                item.velocity -= acceleration
                for block in blocks: 
                        if block.x + 100 > item.x and block.x < item.x + 100: 
                            if block.y + 100 > item.y and block.y < item.y + 100:
                                if abs((block.y - item.y)) < abs((block.x - item.x)):
                                    if item.left: 
                                        item.left = False
                                    else: 
                                        item.left = True
                                else: 
                                    if item.y+50 < block.y: 
                                        item.y = block.y-100 
                                        item.velocity = 0
                temp = pygame.Rect(item.x, item.y, 100, 50)
                temp2 = pygame.Rect(item.x, item.y+50, 100 ,50)
                pygame.draw.rect(screen, "red", temp)
                pygame.draw.rect(screen, "white", temp2)
                if item.x + 100 > playerX and item.x < playerX + 100: 
                    if item.y + 100 > playerY and item.y < playerY + height:
                        if state == 1: 
                            state = 2
                            height = 200 
                            items.remove(item)
                            playerY -= 100
                        elif state == 2:
                            temp = Score(item.x, item.y, 100)
                            scores.append(temp)
                            items.remove(item)
            for block in blocks: 
                if moveRight: 
                    block.x -= moveSpeed 
                if moveLeft: 
                    block.x += moveSpeed
                tempRect = pygame.Rect(block.x, block.y, 100, 100)
                if type(block) == Block:
                    if block.hit == True: 
                        tempRect = pygame.Rect(block.x, block.y-10, 100, 100)
                        block.timer -= 1
                        if block.timer < 0: 
                            block.hit = False
                    if block.pipe == True: 
                        pygame.draw.rect(screen, "green", tempRect) 
                    elif block.coins > 0: 
                        pygame.draw.rect(screen, pygame.Color(200, 64, 51), tempRect) 
                    else: 
                        pygame.draw.rect(screen, pygame.Color(92, 64, 51), tempRect) 
                elif type(block) == ItemBlock: 
                    if block.hit == False:
                        pygame.draw.rect(screen, "yellow", tempRect) 
                    else: 
                        tempRect = pygame.Rect(block.x, block.y-20, 100, 100)
                        pygame.draw.rect(screen, pygame.Color(92, 64, 51), tempRect)
                    if block.hit: 
                        block.timer -= 1
                        if block.timer < 0: 
                            blocks.remove(block)
                            temp = Block(block.x, block.y, 0, False)
                            blocks.append(temp)
                elif type(block) == Pipe:
                    pygame.draw.rect(screen, "green", tempRect)
                    temp = pygame.Rect(block.x, block.y, 100, 50)
                    pygame.draw.rect(screen, "darkgreen", temp, 3)
                if animation == False and block.x + 100 > playerX and block.x < playerX + 100: # block collision (a couple of bugs with falling and hugging a block but overall it works)
                    if block.y + 100 > playerY and block.y < playerY + height:
                        distance = 100
                        if height == 100:
                            distance = 0
                        if abs((block.y) - (playerY + distance)) < abs((block.x + 100) - (playerX + 100)):
                            if left: 
                                playerX += moveSpeed
                            if right: 
                                playerX -= moveSpeed
                        else: 
                            if playerY+(distance/2) < block.y: 
                                playerY = block.y-height 
                                velocity = 0
                                grounded = True
                                jumpIterations = 0
                                if type(block) == Pipe and down == True: 
                                    enterPipe = True
                                    pipeX = block.x
                                    animation = True
                                    aniIterations = 0
                                    down = False
                            elif playerY > block.y - 80 and abs((playerX + 100) - (block.x + 100)) < 95 and velocity > 0: 
                                playerY = block.y+100
                                velocity = 0
                                jumpIterations = 26
                                if type(block) == Block: 
                                    if block.coins>0 and block.hit == False: 
                                        block.hit = True
                                        block.timer = 15
                                        block.coins-=1
                                        temp = Coin(block.x + 40, block.y - 60, True)
                                        coins.append(temp)
                                        coinCount += 1
                                if type(block) == ItemBlock: 
                                    if block.item == "Mushroom" and block.hit == False: 
                                        temp = Mushroom(block.x, block.y-100)
                                        items.append(temp)
                                        block.hit = True
        else: # underground code block
            for block in underblocks: 
                if moveRight: 
                    block.x -= moveSpeed 
                if moveLeft: 
                    block.x += moveSpeed
                tempRect = pygame.Rect(block.x, block.y, 100, 100)
                if type(block) == Block:
                    if block.hit == True: 
                        tempRect = pygame.Rect(block.x, block.y-10, 100, 100)
                        block.timer -= 1
                        if block.timer < 0: 
                            block.hit = False
                    if block.pipe == True: 
                        pygame.draw.rect(screen, "green", tempRect) 
                    else: 
                        pygame.draw.rect(screen, "darkgray", tempRect) 
                if type(block) == Pipe:
                    temp = pygame.Rect(block.x, block.y, 100, 50)
                    pygame.draw.rect(screen, "green", tempRect)
                    pygame.draw.rect(screen, "darkgreen", temp, 3)
                if animation == False and block.x + 100 > playerX and block.x < playerX + 100: # block collision (a couple of bugs with falling and hugging a block but overall it works)
                    if block.y + 100 > playerY and block.y < playerY + height:
                        distance = 100
                        if height == 100:
                            distance = 0
                        if abs((block.y) - (playerY + distance)) < abs((block.x + 100) - (playerX + 100)):
                            if left: 
                                playerX += moveSpeed
                            if right: 
                                playerX -= moveSpeed
                        else: 
                            if playerY+(distance/2) < block.y: 
                                playerY = block.y-height 
                                velocity = 0
                                grounded = True
                                jumpIterations = 0
                                if type(block) == Pipe and down == True: 
                                    enterPipe = True
                                    pipeX = block.x
                                    animation = True
                                    aniIterations = 0
                                    down = False
                            elif playerY > block.y - 80 and abs((playerX + 100) - (block.x + 100)) < 95 and velocity > 0: 
                                playerY = block.y+100
                                velocity = 0
                                jumpIterations = 26
                for coin in undercoins: 
                    temp = pygame.Rect(coin.x, coin.y, 20, 40)
                    pygame.draw.rect(screen, "yellow", temp)
                    if coin.x + 20 > playerX and coin.x < playerX + 100: # block collision (a couple of bugs with falling and hugging a block but overall it works)
                        if coin.y + 40 > playerY and coin.y < playerY + height:
                            undercoins.remove(coin)
                            coinCount += 1
        for coin in coins: 
            if moveLeft: 
                coin.x += moveSpeed
            if moveRight:
                coin.x -= moveSpeed
            temp = pygame.Rect(coin.x, coin.y, 20, 40)
            pygame.draw.rect(screen, "yellow", temp)
            if coin.animation: 
                coin.timer -= 1 
                coin.y -= 2
                if coin.timer < 0: 
                    coins.remove(coin)
        for score in scores:
            if moveLeft:
                score.x += moveSpeed
            if moveRight:
                score.x -= moveSpeed
            temp = myFont.render(str(score.amount), False, "white")
            screen.blit(temp, (score.x, score.y))
            if score.timer < 0: 
                scores.remove(score)
            else: 
                score.timer -= 1
        flagRect = pygame.Rect(flag.x + 40, flag.y, 20, 500)
        pygame.draw.rect(screen, "green", flagRect)
        flagRect = pygame.Rect(flag.x-160, flag.y + 20, 200, 100)
        pygame.draw.rect(screen, "red", flagRect)
        if playerX+100 > flag.x and flagAni == False: 
            flagAni = True
            animation = True
            playerX = flag.x - 60
            aniIterations = 0
        temp = MyFont2.render("Coins: " + str(coinCount), False, "white")
        screen.blit(temp, (10, 10))

    pygame.display.flip()
    dt = clock.tick(60)

pygame.quit()