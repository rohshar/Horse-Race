import numpy as np
import collections
import copy

def processInput(in_file):
	# Read text file into matrix
	horse_compatibilities = np.loadtxt(in_file, skiprows=1, dtype=int)

	# Get diagonal values
	horse_performance = copy.deepcopy(horse_compatibilities.diagonal())

	# Set horse compatibilities, setting diagonal elements of mat to 0, in-place
	np.fill_diagonal(horse_compatibilities, 0)

	return horse_performance, horse_compatibilities

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


def optimalHorseRacing(in_file):
	#call helper function to get relevant information in accessible format
	horse_performance, horse_compatibilities = processInput(in_file)

	horseIdx = set(range(horse_compatibilities.shape[0]))
	# Indices of horses that are sources (no horses can go before)
	sourceIdx = list(np.where(~horse_compatibilities.any(axis=0))[0])
	# Rest of horse indices to iterate over
	horseIdx = collections.deque(horseIdx.difference(sourceIdx))

	teams = []
	# While there are still unassigned horses
	while len(horseIdx) > 0:
		team = []
		# If there are sources, use them as starting point of path
		if len(sourceIdx) > 0:
			team.append(sourceIdx.pop())
			curr = team[0]
		else:
			team.append(horseIdx.popleft())
			curr = team[0]
		isValid = True
		# Continue increasing team until a horse that can go after
		while isValid:
			for j in range(horse_compatibilities.shape[0]):
				if horse_compatibilities[curr][j] == 1 and j in horseIdx:
					team.append(j)
					horseIdx.remove(j)
					curr = j
					break
				elif j == horse_compatibilities.shape[0] - 1:
					isValid = False
		teams.append(team)
	print(teams)
	return teams


if __name__ == "__main__":
	f = "sample2.in"
	optimalHorseRacing(f)