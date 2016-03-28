from mpi4py import MPI
import sys

def runMe(fileAndExtraMoney): #fileAndExtraMoney is an array holding a file and the extra amount you with to apply to your loans
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	finances = []
	extra = fileAndExtraMoney[1]
	if rank == 0:
		with open(fileAndExtraMoney[0]) as f:
			for line in f:
				finances.append(line)
		comm.send(finances, dest=1)
		comm.send(finances, dest=2)
		
		###PAY THE HIGHEST LONE OFF FIRST###
		if rank == 1:
			comm.recv(source=0)
			sum = 0
			interests = []
			for i in range(len(finances)):
				sum += finances[i][0]  #i.e finances == [[10000, .01][900, .15]] results in sum == 10900
				interests.append([finances[i][1], i])
			interestsSorted = sortInterests(interests)
			while(sum != 0):
				for i in range(len(finances)):
					sum -= minimumPayment(finances)
		
		###PAY LOANS PROPORTIONALLY###
		if rank == 2:
			comm.recv(source=0)
			sum = 0
			while(sum != 0):
				for i in range(len(finances)):
					sum -= minimumPayment(finances)



def sortInterests(interests):
	sortedInterests = []
	while(len(interests) != 0):
		pointOfInterest = interests[0]
		if len(interests) > 1:
			for i in range(1, len(interests)):
				if pointOfInterest > interests[i]:
					pointOfInterest = interests[i]
		interests.remove(pointOfInterest)
		sortInterests.append(pointOfInterest)
	return sortedInterests;

	return 0;
def minimumPayment(finances):
	return finances[0]*finances[1]+finances[0]*.01;

	MPI.Finalize();





if __name__ == '__main__':
	runMe(sys.argv)
