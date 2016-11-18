import numpy as np
import collections
import copy
import sys

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

def nextHorse(candidates, horse_performance):
	'''Given candidates, find horse with best performance'''
	nextHorse = None
	bestPerformance = -float("inf")
	for i in candidates:
		if horse_performance[i] > bestPerformance:
			bestPerformance = horse_performance[i]
			nextHorse = i
	return nextHorse

def getValidCandidates(candidates, usedHorses):
	return np.setdiff1d(candidates, usedHorses)

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
			# If all horses that can go after curr is a sink, then pick sink with best performance
			if np.all(np.in1d(candidates, sinkIdx)):
				# curr is horse with best performance
				curr = nextHorse(candidates, horse_performance)
				sinkIdx.remove(curr)
			# Else if there are still non-sinks left, pick horse with best performance
			else:
				# Remove sinks from consideration because non-sinks still left
				candidates = np.setdiff1d(candidates, sinkIdx)
				# curr is horse with best performance
				curr = nextHorse(candidates, horse_performance)
				horseIdx.remove(curr)
			usedHorses.append(curr)
			team.append(curr)
			candidates = getValidCandidates(horse_compatibilities[curr], usedHorses)
		teams.append(team)
	print(teams)
	return teams


if __name__ == "__main__":
	f = "sample1.in"
	optimalHorseRacing(f)
