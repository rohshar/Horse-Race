import numpy as np
import collections
import copy

def processInput(in_file):
	# Read text file into a 2d numpy array. First row skipped because matrix starts on second row
	horse_compatibilities = np.loadtxt(in_file, skiprows=1, dtype=int)

	# Diagonal values of 2d numpy array retrieved and converted into 1d numpy array
	horse_performance = copy.deepcopy(horse_compatibilities.diagonal())

	# Set diagonal elements of mat to 0, in-place. Now horse_compatibilities 2d array strictly contain 
	# information on whether horse j can run after horse i
	np.fill_diagonal(horse_compatibilities, 0)

	return horse_performance, horse_compatibilities

def adjacencyMatrix(mat):
	'''Turns matrix of compatibilities into adjacency matrix'''
	adjMat = {}
	for i in range(mat.shape[0]):
		pass

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

	# Represent each horse by its index
	horseIdx = set(range(horse_compatibilities.shape[0]))
	# Find sources (no horses can go before them) by identifying columns with all zeros
	sourceIdx = list(np.where(~horse_compatibilities.any(axis=0))[0])
	# Take the complement of sources to be the rest of the horses
	horseIdx = collections.deque(horseIdx.difference(sourceIdx))

	teams = []
	# While there are still unassigned horses left
	while len(horseIdx) > 0:
		team = []
		# If there are sources, use them as starting horse in the team. curr denotes current horse
		if len(sourceIdx) > 0:
			team.append(sourceIdx.pop())
			curr = team[0]
		# If there are no sources left, pick next available horse as the first horse to start in the team
		else:
			team.append(horseIdx.popleft())
			curr = team[0]
		# isValid indicates whether there is a horse that can go after current horse
		isValid = True
		# Continue increasing team until no horse can go after current horse.
		while isValid:
			# Search for any horse that can go after current horse
			for j in range(horse_compatibilities.shape[0]):
				# If horse j can go after current horse, and horse j has not been assigned to a team already, 
				# add horse j to the team
				if horse_compatibilities[curr][j] == 1 and j in horseIdx:
					# Once horse j is added, remove horse j from unassigned horses (horseIdx), and set horse j as current
					team.append(j)
					horseIdx.remove(j)
					curr = j
					break
				# If no horse is available to run after current horse, set isValid to false to form the next team
				elif j == horse_compatibilities.shape[0] - 1:
					isValid = False
		teams.append(team)
	print(teams)
	return teams


if __name__ == "__main__":
	f = "sample2.in"
	optimalHorseRacing(f)