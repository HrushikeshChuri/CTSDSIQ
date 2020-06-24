import numpy as np


MUTATION_RATE = 0.000001
MAX_ITERATION = 100000


class QueenSequence:
	def __init__(self):
		self.sequence = []
		self.fitness = 0
		self.probability = 0.0
	def setSequence(self, val):
		self.sequence = val
	def setFitness(self, fitness):
		self.fitness = fitness
	def setProbability(self, probability):
		self.probability = probability


def getFitness(seq):

	totalAttacks = 0;
	straight_attaks = abs(len(seq) - len(np.unique(seq)))
	totalAttacks += straight_attaks

	#cross attacks
	for i in range(8):
		for j in range(8):
			if ( i != j & j>i): #& j>i
				pos = abs(i-j)
				val = abs(seq[i] - seq[j])
				if(pos == val):
					totalAttacks += 1

	return 28 - totalAttacks


def generatePopulation(population_size):
	population = [QueenSequence() for i in range(population_size)]
	for i in range(population_size):
		base_seq = np.arange(8)
		np.random.shuffle(base_seq)
		population[i].setSequence(base_seq)
		population[i].setFitness(getFitness(population[i].sequence))
	return population

def selectParents(population):
	population_fitness = 0
	for seq in population:
		population_fitness += seq.fitness

	for seq in population:
		seq.probability = seq.fitness/(population_fitness*1.0)

	max_prob1 = np.max([a.probability for a in population])
	max_prob2 = np.max([a.probability for a in population if a.probability !=max_prob1])

	for seq in population:
		if seq.probability == max_prob1:
			parent1 = seq
			break

	for seq in population:
		if seq.probability == max_prob2:
			parent2 = seq
			break

	return parent1, parent2

def geneateChildWithCrossoverMutation(parent1,parent2):
	crossOverPoint = 4
	child = QueenSequence()
	child.sequence = []
	child.sequence.extend(parent1.sequence[0:crossOverPoint])
	child.sequence.extend(parent2.sequence[crossOverPoint:])
	child.setFitness(getFitness(child.sequence))

	if child.probability < MUTATION_RATE:
		c = np.random.randint(8)
		child.sequence[c] = np.random.randint(8)

	return child

def main(max_iteration,mutation_rate,population):
	MUTATION_RATE = mutation_rate
	MAX_ITERATION = max_iteration
	population = generatePopulation(population)
	"""
	for p in population:
    	print('sequence: ',p.sequence, 'fitness:',p.fitness, 'probability:',p.probability)
	"""
	max_iteration = MAX_ITERATION
	generation = 1
	stop_flag = False

	for chr in population:
		if chr.fitness==28:
			print("Correct Sequence: ", chr.sequence)
			stop_flag = True
			break

	while max_iteration > 0 | stop_flag == False:
		parent1,parent2 = selectParents(population)
		child  = geneateChildWithCrossoverMutation(parent1,parent2)
		max_fitness = np.max([x.fitness for x in population])

		print("Gen :",generation," | Fitness: ", child.fitness," | Max Fitness: ",max_fitness, " | sequence: ", child.sequence)

		for chr in population:
			if chr.fitness==28:
				print("Correct Sequence: ", chr.sequence)
				stop_flag = True

			if stop_flag == True:
				break

		generation+=1
		max_iteration-=1

main(10000,0.000001,1000)
