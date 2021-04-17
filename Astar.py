import heapq
class ShortestPathAstarSolver(object):

    def __init__(self, display_width, display_height, block_size):
        # BaseGameModel.__init__(self, "Shortest Path BFS", "shortest_path_bfs", "spb")
        # Game parameters
        self.display_width = display_width
        self.display_height = display_height
        self.block_size = block_size

        # Action space
        self.actions = {
            0:'left',
            1:'right',
            2:'up',
            3:'down'
        }
    def h(self,a, b):
        """Return distance between 2 points"""
        return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

    
    def move(self, snake_list, fruit_node):
        # BaseGameModel.move(self, environment)
        # shortest_path_move_from_transposition_table = self._path_move_from_transposition_table(self.starting_node, self.fruit_node)
        # if shortest_path_move_from_transposition_table:
        #     return shortest_path_move_from_transposition_table
        self.snake_list = snake_list
        self.fruit_node = fruit_node
        self.starting_node = snake_list[-1]
        # print(self.starting_node)

        shortest_path = self.shortest_path(self.starting_node, self.fruit_node, self.snake_list[1::])
        if shortest_path:
            # self.transposition_table[self.fruit_node] = shortest_path
            # first_point = shortest_path[-2]
            return shortest_path
        return None

    def possible_action(self, starting_node, snake_list):
        # distance_x_right = self.display_width - (starting_node[0] + self.block_size)
        # distance_x_left = self.display_width - distance_x_right
        # distance_y_up = self.display_height - (starting_node[1] + self.block_size)
        # distance_y_down = self.display_height - distance_y_up
        pos_actions = [[0],[0],[0],[0]]
        
        
        if (starting_node[0]+self.block_size < self.display_width and [starting_node[0]+self.block_size, starting_node[1]] not in snake_list):
            pos_actions[3] = [[starting_node[0]+self.block_size, starting_node[1]],['right']]
        else:
            pos_actions[3] = [0]
        if(starting_node[0]-self.block_size > 0 and [starting_node[0]-self.block_size, starting_node[1]] not in snake_list): 
            pos_actions[2] = [[starting_node[0]-self.block_size, starting_node[1]],['left']]
        else:
            pos_actions[2] = [0]
        if (starting_node[1]+self.block_size < self.display_height and [starting_node[0], starting_node[1]+self.block_size] not in snake_list):
            pos_actions[1] = [[starting_node[0], starting_node[1]+self.block_size],['down']]
        else:
            pos_actions[1] = [0]
        if (starting_node[1]-self.block_size > 0 and [starting_node[0], starting_node[1]-self.block_size] not in snake_list):
            pos_actions[0] = [[starting_node[0], starting_node[1]-self.block_size],['up']]
        else:
            pos_actions[0] = [0]
        # for body in self.snake_list:
        #     if body['x'] == x and body['y'] == y:
        #         return True
        #     return False
        #print('ssdasd',pos_actions)
        return pos_actions


    def shortest_path(self, start, end, snake_list):
        queue = []
        heapq.heappush(queue,[start,[],self.h(start,end)])
        # print(snake_list)
        visited_nodes = [list(x) for x in snake_list]
        
        #visited_nodes = snake_list
        # print(visited_nodes)
        shortest_path = []
        while queue:
            current_node = heapq.heappop(queue)
            # print(current_node)
            path = current_node[1]
            cost = current_node[2]
            #print(path)
            if (current_node[0] == end):
                # print("sdasdsakdsalkdlsaldkasl;d;lasl;das;ld",path)
                return path
            if current_node[0] not in visited_nodes:
                visited_nodes.append([current_node[0][0],current_node[0][1]])
                # print(visited_nodes)
                for action in self.possible_action(current_node[0], visited_nodes):
                # print(action)
                    if action[0] == 0:
                        continue
                    new_path = path + [action[1]]
                    new_cost = cost+self.h(action[0],end)
                    heapq.heappush(queue,[action[0],new_path,new_cost])
        
                