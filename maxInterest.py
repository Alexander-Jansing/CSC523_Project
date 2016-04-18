import sys
import numpy as np;

##This program will use the rule of thumb to pay off the highest interest (followed by LOWEST balance) loans off first
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
	maxInterest = findMaxInterest(finances);
	if extraPayoff > maxInterest['balance']:
		extraPayoff -= maxInterest['balance'];
		totalPaid += maxInterest['balance']
		finances = deleteMax(maxInterest, finances);
		payoffMax(finances, extraPayoff, totalPaid);
	else:
		maxInterest['balance'] -= extraPayoff;
		totalPaid += extraPayoff;
		finances = updateFinances(maxInterest, finances);
	return totalPaid;

def monthlyMinPay(finances, minPayment):
	for i in range(len(finances)):
		finances[i]['balance'] -= minPayment[i][1];
	return finances;

def minimumPayments(finances):
	minPayment = [];
	for i in range(len(finances)):
		minPayment.append([finances[i]['rate']*finances[i]['balance'], finances[i]['balance']*.03]);
	return minPayment;

def updateFinances(maxInterest, finances):
	for i in range(len(finances)):
		if finances[i]['id'] == maxInterest['id']:
			finances[i] = maxInterest;
	return finances;

def sumDebt(finances):
	totalDebt = 0
	for json in finances:
		totalDebt += json['balance'];
	return totalDebt;

def printCongrats(maxInterest):
	print "Congrats! You paid off ", maxInterest, "!"

def deleteMax(maxInterest, finances):
	for i in range(len(finances)):
		if finances[i]['id'] == maxInterest['id']:
			del finances[i];
			break;
	return finances

def findMaxInterest(finances):
	rates = collectRates(finances);
	maxRate = max(rates);
	debtOfInterest = findMaxBalance(maxRate, finances);
	return debtOfInterest;

def findMaxBalance(maxRate, finances):
	j = {
		'id':9999,
		'balance':float(0),
		'rate':float(0)
	};
	for json in finances:
		if json['rate'] >= maxRate and j['balance'] < json['balance']:
			j = json;
	return j;

def collectRates(finances):
	rate = [];
	for debt in finances:
		rate.append(debt['rate']);
	return rate;

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