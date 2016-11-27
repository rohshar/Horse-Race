import numpy as np
import collections
import copy
import sys
import os
import math

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
		total += teamLikelihood(team_indices, horse_performance)
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

def nextHorse(candidates, horse_performance, lst_of_sinks):
	'''Given candidates, find horse with best performance'''
	nextHorse = None
	bestPerformance = -float("inf")
	for i in candidates:

		# TODO: test out different values of delta and temperature. Maybe we need some other helpers to determine that.
		# I added the -1.0 because the book is trying to minimize the cost - while we are trying to maximize it.
		delta = -1.0 * (horse_performance[i] - bestPerformance)
		temperature = 1.0

		if nextHorse not in lst_of_sinks and i not in lst_of_sinks:
			# 1. If both are not sinks, use Simulated Annealing to choose the horse

			# First, if i is the better one, we will take it.
			if horse_performance[i] > bestPerformance:
				bestPerformance = horse_performance[i]
				nextHorse = i

			else:
				# If i is the worse one: Generate a random number. If it is lower than delta/temperature,
				# then we replace our solution with the worse one, i.
				rand_num = np.random.random_sample()
				prob = math.exp(-1.0*delta/temperature)

				if rand_num <= prob:
					bestPerformance = horse_performance[i]
					nextHorse = i

		elif nextHorse in lst_of_sinks and i in lst_of_sinks:
			# 2. If both are sinks, use Simulated Annealing but skew it highly to the horse with higher performance.

			temp_temperature = temp * 0.001 # Decrease temperature such that it will skew towards the one with higher performance.

			# First, if i is the better one, we will take it.
			if horse_performance[i] > bestPerformance:
				bestPerformance = horse_performance[i]
				nextHorse = i

			else:
				# If i is the worse one: Generate a random number. If it is lower than delta/temperature,
				# then we replace our solution with the worse one, i.
				rand_num = np.random.random_sample()
				prob = math.exp(-1.0*delta/temp_temperature)

				if rand_num <= prob:
					bestPerformance = horse_performance[i]
					nextHorse = i

		elif ( (nextHorse in lst_of_sinks and i not in lst_of_sinks) and (bestPerformance >= horse_performance[i]) ) \
			or ( (nextHorse not in lst_of_sinks and i in lst_of_sinks) and (bestPerformance <= horse_performance[i]) ):
			# 3. If A is a sink, B is not, performance(A) > performance(B): use Simulated Annealing

			temp_next_horse = nextHorse
			temp_best_performance = bestPerformance

			# First, if i is the better one, we will take it.
			if horse_performance[i] > bestPerformance:
				bestPerformance = horse_performance[i]
				nextHorse = i

			# If i is the sink and it has better performance, see if we use simulated annealing to choose it.
			if i in sink:
				rand_num = np.random.random_sample()
				prob = math.exp(-1.0*delta/temp_temperature)

				if rand_num <= prob:
					bestPerformance = horse_performance[i]
					nextHorse = i

			# Last current choice is the sink and it has better performance. See if we can use simulated annealing to choose it.
			else:
				rand_num = np.random.random_sample()
				prob = math.exp(-1.0*delta/temp_temperature)

				if rand_num <= prob:
					bestPerformance = temp_best_performance
					nextHorse = temp_next_horse

		elif ( (nextHorse in lst_of_sinks and i not in lst_of_sinks) and (bestPerformance <= horse_performance[i]) ) \
			or ( (nextHorse not in lst_of_sinks and i in lst_of_sinks) and (bestPerformance >= horse_performance[i]) ):
			# 4. If A is a sink, B is not, performance(B) > performance(A): use Simulated Annealing, very very highly skewed towards B

			temp_temperature = temp * 0.001 # Decrease temperature such that it will skew towards the one with higher performance.
			temp_next_horse = nextHorse
			temp_best_performance = bestPerformance

			# First, if i is the better one, we will take it.
			if horse_performance[i] > bestPerformance:
				bestPerformance = horse_performance[i]
				nextHorse = i

			# If i is the sink and it has worse performance, see if we use simulated annealing to choose it.
			if i in sink:
				rand_num = np.random.random_sample()
				prob = math.exp(-1.0*delta/temp_temperature)

				if rand_num <= prob:
					bestPerformance = horse_performance[i]
					nextHorse = i

			# Last current choice is the sink and it has worse performance. See if we can use simulated annealing to choose it.
			else:
				rand_num = np.random.random_sample()
				prob = math.exp(-1.0*delta/temp_temperature)

				if rand_num <= prob:
					bestPerformance = temp_best_performance
					nextHorse = temp_next_horse

		else:
			# If none of these cases fits, then we just do what we did before.

			if horse_performance[i] > bestPerformance:
				bestPerformance = horse_performance[i]
				nextHorse = i

		temp *= 0.1 # We should make temperature gradually smaller (P.292 in the book)

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


def optimalHorseRacing(in_file):
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

			# Since now we consider both sinks or non-sinks, I commented out the if branch and modified
			# the arguments to nextHorse. Now it takes in a list of sinks.

			# If all horses that can go after curr is a sink, then pick sink with best performance
			# if np.all(np.in1d(candidates, sinkIdx)):
			# 	# curr is horse with best performance
			# 	curr = nextHorse(candidates, horse_performance)
			# 	sinkIdx.remove(curr)
			# # Else if there are still non-sinks left, pick horse with best performance
			# else:
			# 	# Remove sinks from consideration because non-sinks still left
			# 	candidates = np.setdiff1d(candidates, sinkIdx)
			# 	# curr is horse with best performance
			# 	curr = nextHorse(candidates, horse_performance)
			# 	horseIdx.remove(curr)

			# Get the list of sinks for our next horse call.
			lst_of_sinks = np.setdiff1d(candidates, sinkIdx)
			# curr is horse with best performance
			curr = nextHorse(candidates, horse_performance, lst_of_sinks)
			horseIdx.remove(curr)

			usedHorses.append(curr)
			team.append(curr)
			candidates = getValidCandidates(horse_compatibilities[curr], usedHorses)
		teams.append(team)
	return parseTeams(teams)


if __name__ == "__main__":
	with open("answers.out", "r+") as ofile:
		ofile.truncate()
		#files = os.listdir("cs170_final_inputs")
		all_files = next(os.walk('sample_checker'))[2]
		files = [f for f in all_files if not f.startswith('.')]
		for f in files:
			#team_rep = optimalHorseRacing("cs170_final_inputs/" + f)
			team_rep = optimalHorseRacing("sample_checker/" + f)
			ofile.write(team_rep + "\n")

	#f = "sample1.in"
	#print(optimalHorseRacing(f))
