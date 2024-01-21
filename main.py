import pygame as pg
from random import randrange

WINDOW = 800
TILE_SIZE = 20
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)

def get_random_position(snake, segments):
    while True:
        position = [randrange(*RANGE), randrange(*RANGE)]
        
        if not any(segment.collidepoint(position) for segment in [snake] + segments):
            return position

snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = get_random_position(snake, [])

length = 1
score = 0

high_score_filename = "snake_high_score.txt"

segments = [snake.copy()]

snake_dir = (0,0)

time, base_time_step = 0, 90

food = snake.copy()
food.center = get_random_position(snake, segments)

screen = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()

dirs = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}

pg.font.init()

try:
    f = open(high_score_filename)
except:
    f = open(high_score_filename, "w")
    f.write("0")
finally:
    f.close()
with open (high_score_filename) as f:

    data = f.read()

    if not data:
        high_score = 0
    else:
        high_score = int(data)



font = pg.font.Font(None, 36)

while True:
    for event in pg.event.get():
        
        if event.type == pg.QUIT:
            exit()
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and dirs[pg.K_UP]:
                snake_dir = (0, -TILE_SIZE)
                dirs = {pg.K_UP: 1, pg.K_DOWN: 0, pg.K_LEFT: 1, pg.K_RIGHT: 1}
            
            if event.key == pg.K_DOWN and dirs[pg.K_DOWN]:
                snake_dir = (0, TILE_SIZE)
                dirs = {pg.K_UP: 0, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}
            
            if event.key == pg.K_LEFT and dirs[pg.K_LEFT]:
                snake_dir = (-TILE_SIZE, 0)  
                dirs = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 0}  
            
            if event.key == pg.K_RIGHT and dirs[pg.K_RIGHT]:
                snake_dir = (TILE_SIZE, 0)
                dirs = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 0, pg.K_RIGHT: 1}
    
    screen.fill("black")
    
    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1


    if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
        
        snake.center, food.center = get_random_position(snake, segments), get_random_position(snake, segments)
        
        length, snake_dir = 1, (0,0)
        
        segments = [snake.copy()]
        
        score = 0

    if snake.center == food.center:
        
        food.center = get_random_position(snake, segments)
        
        length += 1
        score += 1
        
        if score > high_score:
            high_score = score
            
            with open(high_score_filename, "w") as f:
                f.write(str(high_score))

    pg.draw.rect(screen, 'red', food)

    [pg.draw.rect(screen, 'green', segment) for segment in segments]
   
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (WINDOW - 150, 20))

    high_score_text = font.render(f"High Score: {high_score}", True, (255,255,255))
    screen.blit(high_score_text, (50, 20))

    time_now = pg.time.get_ticks()
    
    if time_now - time > base_time_step:
        
        time = time_now
        
        snake.move_ip(snake_dir)
        
        segments.append(snake.copy())
        
        segments = segments[-length:]

    pg.display.flip()

    clock.tick(60)        