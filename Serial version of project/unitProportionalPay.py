import sys;
import numpy as np;
import math;

##This program will pay off debts by proportions
def payLoans(file):
	extra = float(file[2]);
	finances = readFile(file[1]);
	totalDebt = sumDebt(finances);
	TOTAL = totalDebt;  # ONLY USE FOR FIND PROMPT
	totalPaid = 0;
	months = 0;
	while(totalDebt > .01):
		loopTotal = 0;
		if len(finances) == 0:
			break;
		minPayment = minimumPayments(finances);
		finances = monthlyMinPay(finances, minPayment);
		for payment in minPayment:
			loopTotal += sum(payment);
		loopTotal = payoffProportionally(finances, extra, loopTotal);
		totalPaid += loopTotal;
		months += 1;
		#print totalDebt
		totalDebt -= loopTotal;
	print("It cost you $", np.ceil(totalPaid), "to pay off $", np.ceil(TOTAL), "in loans over", months, "months");

def getPayOffs(file):
	po = [];
	with open(file) as numbers:
		for num in numbers:
			for n in num.split(','):
				po.append(float(n));
	return po;

def payoffProportionally(finances, extraPayoff, totalPaid):
	if len(finances) == 0:
			return totalPaid;
	else:
		token = reduceBalances(finances, extraPayoff);
		finances = token[0];
		totalPaid += token[1];  # THIS FORMAT IT USED, BUT IN CASE THE LAST PAYOFF AMOUNT IS
								## IS LESS THAN THE AMOUNT OWED -- THIS WAY WE ARE MORE ACCURATE
	return totalPaid;

def findSum(finances, token):
	SUM = 0;
	for debt in finances:
		SUM += debt[token];
	return SUM;

def reduceBalances(finances, extraPayoff):
	paid = 0; 
	for i in range(len(finances)):
		if(len(finances) == 1):
			if finances[0]['balance'] < extraPayoff:
				hold = finances[0]['balance'];
				finances[0]['balance'] = 0;
				return [finances, hold];
			else:
				finances[0]['balance'] -= extraPayoff;
				return [finances, extraPayoff];
		sumInterests = findSum(finances, 'rate');   # IT LOOKS SLOPPY TO RECALCULATE THIS EVERY TIME,
		sumBalances = findSum(finances, 'balance'); ## BUT WHEN DEBT IS PAID OFF, WE NEED IT TO BE
													### REMOVED AND HAVE THE PROPORTIONS DISTRIBUTED
		props = proportions(finances, sumInterests, sumBalances, extraPayoff)
		#print normalizer
		propToThisDebt = proportionedPayment(props[i], extraPayoff);
		# print propToThisDebt, " PROPORTION OF ", extraPayoff
		if finances[i]['balance'] < propToThisDebt:
			extraPayoff -= finances[i]['balance'];
			paid += finances[i]['balance'];
			del finances[i];
			del props[i];
			reduceBalances(finances, extraPayoff);
			break;
		else:
			finances[i]['balance'] -= propToThisDebt;
			paid += propToThisDebt;
	return [finances, paid];


def proportions(finances, rateSum, balSum, extraPayoff):
	b = 0;
	r = 0;
	A = []
	for i in range(len(finances)):
		b += finances[i]['balance']/balSum;
		r += finances[i]['rate']/rateSum;
		A.append(b*r);	
	for i in range(1,len(A)):
		A[i] -= sum(A[:i]);
	inv = (b*r);
	#print A;
	return A;

def proportionedPayment(prop, extraPayoff):
	#print prop * extraPayoff;
	return prop * extraPayoff;
			
def monthlyMinPay(finances, minPayment):
	for i in range(len(finances)):
		finances[i]['balance'] -= minPayment[i][1]; # ONLY PAYING OFF THE 3% OF BALANCE
	return finances;

def minimumPayments(finances):
	minPayment = [];
	for i in range(len(finances)):
		minPayment.append([finances[i]['rate']*finances[i]['balance'], finances[i]['balance']*.03]);
	return minPayment;

def sumDebt(finances):
	totalDebt = 0
	for json in finances:
		totalDebt += json['balance'];
	return totalDebt;

def printCongrats(maxInterest):
	print("Congrats! You paid off ", maxInterest, "!");

def printThings(tokenList):
	for token in tokenList:
		print(token);

def readFile(file):
	finances = [];
	i = 0;
	with open(file) as f:
		for line in f:
			parts = line.split(',')
			data = {
				'id':i,
				'balance':float(parts[0]),
				'rate':float(parts[1].strip())
			};
			i += 1;
			finances.append(data);
	return finances;

if __name__ == '__main__':
	payLoans(sys.argv);