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
		if rank == 1:  #PAY THE HIGHEST LONE OFF FIRST
			sum = 0
			interests = []
			for i in range(len(finances)):
				sum += finances[i][0]  #i.e finances == [[10000, .01][900, .15]] results in sum == 10900
				interests.append([finances[i][1], i])
			interestsSorted = sortInterests(interests)
			while(sum != 0):
				for i in range(len(finances)):
					sum -= minimumPayment(finances)


def sortInterests(interests):
	if 
	return 0;
def minimumPayment(finances):
	return finances[0]*finances[1]+finances[0]*.01;

	MPI.Finalize();

##### QUICKSORT FROM http://interactivepython.org/runestone/static/pythonds/SortSearch/TheQuickSort.html ###
def quickSort(alist):
   quickSortHelper(alist,0,len(alist)-1)

def quickSortHelper(alist,first,last):
   if first<last:

       splitpoint = partition(alist,first,last)

       quickSortHelper(alist,first,splitpoint-1)
       quickSortHelper(alist,splitpoint+1,last)


def partition(alist,first,last):
   pivotvalue = alist[first]

   leftmark = first+1
   rightmark = last

   done = False
   while not done:

       while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
           leftmark = leftmark + 1

       while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
           rightmark = rightmark -1

       if rightmark < leftmark:
           done = True
       else:
           temp = alist[leftmark]
           alist[leftmark] = alist[rightmark]
           alist[rightmark] = temp

   temp = alist[first]
   alist[first] = alist[rightmark]
   alist[rightmark] = temp


   return rightmark
### QUICKSORT FROM http://interactivepython.org/runestone/static/pythonds/SortSearch/TheQuickSort.html ###



if __name__ == '__main__':
	runMe(sys.argv)
