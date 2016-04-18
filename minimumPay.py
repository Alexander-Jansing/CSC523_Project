import sys
import numpy as np;

##This program will pay off debts by minimum payments only
### WE NEED TO PUT A CHECK INTO PLACE TO SEE IF A DEBT IS PAID OFF
#### IT IS OBVIOUS THAT THIS MEATHOD IS THE WORST, BUT WE SHOULD
##### HAVE ACCURATE FINAL PAYOFF AMOUNTS REPORTED.
def payLoans(file):
	finances = readFile(file[1]);
	totalDebt = sumDebt(finances);
	totalPaid = 0;
	##printThings(finances);
	months = 0;
	while(not (len(finances) == 1 and finances[0]['balance'] < 1)):
		if len(finances) == 0:
			break;
		loopTotal = 0;
		minPayment = minimumPayments(finances);
		finances = monthlyMinPay(finances, minPayment);
		for payment in minPayment:
			totalPaid += sum(payment);
		months += 1;
	print "It cost you $", np.ceil(totalPaid), "to pay off $", np.ceil(totalDebt), "in loans over", months, "months";

def getPayOffs(file):
	po = [];
	with open(file) as numbers:
		for num in numbers:
			for n in num.split(','):
				po.append(float(n));
	return po;

def monthlyMinPay(finances, minPayment):
	for i in range(len(finances)):
		finances[i]['balance'] -= minPayment[i][1];
		if finances[i]['balance'] < 1:  # just assume that you can pony up an extra dollar
			del finances[i]
			monthlyMinPay(finances, minPayment);
			break;
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