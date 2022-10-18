#  conda activate myenv
# python3 -m connect4.ConnectFour random ai connect4/initial_states/case1.txt --time 10


# import random
from cmath import inf
from os import stat
import numpy as np
import time
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer
# import logging


# logging.basicConfig(filename='exec_data.log', level=logging.DEBUG, format='%(lineno)d:%(message)s')


class AIPlayer:
    def __init__(self, player_number: int, time: int):
        """
        :param player_number: Current player number
        :param time: Time per move (seconds)
        """
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.time = time
    
    def activation_fn(self, x):
        return 1/(1 + np.exp(-x))

    def update_state(self, state_1: Tuple[np.array, Dict[int, Integer]], action: Tuple[int, bool], player_number: int):
        # logging.debug(f"action: {action} player: {player_number} popout: {state[1][player_number].get_int()}")

        if(state_1[1][player_number].get_int() == 0 and action[1] == True): return state_1

        obj1 = Integer(state_1[1][1].get_int())
        obj2 = Integer(state_1[1][2].get_int())
        state = (state_1[0].copy(), {1:obj1, 2:obj2})
        # (np.copy(state[0]), {1:state[1][1].get_int().copy(), 2:state[1][2].get_int().copy()})

        array = state[0]
        column = action[0]

        first_occupied_row = 0
        while(True):
            if first_occupied_row == len(array): break
            elif(array[first_occupied_row][column] == 0): first_occupied_row += 1
            else: break
        first_occupied_row -= 1

        if(action[1] == True):
            for r in range(len(array)-1, 0, -1):
                array[r, column] = array[r - 1, column]
            array[0, column] = 0
            # logging.debug(f'-------Player num = {player_number}---------{state[1][player_number].get_int()}')
            state[1][player_number].decrement()
        elif(first_occupied_row < 0): return array
        else:
            array[first_occupied_row][column] = player_number

        return state

    def update_array(self, array :np.array, action: Tuple[int, bool]):
        # original_array = array
        column = action[0]

        first_occupied_row = 0
        while(True):
            if first_occupied_row == len(array): break
            elif(array[first_occupied_row][column] == 0): first_occupied_row += 1
            else: break
        first_occupied_row -= 1

        if(action[1] == True):
            for r in range(len(array)-1, 0, -1):
                array[r, column] = array[r - 1, column]
            array[0, column] = 0
        elif(first_occupied_row < 0): return array
        else:
            array[first_occupied_row][column] = self.player_number

        return array

    # returns the best utility it can get
    def minimax(self, depth, state: Tuple[np.array, Dict[int, Integer]], alpha, beta, player_num, start_time) -> int:
        if depth == 0 or (time.time() - start_time > self.time - 0.2):
            # return get_pts(player_num, state[0])
            return get_pts(self.player_number, state[0]) - get_pts(1 + self.player_number%2, state[0])
        
        valid_actions = get_valid_actions(player_num, state)
        opp_player_num = 1 + player_num%2

        if len(valid_actions) == 0:
            # return get_pts(player_num, state[0])
            return get_pts(self.player_number, state[0]) - get_pts(self.player_number%2 + 1, state[0])

        # maximizing player
        if player_num == self.player_number:
            max_val = -inf
            for action in valid_actions:
                new_state = self.update_state(state, action, player_num)
                # new_state = self.update_state((state[0].copy(), state[1].copy()), action, player_num)
                val = self.minimax(depth-1, (new_state[0].copy(), new_state[1].copy()), alpha, beta, opp_player_num, start_time)
                max_val = max(max_val, val)
                alpha = max(alpha, max_val)

                # Alpha-Beta Pruning
                if beta <= alpha:
                    break

            return max_val
            
        # minimizing player
        else:
            min_val = inf
            for action in valid_actions:
                new_state = self.update_state(state, action, player_num)
                # new_state = self.update_state((state[0].copy(), state[1].copy()), action, player_num)
                val = self.minimax(depth-1, (new_state[0].copy(), new_state[1].copy()), alpha, beta, opp_player_num, start_time)
                min_val = min(min_val, val)
                beta = min(beta, min_val)

                if beta <= alpha:
                    break

            return min_val


    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        # Do the rest of your implementation here
        if(np.sum(state[0])<3):
            return ((len(state[0][0])//2, False))

        start_time = time.time()

        max_depth = 3
        if(np.sum(state[0]) < (len(state[0])*(len(state[0][0])*1.5*0.65))):
            max_depth = 3
        elif(np.sum(state[0]) < (len(state[0])*(len(state[0][0])*1.5*0.8))):
            max_depth = 5
        else:
            max_depth = 7


        valid_actions = get_valid_actions(self.player_number, state)

        max_val = -inf
        best_move = valid_actions[0]
        opp_player_num = 1 + self.player_number%2
        n = len(state[0][0])

        weight = 1.2
        if(np.sum(state[0]) < (len(state[0])*(len(state[0][0])*1.5*0.5))):
            weight = 1.2
        else:
            weight = 1

        for action in valid_actions:
            new_state = self.update_state(state, action, self.player_number)
            # new_state = self.update_state((state[0].copy(), state[1].copy()), action, player_num)
            val = self.minimax(max_depth, (new_state[0].copy(), new_state[1].copy()), -inf, inf, opp_player_num, start_time)

            if(np.sum(state[0]) < (len(state[0])*(len(state[0][0])*1.5*0.5))):
                val = self.activation_fn(val)

            if(action[0] >= n//4 and action[0] < 3*n//4):
                val = weight * val
                # if(val < 0):
                #     val = val/weight
                # else:
                #     val = weight*val

            print(f"action {action} val {val} ")

            if(val > max_val):
                max_val = val
                best_move = action

        # print(weight)
        # print(np.sum(state[0])/(len(state[0])*(len(state[0][0])*1.5)))
        print(f"Time taken2 {time.time()-start_time} ")        

        return best_move

    def get_expectimax_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        # Do the rest of your implementation here

        if(np.sum(state[0])<3):
            return ((len(state[0][0])//2, False))

        start_time = time.time()

        max_depth = 3
        valid_actions = get_valid_actions(self.player_number, state)

        max_val = -inf
        best_move = valid_actions[0]
        opp_player_num = 1 + self.player_number%2

        for action in valid_actions:
            new_state = self.update_state(state, action, self.player_number)
            # new_state = self.update_state((state[0].copy(), state[1].copy()), action, player_num)
            val = self.minimax(max_depth, (new_state[0].copy(), new_state[1].copy()), -inf, inf, opp_player_num, start_time)
            if(val > max_val):
                max_val = val
                best_move = action

        print(f"Time taken {time.time()-start_time} ")        

        return best_move






        start_time = time.time()
        valid_moves = get_valid_actions(self.player_number, state)
        # logging.debug(f'Valid moves at start :{valid_moves}')
        best_move = valid_moves[0]
        frontiers = []
        opp_player_num = 1 + (self.player_number)%2
        depth = 1
        max_diff = 0

        # pop_outs = state[1][self.player_number].get_int()        
        # if(pop_outs < 4):
        #     max_depth = 1
        # else:
        #     max_depth = 2

        max_depth = 1
        if(np.sum(state[0]) < (len(state[0])*(len(state[0][0])*1.5*0.6))):
            max_depth = 1
        elif(np.sum(state[0]) < (len(state[0])*(len(state[0][0])*1.5*0.8))):
            max_depth = 2
        else:
            max_depth = 3

        # if ((get_pts(self.player_number, state[0]) < (get_pts(opp_player_num, state[0]) + 100))):
        #     max_depth = 1

        if(np.sum(state[0])<3):
            return ((len(state[0][0])//2, False))

        for i in range(len(valid_moves)):
            # logging.debug(f'Valid move -- {valid_moves[i]}')
            new_state = self.update_state(state, valid_moves[i], self.player_number)
            frontiers.append((self.player_number, i, depth, new_state))
        
        for i in range(max_depth):
            if(time.time() - start_time > self.time - 0.5):
                # logging.debug(f'Best move = {best_move}')
                return best_move
            
            new_frontiers = []

            while(len(frontiers)>0):
                if(time.time() - start_time > self.time - 0.5):
                    # logging.debug(f'Best move = {best_move}')
                    return best_move
                new_move = frontiers.pop(0)
                new_valid_moves = get_valid_actions(1 + (new_move[0])%2, new_move[3])
                for j in range(len(new_valid_moves)):
                    if(time.time() - start_time > self.time - 0.5):
                        # logging.debug(f'Best move = {best_move}')
                        return best_move
                    # logging.debug(f'Player = {1+(new_move[0])%2} -- {new_valid_moves[j]}')
                    new_state = self.update_state(new_move[3], new_valid_moves[j], new_move[0])
                    new_frontiers.append((1 + (new_move[0])%2, new_move[1], depth + 1, new_state))
            if(len(new_frontiers) == 0): continue


            frontiers = new_frontiers
            new_frontiers = []

            while(len(frontiers)>0):
                if(time.time() - start_time > self.time - 0.5):
                    # logging.debug(f'Best move = {best_move}')
                    return best_move
                new_move = frontiers.pop(0)
                new_valid_moves = get_valid_actions(1 + (new_move[0])%2, new_move[3])
                for j in range(len(new_valid_moves)):
                    if(time.time() - start_time > self.time - 0.5):
                        # logging.debug(f'Best move = {best_move}')
                        return best_move
                    # logging.debug(f'Player = {1+(new_move[0])%2} -- {new_valid_moves[j]}')
                    new_state = self.update_state(new_move[3], new_valid_moves[j], new_move[0])
                    new_frontiers.append((1 + (new_move[0])%2, new_move[1], depth + 1, new_state))
            if(len(new_frontiers) == 0): continue



            if new_frontiers[0][0] == self.player_number:
            # if i == max_depth - 1:
                for moves in new_frontiers:
                    if(time.time() - start_time > self.time - 0.5):
                        # logging.debug(f'Best move = {best_move}')
                        return best_move
                    new_my_score = get_pts(self.player_number, moves[3][0])
                    new_opp_score = get_pts(opp_player_num, moves[3][0])
                    # if max_diff < (new_my_score):
                    #     best_move = valid_moves[moves[1]]
                    #     max_diff = (new_my_score)
                    # logging.debug(moves[3][0])
                    # logging.debug(f'move {valid_moves[moves[1]]} new score = {new_my_score}, opp score = {new_opp_score}')
                    # logging.debug(f'Player {self.player_number}, new score = {new_my_score}, Player {opp_player_num}, opp score = {new_opp_score}')

                    if max_diff < (new_my_score - new_opp_score):
                        best_move = valid_moves[moves[1]]
                        max_diff = (new_my_score - new_opp_score)
                        # logging.debug(f'max diff = {max_diff}')
            frontiers = new_frontiers
            new_frontiers = []

        # logging.debug(f'Best move Gg = {best_move}')
        # print(f"Time taken {time.time()-start_time} ")
        return best_move


            


            # dfs_stack = valid_moves
            # pot_states = []
            # for i in range()
            # valid_moves_new = get_valid_actions(self.player_number, state)
            # for i in range(len(valid_moves_new)):
            #     dfs_stack.append(new_state)

            # depth = depth + 1
            # for x in valid_moves:
            #     dfs_stack.append((new_state, my_level, idx))

            # while(True):
            #     my_level = (my_level + 1)%2
            #     valid_moves_new = get_valid_actions(self.player_number, state)
            #     depth = depth + 1
            #     for x in valid_moves:
            #         dfs_stack.append((new_state, my_level, idx))
                
            # valid_actions = get_valid_actions(self.player_number, state)
            # action, is_popout = random.choice(valid_actions)
            # return action, is_popout

        # raise NotImplementedError('Whoops I don\'t know what to do')