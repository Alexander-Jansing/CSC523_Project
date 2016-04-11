import sys 
import maxInterest
import minimumPay


def call(vars):
	maxInterest.payLoans(vars)
	minimumPay.payLoans(vars)

if __name__ == '__main__':
	call(sys.argv);