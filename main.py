# _*_ coding: utf-8 _*_
import pygame, sys, time, random, asyncio

side = 30  # 单块边长
windowX = 20  # 窗口宽30格子
windowY = 30  # 窗口高20格子
blockX = int(windowX / 2)  # x第3格(3*30) 方块X位置
blockY = -2  # y第6格(6*30) 方块Y位置
currentBlock = [[0, 0], [0, -1], [0, 1], [0, 2]]  # 当前方块，默认I
x = 0  # 方块x距离
y = 0  # 方块y距离
Map = []  # 二维数组地图
keyDown = {'left': False, 'right': False, 'down': False, 'up': False}  # 记录键是否按下
delay = 5  # 下落延迟(等于按 ←→↓速度*delay)

# 窗口
screen = pygame.display.set_mode((side * windowX, side * windowY))

# 标题
pygame.display.set_caption('hello world')

allBlock = [[[0, 0], [0, -1], [0, 1], [0, 2]],  # 物块形状为I
            [[0, 0], [0, 1], [1, 1], [1, 0]],  # 物块形状为O
            [[0, 0], [0, -1], [-1, 0], [-1, 1]],  # 物块形状为Z
            [[0, 0], [0, 1], [-1, -1], [-1, 0]],  # 物块形状为S
            [[0, 0], [0, 1], [1, 0], [0, -1]],  # 物块形状为T
            [[0, 0], [1, 0], [-1, 0], [1, -1]],  # 物块形状为L
            [[0, 0], [1, 0], [-1, 0], [1, 1]]]  # 物块形状为J


# 初始化地图
def initMap():
    global Map
    Map = [[] for y in range(windowY)]
    for y in range(windowY):
        Map[y] = [False for x in range(windowX)]


# 生成地图
def createMap():
    for y in range(len(Map)):
        for x in range(len(Map[y])):
            if Map[y][x] == True:
                pygame.draw.rect(screen, (0, 0, 255), (x * side, y * side, side - 2, side - 2))


# 旋转
def rotate():
    global currentBlock
    tempBlock = [] * len(currentBlock)
    for i in range(len(currentBlock)):
        tempBlock.append([currentBlock[i][1] * -1, currentBlock[i][0]])
    if judgeMove(blockX, blockY, tempBlock):
        currentBlock = tempBlock


# 判断移动 判断到底 判断碰到方块
def judgeMove(blockX, blockY, currentBlock):
    global Map
    for block in currentBlock:
        if block[0] + blockX < 0 or block[0] + blockX >= windowX or block[1] + blockY >= windowY or \
                Map[block[1] + blockY][block[0] + blockX] == True:
            return False
    return True


# 改变按键
def keyChange(keyType, ifDown):
    if keyType == pygame.K_UP:  # ↑
        if ifDown == True:
            rotate()
    elif keyType == pygame.K_DOWN:  # ↓
        keyDown['down'] = ifDown
    elif keyType == pygame.K_LEFT:  # ←
        keyDown['left'] = ifDown
    elif keyType == pygame.K_RIGHT:  # →
        keyDown['right'] = ifDown


# 生成已经放置的方块
def getTo(current_block, block_x, block_y):
    global Map
    for block in current_block:
        Map[block[1] + block_y][block[0] + block_x] = True

    # 判断消除
    allY = []
    for block in current_block:
        allY.append(block[1] + block_y)
    allY.sort()
    for y in allY:
        if False not in Map[y]:
            Map[0] = [False for i in range(len(Map[0]))]
            for i in range(y, 1, -1):
                Map[i] = Map[i - 1]

    # 判断死亡
    if True in Map[0]:
        print('死亡，结束游戏')
        sys.exit()

    initBlock()


# 初始化方块
def initBlock():
    global currentBlock, blockX, blockY
    currentBlock = allBlock[random.randint(0, len(allBlock) - 1)]
    # currentBlock = allBlock[0]
    blockX = random.randint(1, windowX - 2)
    blockY = 0


times = 0  # 下落时间存放
initMap()  # 初始化地图
pygame.init()  # 初始化游戏
# 开始游戏
while True:
    screen.fill((255, 255, 255))  # 窗口背景为白色
    createMap()  # 生成地图
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # 按下键
            if event.key == pygame.K_SPACE:  # 按空格
                while judgeMove(blockX, blockY + 1, currentBlock):
                    blockY += 1
                getTo(currentBlock, blockX, blockY)
            keyChange(event.key, True)
        elif event.type == pygame.KEYUP:  # 松开键
            keyChange(event.key, False)

    if keyDown['left'] and judgeMove(blockX - 1, blockY, currentBlock):
        time.sleep(0.05)
        blockX -= 1
    if keyDown['right'] and judgeMove(blockX + 1, blockY, currentBlock):
        time.sleep(0.05)
        blockX += 1
    if keyDown['down'] and judgeMove(blockX, blockY + 1, currentBlock):
        blockY += 1
    elif keyDown['down']:
        getTo(currentBlock, blockX, blockY)

    times += 1
    if times >= delay:
        times = 0
        if judgeMove(blockX, blockY + 1, currentBlock):
            blockY += 1
        else:
            getTo(currentBlock, blockX, blockY)

    for block in currentBlock:  # 生成方块
        x = (blockX + block[0]) * side
        y = (blockY + block[1]) * side
        pygame.draw.rect(screen, (0, 255, 0), (x, y, side - 2, side - 2))
    time.sleep(0.05)
    pygame.display.update()
