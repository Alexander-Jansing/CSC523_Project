from mpi4py import MPI;
import sys;

def runMe(fileAndExtraMoney):                                                               #fileAndExtraMoney IS A LIST WITH A FILENAME AND THE
                                                                                            ## EXTRA AMOUNT YOU WISH TO APPLY TO YOUR loans
	comm = MPI.COMM_WORLD;
	rank = comm.Get_rank();
	print rank
	finances = [];
	extra = fileAndExtraMoney[1];
	if rank == 0:
		with open(fileAndExtraMoney[0]) as f:
			for line in f:
				finances.append(line.split(","));
		comm.send([finances, fileAndExtraMoney[1]], dest=1);                                # [ [ [debt, interest], ... ], extraTowardLoans]
		comm.send([finances, fileAndExtraMoney[1]], dest=2);                                # [ [ [debt, interest], ... ], extraTowardLoans]

		###PAY THE HIGHEST LONE OFF FIRST###
		if rank == 1:
			totalPaid1 = 0
			localFinances1 = comm.recv(source=0);
			sum = 0;
			interests = [];
			for i in range(len(localFinances1[0])):
				sum += localFinances1[0][i][0];                                             #i.e. localFinances1 == [[10000, .01][900, .15]] RESULTS
				                                                                            ## IN sum == 10900
				interests.append([localFinances1[0][i][1], i]);
			interestsSorted = sortInterests(interests);
			while(sum != 0):                                                                # WHILE YOU'RE STILL IN DEBT
				for i in range(len(localFinances1[0])):
					totalPaid1 += localFinances1[0][i][0]*localFinances1[0][i][1];          # THIS IS ADDED HERE, BECAUSE IT IS NOT COMPUTED IN
					                                                                        ## minimumPaymentReduction METHOD... THIS IS THE INTEREST
					                                                                        ### ACCRUED IN A MONTH
					minPay = minimumPaymentReduction(localFinances1[0][i]);                 # AMOUNT YOU PAY OFF WITH THE 1% PRINCIPAL PAYOFF PLAN
					totalPaid1 += minPay;                                                   # ADDING AMOUNT YOU PAY OFF WITH THE 1% PRINCIPAL PAYOFF
					                                                                        ## PLAN TO YOUR TOTAL COST
					localFinances1[0][i][0] -= minPay;                                      # REDUCE SPECIFIC LOAN BY MINIMUM PAYOFF
					sum -= minPay;                                                          # REDUCE TOTAL DEBT BY MINIMUM PAYOFF
				highestInterestIndex = interestsSorted[len(interestsSorted)-1][1];     		# [ [.01, 2], [.06, 0], [.15, 1] ] NEED TO RETURN "1"... 
				                                                                            ## SO list[len()-1][1]
				localFinances1[0][highestInterestIndex][0] -= localFinances1[1];     		# HIGHEST INTEREST LOAN AMOUNT MINUS EXTRA
				sum -= localFinances1[1];                                                   # TOTAL DEBT MINUS EXTRA
				totalPaid1 += localFinances1[1];                                            # ADDING THE EXTRA YOU PAY TOWARD THE TOTAL
			print "Via the plan of just paying off highest interest loans first, you pay ", totalPaid1;
		
		###PAY LOANS PROPORTIONALLY AFTER BEATING OUT THE NEXT MONTH'S INTEREST (conditional on the extra you want to pay toward your loans)###
		if rank == 2:
			localFinances2 = comm.recv(source=0);
			sum = 0;
			for i in range(len(localFinances1[0])):
				sum += localFinances2[0][i][0];  #i.e localFinances1 == [[10000, .01][900, .15]] results in sum == 10900
			interestDenominator = sumOfSecondElements(localFinances2[0]); # from example above, interestDenominator == .16
			while(sum != 0):
				for i in range(len(localFinances2[0])):
					sum -= minimumPaymentReduction(localFinances2[0]);
				#if()


	MPI.Finalize();



## USED FOR SUMMING THE SECOND ELEMENTS OF A LIST.
### FIRST USE FOR ADDING UP THE INTEREST RATES OF ALL LOANS SUPPIED.
def sumOfSecondElements(finances):
	sum = 0;
	for loan in finances:
		sum += loan[1];
	return sum;

## SORTS 2D LIST BASED ON THE FIRST ELEMENTS.
### SECOND ELEMENTS REFER TO THE INDEX OF THEIR ORIGIN IN THE finance LIST
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
def minimumPaymentReduction(finances):
	return finances[0]*.01;  ## NOTE YOUR MINIMUM PAYMENT WOULD ACTUALLY BY finances[0]*finances[1]+finances[0]*.01 ... INTEREST+ ( 1% OF PRINCIPAL )






if __name__ == '__main__':
	runMe(sys.argv);
