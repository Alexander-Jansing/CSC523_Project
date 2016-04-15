import sys
import mpi4py as MPI
import maxInterest
import minimumPay
import unitProportionalPay
import directProportionalPay


def call(vars):
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()

	if rank == 0:
		minimumPay.payLoans(vars);
	if rank == 1:
		maxInterest.payLoans(vars);
	if rank == 2:
		unitProportionalPay.payLoans(vars);
	if rank == 3:
		directProportionalPay.payLoans(vars);
	MPI.Finalize();


if __name__ == '__main__':
	call(sys.argv);