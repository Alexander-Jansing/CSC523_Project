import sys;
import numpy as np;

##This program will pay off debts by proportions
def payLoans(file):
	extra = float(file[2]);
	finances = readFile(file[1]);
	totalDebt = sumDebt(finances);
	totalPaid = 0;
	months = 0;
	while(not (len(finances) == 1 and finances[0]['balance'] < 1)):
		if len(finances) == 0:
			break;
		loopTotal = 0;
		minPayment = minimumPayments(finances);
		finances = monthlyMinPay(finances, minPayment);
		for payment in minPayment:
			totalPaid += sum(payment);
		totalPaid += payoffMax(finances, extra, loopTotal);
		months += 1;
	print "It cost you $", np.ceil(totalPaid), "to pay off $", np.ceil(totalDebt), "in loans over", months, "months";

def getPayOffs(file):
	po = [];
	with open(file) as numbers:
		for num in numbers:
			for n in num.split(','):
				po.append(float(n));
	return po;

def payoffMax(finances, extraPayoff, totalPaid):
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
			return [finances, 0];
		sumInterests = findSum(finances, 'rate');   # IT LOOKS SLOPPY TO RECALCULATE THIS EVERY TIME,
		sumBalances = findSum(finances, 'balance'); ## BUT WHEN DEBT IS PAID OFF, WE NEED IT TO BE
													### REMOVED AND HAVE THE PROPORTIONS DISTRIBUTED
		propToThisDebt = proportionedPayment(finances[i], sumInterests, sumBalances, extraPayoff);
		if finances[i]['balance'] < propToThisDebt:
			extraPayoff -= finances[i]['balance'];
			paid += finances[i]['balance'];
			del finances[i];
			reduceBalances(finances, extraPayoff);
			break;
		else:
			finances[i]['balance'] -= propToThisDebt;
			paid += propToThisDebt;
	return [finances, paid];

def proportionedPayment(debt, rateSum, balSum, extraPayoff):
	return debt['rate']/rateSum * extraPayoff;
			
def monthlyMinPay(finances, minPayment):
	for i in range(len(finances)):
		finances[i]['balance'] -= minPayment[i][1];
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
	print "Congrats! You paid off ", maxInterest, "!"

def printThings(tokenList):
	for token in tokenList:
		print token;

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