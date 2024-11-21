from state import State, State_2
import time
from importlib import import_module
import statistics
import sys
  
def run(player_X, player_O, rule = 2):
    dict_player = {1: 'X', -1: 'O'}
    if rule == 1:
        cur_state = State()
    else:
        cur_state = State_2()
    turn = 1    

    limit = 81
    remain_time_X = 120
    remain_time_O = 120
    
    player_1 = import_module(player_X)
    player_2 = import_module(player_O)
    times_of_player_X = []
    times_of_player_O = []
    winner = 0
    
    while turn <= limit:
        #print("turn:", turn, end='\n\n')
        if cur_state.game_over:
            winner = dict_player[cur_state.player_to_move * -1]
            print("winner:", dict_player[cur_state.player_to_move * -1])
            break
        
        start_time = time.time()
        if cur_state.player_to_move == 1:
            new_move = player_1.select_move(cur_state, remain_time_X)
            elapsed_time = time.time() - start_time
            remain_time_X -= elapsed_time
            times_of_player_X.append(elapsed_time)
        else:
            new_move = player_2.select_move(cur_state, remain_time_O)
            elapsed_time = time.time() - start_time
            remain_time_O -= elapsed_time
            times_of_player_O.append(elapsed_time)
            
        #print("elasped time: {}\n".format(elapsed_time))
        
        if new_move == None:
            break
        
        if remain_time_X < 0 or remain_time_O < 0:
            winner = dict_player[cur_state.player_to_move * -1]
            print("out of time")
            print("winner:", dict_player[cur_state.player_to_move * -1])
            break
                
        if elapsed_time > 10.0:
            winner = dict_player[cur_state.player_to_move * -1]
            print("elapsed time:", elapsed_time)
            print("winner: ", dict_player[cur_state.player_to_move * -1])
            break
        
        cur_state.act_move(new_move)
        #print(cur_state)
        
        turn += 1
        
    print("X:", cur_state.count_X)
    print("O:", cur_state.count_O)

    if len(times_of_player_X) == 0:
        times_of_player_X.append(0)
    
    if len(times_of_player_O) == 0:
        times_of_player_O.append(0)
    
    return winner, times_of_player_X, times_of_player_O

class Player:
    def __init__(self, model):
        self.times_in_rounds = []
        self.model = model
        self.rounds_win = 0
    
    def add_times_after_a_round(self, time_in_turns: list):
        self.times_in_rounds.append(time_in_turns)
        
    def get_avg_time_per_turn(self):
        flattened_list = [num for round in self.times_in_rounds for num in round]
        return statistics.mean(flattened_list)
    
    def get_avg_sum_time(self):
        total = []
        for round in self.times_in_rounds:
            total.append(sum(round))
        return statistics.mean(total)
    
    def get_max_time(self):
        time = 0
        for round in self.times_in_rounds:
            time = max(time, max(round))
        return time

    
def play_a_round(player_X, player_O):
    print("X: {}\nO: {}\n".format(player_X.model, player_O.model))
        
    winner, times_of_player_X, times_of_player_O = run(player_X.model, player_O.model)
    if winner == 'X':
        player_X.rounds_win += 1
    elif winner == 'O':
        player_O.rounds_win += 1
        
    player_X.add_times_after_a_round(times_of_player_X)
    player_O.add_times_after_a_round(times_of_player_O)

def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py <player 1 model> <player 2 model> <number of rounds>")
        return
    
    player_1_model = sys.argv[1]
    player_2_model = sys.argv[2]
    total_match = int(sys.argv[3])
    
    player_1 = Player(player_1_model)
    player_2 = Player(player_2_model)
    
    print("\nMatch: {} (1) vs {} (2)".format(player_1.model, player_2.model))
    for i in range(total_match):
        print("\nRound {}/{}:".format(i+1, total_match))
        if i % 2 == 0:
            play_a_round(player_1, player_2)
        else:
            play_a_round(player_2, player_1)
    
    draw = total_match - player_1.rounds_win - player_2.rounds_win
    
    print("\nOverall stats:\n")
    print("Player 1: win={} lose={} draw={} rate={}".format(player_1.rounds_win, player_2.rounds_win, draw, player_1.rounds_win/total_match))
    
    print("Player 1's average total thinking time: {}".format(player_1.get_avg_sum_time()))
    print("Player 1's average thinking time per turn: {}".format(player_1.get_avg_time_per_turn()))
    print("Player 1's max thinking time: {}\n".format(player_1.get_max_time()))
    
    print("Player 2: win={} lose={} draw={} rate={}".format(player_2.rounds_win, player_1.rounds_win, draw, player_2.rounds_win/total_match))
    
    print("Player 2's average total thinking time: {}".format(player_2.get_avg_sum_time()))
    print("Player 2's average thinking time per turn: {}".format(player_2.get_avg_time_per_turn()))
    print("Player 2's max thinking time: {}\n".format(player_2.get_max_time()))


main()