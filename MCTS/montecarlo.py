# Author: Andre Slavescu
# Description: This script intends to play tic tac toe independently.

# Objective:
#   The algorithm would need to take in the current state of the game and then evaluate all of the possible moves that could be made.
#   It would then need to choose the move that would result in the best possible outcome for the player.

# Monte Carlo Tree Search Algorithm:
# 1. parse the game state into a tree of nodes
# 2. each node has a value and a list of children
# 3. hold weights for each move that can be made to determine the best move

import random
import numpy as np
import pandas as pd

class Game:
    def __init__(self):
        self.board = np.zeros((3,3)) # game board - 3x3 matrix of 0's
        self.winner = None # player who won the game
        self.ended = False # game status - ended or not
        self.turn = 1 # current player's turn

    # check if the game has ended
    def is_game_over(self):
        # check if a player has won
        if (self.winner is not None):
            self.ended = True
            return True
        # check if the board is full
        elif (np.all(self.board != 0)):
            self.ended = True
            return True
        # game is not over
        else:
            return False

    # get the player who's turn it is
    def get_current_player(self):
        return 1 if self.turn == 1 else 2

    # check if a position is valid on the board
    def is_valid_position(self, row, col):
        return (self.board[row, col] == 0)

    # play a move on the board
    def play_move(self, row, col):
        # check if the position is valid
        if not self.is_valid_position(row, col):
            print("Invalid Move")
            return
        # play the move
        self.board[row, col] = self.get_current_player()
        # check if the game is over
        if self.is_game_over():
            self.winner = self.get_current_player()
        # change the turn
        self.turn += 1

    # get all the possible moves that can be made
    def get_possible_moves(self):
        possible_moves = []
        # loop through all the positions on the board
        for row in range(3):
            for col in range(3):
                # check if the position is valid
                if self.is_valid_position(row, col):
                    possible_moves.append((row, col))
        return possible_moves

    # get the state of the game as a string
    def get_state(self):
        return str(self.board.reshape(9))

    # print the current state of the game
    def print_board(self):
        for row in range(3):
            for col in range(3):
                value = self.board[row, col]
                print("X " if value == 1 else "O " if value == 2 else "_ ", end="")
            print()

# Monte Carlo Tree Search Algorithm
class MCTS:
    def __init__(self):
        self.nodes = {} # dictionary of nodes, each node is a key-value pair of (state, children)
        self.c = 1 # exploration parameter

    # get the child node with the highest value
    def get_child_with_max_value(self, node):
        # get the list of children for the node
        children = self.nodes[node][1]
        # init the max child and value
        max_child, max_value = None, -float("inf")
        # loop through all the children
        for child in children:
            # get the value of the child
            child_value = self.nodes[child][0]
            # update the max child and value
            if child_value > max_value:
                max_child, max_value = child, child_value
        return max_child, max_value

    # get the child node with the minimum value
    def get_child_with_min_value(self, node):
        # get the list of children for the node
        children = self.nodes[node][1]
        # init the min child and value
        min_child, min_value = None, float("inf")
        # loop through all the children
        for child in children:
            # get the value of the child
            child_value = self.nodes[child][0]
            # update the min child and value
            if child_value < min_value:
                min_child, min_value = child, child_value
        return min_child, min_value

    # get the child node with the maximum upper confidence bound
    def get_child_with_max_ucb(self, node):
        # get the list of children for the node
        children = self.nodes[node][1]
        # init the max child and ucb
        max_child, max_ucb = None, -float("inf")
        # loop through all the children
        for child in children:
            # get the value and number of visits for the child
            child_value, child_n = self.nodes[child][0], self.nodes[child][2]
            # compute the upper confidence bound
            ucb = child_value + self.c * np.sqrt(np.log(self.nodes[node][2]) / child_n)
            # update the max child and ucb
            if ucb > max_ucb:
                max_child, max_ucb = child, ucb
        return max_child, max_ucb

    # get the child node with the minimum lower confidence bound
    def get_child_with_min_lcb(self, node):
        # get the list of children for the node
        children = self.nodes[node][1]
        # init the min child and lcb
        min_child, min_lcb = None, float("inf")
        # loop through all the children
        for child in children:
            # get the value and number of visits for the child
            child_value, child_n = self.nodes[child][0], self.nodes[child][2]
            # compute the lower confidence bound
            lcb = child_value - self.c * np.sqrt(np.log(self.nodes[node][2]) / child_n)
            # update the min child and lcb
            if lcb < min_lcb:
                min_child, min_lcb = child, lcb
        return min_child, min_lcb

    # select the child node using the upper confidence bound
    def select_child_node_ucb(self, node):
        # get the child node with the maximum upper confidence bound
        max_child, max_ucb = self.get_child_with_max_ucb(node)
        # return the child node
        return max_child

    # select the child node using the lower confidence bound
    def select_child_node_lcb(self, node):
        # get the child node with the minimum lower confidence bound
        min_child, min_lcb = self.get_child_with_min_lcb(node)
        # return the child node
        return min_child

    # expand the tree by adding child nodes
    def expand_tree(self, node):
        # get the possible moves for the current state
        possible_moves = self.game.get_possible_moves()
        # select a random move
        random_move = random.choice(possible_moves)
        # get the child node
        child_node = self.game.get_state()
        # add the child node to the dictionary of nodes
        self.nodes[child_node] = (0, [], 1)
        # return the child node
        return child_node

    # simulate the game from the child node to the end
    def simulate_game(self, node):
        # create a new game instance
        game_sim = Game()
        # get the state of the game from the node
        state = node
        # loop until the game is over
        while not game_sim.is_game_over():
            # get the possible moves for the current state
            possible_moves = game_sim.get_possible_moves()
            # select a random move
            random_move = random.choice(possible_moves)
            # play the move
            row, col = random_move
            game_sim.play_move(row, col)
            # get the state of the game
            state = game_sim.get_state()
        # return the winner of the game
        return game_sim.winner

    # backpropagate the results of the simulation
    def backpropagate(self, node, winner):
        # update the value of the node
        self.nodes[node][0] += 1 if winner == self.game.get_current_player() else -1
        # update the number of visits for the node
        self.nodes[node][2] += 1
        # check if the node is the root node
        if node == self.root:
            return
        # get the parent node
        parent_node = self.nodes[node][3]
        # backpropagate from the parent node
        self.backpropagate(parent_node, winner)

    # get the best move for the current state
    def get_best_move(self):
        # get the list of child nodes
        children = self.nodes[self.root][1]
        # init the best move and value
        best_move, best_value = None, -float("inf")
        # loop through all the child nodes
        for child in children:
            # get the value of the child node
            child_value = self.nodes[child][0]
            # update the best move and value
            if child_value > best_value:
                best_move, best_value = child, child_value
        # return the best move
        return best_move

    # play the game
    def play(self, game, iterations):
        # set the game instance
        self.game = game
        # set the root node
        self.root = self.game.get_state()
        # add the root node to the dictionary of nodes
        self.nodes[self.root] = (0, [], 1)

        # loop for the specified number of iterations
        for i in range(iterations):
            # check if the game is over
            if self.game.is_game_over():
                break
            # select the child node
            child_node = self.select_child_node_ucb(self.root)
            # check if the child node is not in the dictionary of nodes
            if child_node not in self.nodes:
                # expand the tree
                child_node = self.expand_tree(child_node)
            # simulate the game from the child node
            winner = self.simulate_game(child_node)
            # backpropagate the results
            self.backpropagate(child_node, winner)

        # get the best move for the current state
        return self.get_best_move()

# Run the game for the specified number of iterations (default: 1000)
if __name__ == "__main__":
    # create a new game
    game = Game()
    # create a new MCTS algorithm
    mcts = MCTS()
    # play the game
    iterations = 1000
    best_move = mcts.play(game, iterations)
    print("Best Move:", best_move)
    print("Value:", mcts.nodes[best_move][0])
    print("Number of Visits:", mcts.nodes[best_move][2])


