import numpy as np
import collections
import random
import copy
import sys
import os
import pdb

def processInput(in_file):
        # Read text file into a 2d numpy array. First row skipped because matrix starts on second row
        horse_compatibilities = np.loadtxt(in_file, skiprows=1, dtype=int)

        # Diagonal values of 2d numpy array retrieved and converted into 1d numpy array
        horse_performance = copy.deepcopy(horse_compatibilities.diagonal())

        # Set diagonal elements of mat to 0, in-place. Now horse_compatibilities 2d array strictly contain 
        # information on whether horse j can run after horse i
        np.fill_diagonal(horse_compatibilities, 0)

        return horse_performance, horse_compatibilities

def findSource(mat):
        '''Returns set of sources from compatibility matrix'''
        # Find sources (no horses can go before them) by identifying columns with all zeros
        return set(np.where(~mat.any(axis=0))[0])

def findSink(mat):
        '''Returns set of sinks from compatibility matrix'''
        # Find sinks (no horses can go after them) by identifying rows with all zeros
        return set(np.where(~mat.any(axis=1))[0])

def adjacencyMatrix(mat):
        '''Turns matrix of compatibilities into adjacency matrix'''
        adjMat = {}
        # For each row in compatibility matrix
        for i in range(mat.shape[0]):
                # Find j corresponding for where mat[i][j] = 1
                adjMat[i] = np.where(mat[i] == 1)[0]

        return adjMat

def totalLikelihood(teams, horse_performance):
        #calculate total likelihood of winning based on all teams created
        total = 0
        for team in teams:
                total += teamLikelihood(team, horse_performance)
        return total


def teamLikelihood(team_indices, horse_performance):
        #calculate likelihood of individual team winning based on formula described in spec
        #where team_indices contains the index of all of the horses that race with one 
        #specific team
        total = 0
        for ti in team_indices:
                total += horse_performance[ti]
        scaled_total = total * len(team_indices)
        return scaled_total

def nextHorse(candidates, horse_performance, eps):
        '''Given candidates, find horse with best performance 1-EPS of the time
           In EPS of the cases, we just choose randomly
        '''
        if random.random() < eps:
                return candidates[random.randrange(0, len(candidates))]
        
        nextHorse = None
        bestPerformance = -float("inf")
        for i in candidates:
                if horse_performance[i] > bestPerformance:
                        bestPerformance = horse_performance[i]
                        nextHorse = i
        return nextHorse

def getValidCandidates(candidates, usedHorses):
        return np.setdiff1d(candidates, usedHorses)


def parseTeams(teams):
        race_output = ""
        for i in range(len(teams)):
                for j in range(len(teams[i])):
                        if (j == len(teams[i]) - 1) and (i == len(teams) - 1):
                                race_output += str(teams[i][j])
                        elif j == len(teams[i]) - 1:
                                race_output += str(teams[i][j]) + "; "
                        else:   
                                race_output += str(teams[i][j]) + " "
        return race_output

# [MICHAEL] Almost the same as OPTIMALHORSERACING1 except with a random factor EPS
def randomizedSolution(horse_performance, horse_compatibilities, eps):
        # Find source and sink IDs respectively
        sourceIdx = findSource(horse_compatibilities)
        sinkIdx = findSink(horse_compatibilities)

        # Represent each horse by its index
        horseIdx = set(range(len(horse_compatibilities)))

        # Remove sinks from horseIdx
        horseIdx = horseIdx.difference(sinkIdx)

        # Remove sources from horseIdx  
        horseIdx = collections.deque(horseIdx.difference(sourceIdx))

        # Convert horse_compatibilities to adjacency matrix
        horse_compatibilities = adjacencyMatrix(horse_compatibilities)

        teams = []
        usedHorses = []
        sourceIdx = list(sourceIdx)
        sinkIdx = list(sinkIdx)
        # While there are still unassigned horses left
        while len(horseIdx) > 0 or len(sourceIdx) > 0 or len(sinkIdx) > 0:
                team = []
                # If there are sources, use them as starting horse in the team. curr denotes current horse
                # [MICHAEl] Choices of start node for a team are made randomly drawing from the appropriate set
                # (sourceIdx, horseIdx, or sinkIdx)
                if len(sourceIdx) > 0:
                        #team.append(sourceIdx.pop())
                        team.append(sourceIdx[random.randrange(0, len(sourceIdx))])
                        curr = team[0]
                        sourceIdx.remove(curr)
                        if curr in sinkIdx:
                                sinkIdx.remove(curr)
                # If there are no sources left, pick next available horse as the first horse to start in the team
                elif len(horseIdx) > 0:
                        #team.append(horseIdx.pop())
                        team.append(horseIdx[random.randrange(0, len(horseIdx))])
                        curr = team[0]
                        horseIdx.remove(curr)
                # If sinks are the only horses left, then form team with sinks
                else:
                        #team.append(sinkIdx.pop())
                        team.append(sinkIdx[random.randrange(0, len(sinkIdx))])
                        curr = team[0]
                        sinkIdx.remove(curr)
                usedHorses.append(curr)
                # Remove from consideration horses that have been used
                candidates = getValidCandidates(horse_compatibilities[curr], usedHorses)
                while len(candidates) > 0:
                        # If all horses that can go after curr is a sink, then pick sink with best performance
                        if np.all(np.in1d(candidates, sinkIdx)):
                                # curr is horse with best performance, most of the time
                                curr = nextHorse(candidates, horse_performance, eps)
                                sinkIdx.remove(curr)
                                if curr in sourceIdx:
                                        sourceIdx.remove(curr)
                        # Else if there are still non-sinks left, pick horse with best performance
                        else:
                                # Remove sinks from consideration because non-sinks still left
                                candidates = np.setdiff1d(candidates, sinkIdx)
                                # curr is horse with best performance, most of the time
                                curr = nextHorse(candidates, horse_performance, eps)
                                horseIdx.remove(curr)
                        usedHorses.append(curr)
                        team.append(curr)
                        candidates = getValidCandidates(horse_compatibilities[curr], usedHorses)
                teams.append(team)
        return teams
        
# The nonrandom, greedy version
def optimalHorseRacing1(in_file):
        #call helper function to get relevant information in accessible format
        horse_performance, horse_compatibilities = processInput(in_file)

        # Find source and sink IDs respectively
        sourceIdx = findSource(horse_compatibilities)
        sinkIdx = findSink(horse_compatibilities)

        # Represent each horse by its index
        horseIdx = set(range(len(horse_compatibilities)))

        # Remove sinks from horseIdx
        horseIdx = horseIdx.difference(sinkIdx)

        # Remove sources from horseIdx  
        horseIdx = collections.deque(horseIdx.difference(sourceIdx))

        # Convert horse_compatibilities to adjacency matrix
        horse_compatibilities = adjacencyMatrix(horse_compatibilities)

        teams = []
        usedHorses = []
        sourceIdx = list(sourceIdx)
        sinkIdx = list(sinkIdx)
        # While there are still unassigned horses left
        while len(horseIdx) > 0 or len(sourceIdx) > 0 or len(sinkIdx) > 0:
                team = []
                # If there are sources, use them as starting horse in the team. curr denotes current horse
                if len(sourceIdx) > 0:
                        team.append(sourceIdx.pop())
                        curr = team[0]
                        if curr in sinkIdx:
                                sinkIdx.remove(curr)
                # If there are no sources left, pick next available horse as the first horse to start in the team
                elif len(horseIdx) > 0:
                        team.append(horseIdx.pop())
                        curr = team[0]
                # If sinks are the only horses left, then form team with sinks
                else:
                        team.append(sinkIdx.pop())
                        curr = team[0]
                usedHorses.append(curr)
                # Remove from consideration horses that have been used
                candidates = getValidCandidates(horse_compatibilities[curr], usedHorses)
                while len(candidates) > 0:
                        # If all horses that can go after curr is a sink, then pick sink with best performance
                        if np.all(np.in1d(candidates, sinkIdx)):
                                # curr is horse with best performance
                                curr = nextHorse(candidates, horse_performance, 0)
                                sinkIdx.remove(curr)
                                if curr in sourceIdx:
                                        sourceIdx.remove(curr)
                        # Else if there are still non-sinks left, pick horse with best performance
                        else:
                                # Remove sinks from consideration because non-sinks still left
                                candidates = np.setdiff1d(candidates, sinkIdx)
                                # curr is horse with best performance
                                curr = nextHorse(candidates, horse_performance, 0)
                                horseIdx.remove(curr)
                        usedHorses.append(curr)
                        team.append(curr)
                        candidates = getValidCandidates(horse_compatibilities[curr], usedHorses)
                teams.append(team)
        return totalLikelihood(teams, horse_performance), teams

# The random, greedy version. Essentially we introduce randomness and run a bunch of times,
# taking the best result of those runs
def optimalHorseRacing2(in_file):
        horse_performance, horse_compatibilities = processInput(in_file)

        num_runs = 50
        best_teams = []
        best_teams_val = -1
        for i in range(num_runs):
                curr_teams = randomizedSolution(horse_performance, horse_compatibilities, 1.0)
                curr_teams_val = totalLikelihood(curr_teams, horse_performance)
                if curr_teams_val > best_teams_val:
                        best_teams_val = curr_teams_val
                        best_teams = curr_teams
                
        return best_teams_val, best_teams

# Longest path approach - calling it many times so it is better to use high order functions        
def optimalHorseRacing3(in_file):
        # Call helper function to get relevant information in accessible format
        horse_performance, horse_compatibilities = processInput(in_file)

        num_runs = 50
        best_teams = []
        best_teams_val = -1
        for i in range(num_runs):
                curr_teams_val, curr_teams = LongestPathSolution(horse_performance, horse_compatibilities, 1.0)
                if curr_teams_val > best_teams_val:
                        best_teams_val = curr_teams_val
                        best_teams = curr_teams

        return best_teams_val, best_teams

# The longest path approach
def LongestPathSolution(horse_performance, horse_compatibilities, eps):

        # Find source and sink IDs respectively
        sourceIdx = findSource(horse_compatibilities)
        sinkIdx = findSink(horse_compatibilities)

        # Represent each horse by its index
        horseIdx = set(range(len(horse_compatibilities)))

        # Remove sinks from horseIdx
        horseIdx = horseIdx.difference(sinkIdx)

        # Remove sources from horseIdx  
        horseIdx = collections.deque(horseIdx.difference(sourceIdx))

        # Convert horse_compatibilities to adjacency matrix
        horse_compatibilities = adjacencyMatrix(horse_compatibilities)

        teams = []
        usedHorses = []
        sourceIdx = list(sourceIdx)
        sinkIdx = list(sinkIdx)
        removedNodes = set()

        # While there are still unassigned horses left
        while len(horseIdx) > 0 or len(sourceIdx) > 0 or len(sinkIdx) > 0:

                # New Code

                # If there are sources, use them as starting horse to find the longest path for. Use our helper which returns
                # the longest path and the resulting new graph with all nodes on the path removed. Starting from horse is the same.
                # Except we pick a different list of starting nodes
                if len(sourceIdx) > 0 or len(horseIdx) > 0:

                        if len(sourceIdx) > 0:
                                startingNodesForLongestPaths = list(sourceIdx)[:]
                        else:
                                # If there are no sources left, use the next available horses as the first horse as the first horse
                                # in the longest path. Use our helper which returns the longest path and the resulting new graph 
                                # with all nodes on the path removed.
                                startingNodesForLongestPaths = list(horseIdx)[:]

                        max_performance = -1
                        max_node = None

                        for node in startingNodesForLongestPaths:
                                if max_performance < horse_performance[node]:
                                        max_performance = horse_performance[node]
                                        max_node = node

                        if random.random() < eps:
                            # print "hiii"
                            max_node = startingNodesForLongestPaths[random.randrange(0, len(startingNodesForLongestPaths))]

                        team, resultingGraph = findLongestPath([max_node], horse_compatibilities)

                        # Record which nodes are being removed. Then, we will remove those nodes in our horseIdx/srcIdx/sinkIdx lists
                        for node in team:
                                removedNodes.add(node)

                        # Update horseIdx, sourceIdx, sinkIdx
                        sourceIdx = findSource(resultingGraph)
                        sinkIdx = findSink(resultingGraph)
                        horseIdx = set(range(len(horse_compatibilities)))
                        horseIdx = (horseIdx - sourceIdx) - sinkIdx

                        # Remove all the nodes that are on the path we found
                        for node in removedNodes:
                                if node in sourceIdx:
                                    sourceIdx.remove(node)

                                if node in sinkIdx:
                                    sinkIdx.remove(node)

                                if node in horseIdx:
                                    horseIdx.remove(node)

                        horse_compatibilities = adjacencyMatrix(resultingGraph)

                        sourceIdx = list(sourceIdx)
                        sinkIdx = list(sinkIdx)
                        horseIdx = list(horseIdx)

                # If sinks are the only horses left, then form team with sinks
                else:
                        team.append(sinkIdx.pop())

                teams.append(team)

        return totalLikelihood(teams, horse_performance), teams

def findLongestPath(startingNodesForLongestPaths, horse_compatibilities):

        # Use DFS to find all paths reachable from the starting nodes.

        allLongestPaths = []

        for cur_node in startingNodesForLongestPaths:

                possiblePaths = []

                # Make a visited array to represent if the node has been visited before
                visited = set()

                # Have a stack to keep track of all the paths we have found so far
                pathStack = [[cur_node]]

                while pathStack:
                        cur_path = pathStack.pop()

                        last_node = cur_path[len(cur_path) - 1]

                        if last_node in visited: 
                                continue

                        # Add this path to the list of all possible paths
                        possiblePaths.append(cur_path)

                        # Mark the last node on the path as visited
                        visited.add(last_node)

                        # Get a list of unvisited and reachable nodes from the last node on the current path
                        nextPossibleNodes = horse_compatibilities[last_node][:]

                        # Append all possible next nodes to the current path we have. Push it onto the stack.
                        for node in nextPossibleNodes:
                                new_path = cur_path[:] + [node]
                                pathStack.append(new_path)

                # Sort this list of paths. Longest path is in the front
                sorted_lst_by_length = sorted(possiblePaths, key=lambda lst: -len(lst))

                # Get the longest path
                allLongestPaths.append(sorted_lst_by_length[0])

        allLongestPathsSorted = sorted(allLongestPaths, key=lambda lst: -len(lst))

        resultingGraphRemovedNodes = removingNodesOnPath(allLongestPathsSorted[0], horse_compatibilities)

        return allLongestPathsSorted[0], resultingGraphRemovedNodes

def removingNodesOnPath(path, horse_compatibilities):
        # Reconstruct the matrix
        new_matrix = [[0]*len(horse_compatibilities)]*len(horse_compatibilities)

        for node in path:
                # Mark the row for the node as removed
                new_matrix[node] = [0]*len(horse_compatibilities)

                # Mark the col for the node as removed
                for i in xrange(0, len(horse_compatibilities)):
                        new_matrix[i][node] = 0

        return np.array(new_matrix)

if __name__ == "__main__":
        counter = 1
        with open("answers_opt2_and_3_Michael_434_439.out", "r+") as ofile, open("perf_opt2_and_3_Michael_434_439.out", "r+") as pfile:
                ofile.truncate()
                pfile.truncate()
                all_files = next(os.walk('cs170_final_inputs_434_439'))[2]
                # all_files = next(os.walk('sample_checker'))[2]
                files = [f for f in all_files if not f.startswith('.')]
                files.sort(key = lambda x: int(x.split('.')[0]))

                for f in files:

                        print(counter)
                        print f
                        perf2, teams2 = optimalHorseRacing2("cs170_final_inputs_434_439/" + f)
                        horse_performance, ignore = processInput("cs170_final_inputs_434_439/" + f)

                        perf3, teams3 = optimalHorseRacing3("cs170_final_inputs_434_439/" + f)
                        horse_performance, ignore = processInput("cs170_final_inputs_434_439/" + f)

                        # perf2, teams2 = optimalHorseRacing2("sample_checker/" + f)
                        # horse_performance, ignore = processInput("sample_checker/" + f)

                        # perf3, teams3 = optimalHorseRacing3("sample_checker/" + f)
                        # horse_performance, ignore = processInput("sample_checker/" + f)

                        if perf2 >= perf3:
                            teams = teams2
                            perf = perf2
                        else:
                            print "optimalHorseRacing3 is better!"
                            teams = teams3
                            perf = perf3

                        team_rep = parseTeams(teams)
                        ofile.write(team_rep + "\n")
                        pfile.write(str(perf) + "\n")
                        counter = counter + 1
                      
        '''

        #f = 'sample_checker/15.in'
        f = '289.in'
        val1, teams1 = optimalHorseRacing1(f)
        val2, teams2 = optimalHorseRacing2(f)
        pdb.set_trace()
        print("val1: " + str(val1) + ", val2: " + str(val2))
        '''
