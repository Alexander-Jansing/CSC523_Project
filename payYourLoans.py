import sys
import mpi4py as MPI
import maxInterest
import minimumPay
import unitProportionalPay
import directProportionalPay
import time

def call(vars):
	start_time = time.time();

	minimumPay.payLoans(vars);
	maxInterest.payLoans(vars);
	directProportionalPay.payLoans(vars);
	unitProportionalPay.payLoans(vars);
	end_time = time.time();
	print "Program took", (end_time - start_time), "seconds to execute."

if __name__ == '__main__':
	call(sys.argv);