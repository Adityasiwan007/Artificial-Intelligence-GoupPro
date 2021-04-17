import pygame
import random
pygame.init()
import Qlearning
import itertools
import json
import BreadthFirstSearch
import DepthFirstSearch
import Astar
import sys


BLOCK_SIZE = 10 
DIS_WIDTH = 400
DIS_HEIGHT = 400
ticks = 100

def Q_GameLoop(learner):
    global dis
    
    dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()

    # Starting position of snake
    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2
    x1_change = 0
    y1_change = 0
    snake_list = [(x1,y1),[x1-BLOCK_SIZE , y1],[x1-(2*BLOCK_SIZE) , y1]]
    length_of_snake = 1

    # Create first food
    foodx = round(random.randrange(0, DIS_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
    foody = round(random.randrange(0, DIS_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

    dead = False
    reason = None
    first_time = True
    while not dead:
        # Get action from agent
        action = learner.act(snake_list, (foodx,foody))
        # action = None
        events = pygame.event.get()
        if first_time:
            x1_change = -BLOCK_SIZE
            first_time = False
        # for event in events:
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_LEFT or action =='left':
        #             x1_change = -BLOCK_SIZE
        #             y1_change = 0
        #         elif event.key == pygame.K_RIGHT or action == "right":
        #             x1_change = BLOCK_SIZE
        #             y1_change = 0
        #         elif event.key == pygame.K_UP or action == "up":
        #             y1_change = -BLOCK_SIZE
        #             x1_change = 0
        #         elif event.key == pygame.K_DOWN or action == "down":
        #             y1_change = BLOCK_SIZE
        #             x1_change = 0
        if action =='left':
            x1_change = -BLOCK_SIZE
            y1_change = 0
        elif action == "right":
            x1_change = BLOCK_SIZE
            y1_change = 0
        elif action == "up":
            y1_change = -BLOCK_SIZE
            x1_change = 0
        elif action == "down":
            y1_change = BLOCK_SIZE
            x1_change = 0
        # Move snake
        x1 += x1_change
        y1 += y1_change
        snake_head = (x1,y1)
        snake_list.append(snake_head)

        # Check if snake is off screen
        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
            reason = 'Screen'
            dead = True

        # Check if snake hit tail
        if snake_head in snake_list[:-1]:
            reason = 'Tail'
            dead = True
        # for square in snake_list[:-1]:
        #     print(snake_list[:-1],snake_list)
        #     if pygame.Rect(square[0],square[1],10,10).colliderect(pygame.Rect(snake_head[0],snake_head[1],10,10)):
        #         reason = 'Tail'
        #         dead = True

        # Check if snake ate food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, DIS_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
            foody = round(random.randrange(0, DIS_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
            length_of_snake += 1

        # Delete the last cell since we just added a head for moving, unless we ate a food
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Draw food, snake and update score
        dis.fill((0,0,255))
        DrawFood(foodx, foody)
        DrawSnake(snake_list)
        DrawScore(length_of_snake - 1)
        pygame.display.update()

        # Update Q Table
        learner.UpdateQValues(reason)
        
        # Next Frame
        clock.tick(ticks)
    if dead:
        print(reason)

    return length_of_snake - 1, reason

def DrawFood(foodx, foody):
    pygame.draw.rect(dis, (0,255,0), [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])   

def DrawScore(score):
    font = pygame.font.SysFont("comicsansms", 35)
    value = font.render(f"Score: {score}", True, (255,255,0))
    dis.blit(value, [0, 0])

def DrawSnake(snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, (0,0,0), [x[0], x[1], BLOCK_SIZE, BLOCK_SIZE])

# GameLoop()
def run_q_learning():
    game_count = 1

    learner = Qlearning.Learner(DIS_WIDTH, DIS_HEIGHT, BLOCK_SIZE)

    while True:
        learner.Reset()
        if game_count > 100:
            learner.epsilon = 0
        else:
            learner.epsilon = .1
        score, reason = Q_GameLoop(learner)
        print(f"Games: {game_count}; Score: {score}; Reason: {reason}") # Output results of each game to console to monitor as agent is training
        game_count += 1
        if game_count % 100 == 0: # Save qvalues every qvalue_dump_n games
            print("Save Qvals")
            learner.SaveQvalues()

def general_Gameloop(obj):
    global dis
    
    dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()

    # Starting position of snake
    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2
    x1_change = 0
    y1_change = 0
    snake_list = [(x1,y1)]
    length_of_snake = 1

    # Create first food
    foodx = round(random.randrange(0, DIS_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
    foody = round(random.randrange(0, DIS_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

    dead = False
    reason = None
    first_time = True
    
        # Get action from agent
        # action = learner.act(snake_list, (foodx,foody))
    
    # print(actions)
    prev_action = None
    while not dead:
        
        actions = obj.move(snake_list, [foodx,foody])
        while (actions == None):
            foodx = round(random.choice([i for i in range(0,DIS_WIDTH-BLOCK_SIZE) if i not in snake_x]) / 10.0) * 10.0
            foody = round(random.choice([i for i in range(0,DIS_HEIGHT-BLOCK_SIZE) if i not in snake_y]) / 10.0) * 10.0
            actions = obj.move(snake_list, [foodx,foody])
        for action in actions:
            event = pygame.event.get()
            dis.fill((0,0,255))
            # action = None
            # events = pygame.event.get()
            # if first_time:
            #     x1_change = -BLOCK_SIZE
                #first_time = False
            # for event in events:
            #     if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_LEFT or action =='left':
            #             x1_change = -BLOCK_SIZE
            #             y1_change = 0
            #         elif event.key == pygame.K_RIGHT or action == "right":
            #             x1_change = BLOCK_SIZE
            #             y1_change = 0
            #         elif event.key == pygame.K_UP or action == "up":
            #             y1_change = -BLOCK_SIZE
            #             x1_change = 0
            #         elif event.key == pygame.K_DOWN or action == "down":
            #             y1_change = BLOCK_SIZE
            #             x1_change = 0
            #print(action)
            if action[0] =='left':
                x1_change = -BLOCK_SIZE
                y1_change = 0
                prev_action = 'left'
            elif action[0] == "right":
                x1_change = BLOCK_SIZE
                y1_change = 0
                prev_action = 'right'
            elif action[0] == "up":
                y1_change = -BLOCK_SIZE
                x1_change = 0
                prev_action = 'up'
            elif action[0] == "down":
                y1_change = BLOCK_SIZE
                x1_change = 0
                prev_action = 'down'
            # Move snake
            x1 += x1_change
            y1 += y1_change
            snake_head = (x1,y1)
            snake_list.append(snake_head)
            
            DrawFood(foodx, foody)
            DrawSnake(snake_list)
            DrawScore(length_of_snake - 1)
            pygame.display.update()
            # Check if snake is off screen
            if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
                reason = 'Screen'
                dead = True

            # Check if snake hit tail
            if snake_head in snake_list[:-1]:
                reason = 'Tail'
                dead = True
            # for square in snake_list[:-1]:
            #     print(snake_list[:-1],snake_list)
            #     if pygame.Rect(square[0],square[1],10,10).colliderect(pygame.Rect(snake_head[0],snake_head[1],10,10)):
            #         reason = 'Tail'
            #         dead = True

            # Check if snake ate food
            if x1 == foodx and y1 == foody:
                snake_x = []
                snake_y = []
                for snake in snake_list:
                    snake_x.append(snake[0]) 
                    snake_y.append(snake[1]) 
                foodx = round(random.choice([i for i in range(0,DIS_WIDTH-BLOCK_SIZE) if i not in snake_x]) / 10.0) * 10.0
                foody = round(random.choice([i for i in range(0,DIS_HEIGHT-BLOCK_SIZE) if i not in snake_y]) / 10.0) * 10.0
                # if ((new_foodx,new_foody) in snake_list):
                #     print(True)
                #     while((new_foodx,new_foody) in snake_list):
                #         new_foodx = round(random.randrange(0, DIS_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
                #         new_foody = round(random.randrange(0, DIS_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
                # foodx=new_foodx
                # foody=new_foody
                length_of_snake += 1

            # Delete the last cell since we just added a head for moving, unless we ate a food
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            # Next Frame
            clock.tick(50)
    if dead:
        print(reason)



if __name__ == '__main__':
    # run_bfs()
    bfs = BreadthFirstSearch.ShortestPathBFSSolver(DIS_WIDTH, DIS_HEIGHT, BLOCK_SIZE)
    dfs = DepthFirstSearch.ShortestPathDFSSolver(DIS_WIDTH, DIS_HEIGHT, BLOCK_SIZE)
    a_star = Astar.ShortestPathAstarSolver(DIS_WIDTH, DIS_HEIGHT, BLOCK_SIZE)
    arg = sys.argv[1]
    if arg == '-q':
        run_q_learning()
    if arg == '-dfs':
        general_Gameloop(dfs)
    if arg == '-bfs':
        general_Gameloop(bfs)
    if arg == '-astar':
        general_Gameloop(a_star)