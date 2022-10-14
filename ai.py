#  conda activate myenv
# python3 -m connect4.ConnectFour random ai connect4/initial_states/case1.txt --time 10


# import random
from os import stat
import numpy as np
import time
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer


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
        # Do the rest of your implementation here

    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move
        This will play against either itself or a human player
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        # Do the rest of your implementation here
        raise NotImplementedError('Whoops I don\'t know what to do')

    def update_state(self, state_1: Tuple[np.array, Dict[int, Integer]], action: Tuple[int, bool], player_number: int):
        # print(f"action: {action} player: {player_number} popout: {state[1][player_number].get_int()}")

        if(state_1[1][player_number].get_int() == 0): return state_1
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
            # print(f'-------Player num = {player_number}---------{state[1][player_number].get_int()}')
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

        # if(first_occupied_row < 0): return array

        if(action[1] == True):
            for r in range(len(array)-1, 0, -1):
                array[r, column] = array[r - 1, column]
            array[0, column] = 0
        elif(first_occupied_row < 0): return array
        else:
            array[first_occupied_row][column] = self.player_number

        return array

    def get_expectimax_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        # Do the rest of your implementation here
        start_time = time.time()
        valid_moves = get_valid_actions(self.player_number, state)
        # print(f'Valid moves at start :{valid_moves}')
        # start_state = state
        best_move = valid_moves[0]
        frontiers = []
        opp_player_num = 1 + (self.player_number)%2
        depth = 1

        # pop_outs = state[1][self.player_number].get_int()        
        # if(pop_outs < 4):
        #     max_depth = 1
        # else:
        #     max_depth = 2
            
        # if(pop_outs < 4):
        #     max_depth = 1
        # elif(pop_outs < 6):
        #     max_depth = 2
        # else:
        #     max_depth = 3

        max_depth = 3

        max_diff = 0


        if(np.sum(state[0])<3):
            return ((len(state[0][0])//2, False))

        for i in range(len(valid_moves)):
            # print(f'Valid move -- {valid_moves[i]}')
            new_state = self.update_state(state, valid_moves[i], self.player_number)
            frontiers.append((self.player_number, i, depth, new_state))
        
        # print(f'Out of first loop ')

        # print(f'Popouts remaining = {state[1][self.player_number].get_int()}')
        

        for _ in range(max_depth):
            if(time.time() - start_time > self.time - 0.1):
                # print(f'Best move = {best_move}')
                return best_move
            
            new_frontiers = []

            while(len(frontiers)>0):
                if(time.time() - start_time > self.time - 0.1):
                    # print(f'Best move = {best_move}')
                    return best_move
                new_move = frontiers.pop(0)
                new_valid_moves = get_valid_actions(1 + (new_move[0]+1)%2, new_move[3])
                for j in range(len(new_valid_moves)):
                    if(time.time() - start_time > self.time - 0.1):
                        # print(f'Best move = {best_move}')
                        return best_move
                    # print(f'Player = {1+(new_move[0]+1)%2} -- {new_valid_moves[j]}')
                    new_state = self.update_state(new_move[3], new_valid_moves[j], new_move[0])
                    new_frontiers.append((1 + (new_move[0]+1)%2, new_move[1], depth + 1, new_state))
            if new_frontiers[0][0] == self.player_number:
                for moves in new_frontiers:
                    if(time.time() - start_time > self.time - 0.1):
                        # print(f'Best move = {best_move}')
                        return best_move
                    new_my_score = get_pts(self.player_number, moves[3][0])
                    new_opp_score = get_pts(opp_player_num, moves[3][0])
                    # if max_diff < (new_my_score):
                    #     best_move = valid_moves[moves[1]]
                    #     max_diff = (new_my_score)
                    # print(f'new score = {new_my_score}, opp score = {new_opp_score}')
                    # print(f'Player {self.player_number}, new score = {new_my_score}, Player {opp_player_num}, opp score = {new_opp_score}')

                    if max_diff < (new_my_score - new_opp_score):
                        best_move = valid_moves[moves[1]]
                        max_diff = (new_my_score - new_opp_score)
                        # print(f'max diff = {max_diff}')
            frontiers = new_frontiers
            new_frontiers = []

        # print(f'Best move = {best_move}')
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
