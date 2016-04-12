import sys
import mpi4py
import maxInterest
import minimumPay
import unitProportionalPay
import directProportionalPay


def call(vars):
	minimumPay.payLoans(vars);
	maxInterest.payLoans(vars);
	unitProportionalPay.payLoans(vars);
	directProportionalPay.payLoans(vars);

if __name__ == '__main__':
	call(sys.argv);