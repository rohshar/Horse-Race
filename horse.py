def processInput(in_file):
	with open(in_file, "r") as ifile:
		#Get all of the lines in the file in a list
		file_lines = ifile.read().splitlines()
		#Figure out the total amount of horses
		num_lines = file_lines[0]
		#Array stores each horse's performace value corresponding to index
		horse_compatibilities = []
		#Array stores each horse's ability to run before any of the other horses
			#corresponding to index. A horse's ability to run before itself is 0.
			#If a horse i is willing to race before horse j, then horse_performace[i][j] = 1,
			#otherwise 0
		horse_performance = []
		#Go through the matrix and store performances and compatibilities in their
			#corresponding arrays after converting the numbers to integers
		for i in range(0, int(num_lines)):
			curr_line = file_lines[i + 1]
			elements = curr_line.split(" ")
			horse_performance.append(int(elements[i]))
			elements[i] = '0'
			for e in range(len(elements)):
				if elements[e] == '0' or elements[e] == '1':
					elements[e] = int(elements[e])
				else:
					elements.remove(elements[e])
			horse_compatibilities.append(elements)
	#return the relevant information
	return num_lines, horse_performance, horse_compatibilities

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


def isTeamValid(team_indices, horse_compatibilities):
	pass


def optimalHorseRacing(in_file):
	#call helper function to get relevant information in accessible format
	num_horses, horse_performance, horse_compatibilities = processInput(in_file)

	#print(num_horses)
	#print(horse_performance)
	#print(horse_compatibilities) 




if __name__ == "__main__":
	f = "sample1.in"
	optimalHorseRacing(f)