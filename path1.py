import sys

##Path1 will use the rule of thumb to pay off the highest interest (followed by LOWEST balance) loans off first
def payLoans(file):
	payOffs = getPayOffs(file[2]);
	finances = readFile(file[1]);
	totalDebt = sumDebt(finances);
	totalPaid = 0;
	printThings(finances);
	for i in range(len(payOffs)):
		if len(finances) == 0:
			break;
		loopTotal = 0;
		minPayment = minimumPayments(finances);
		finances = monthlyMinPay(finances, minPayment);
		totalPaid += sum(minPayment);
		del minPayment;
		## print totalPaid, minPayment, sum(minPayment)
		totalPaid += payoffMax(finances, payOffs[i], loopTotal);
	print totalPaid, totalDebt;
	print "Congrats you paid off all your loans!";
	print "It cost you $", totalPaid, "to pay off $", totalDebt, " in loans.";

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
		## print "TEST LINE ", totalPaid
		finances = deleteMax(maxInterest, finances);
		printCongrats(maxInterest);
		payoffMax(finances, extraPayoff, totalPaid);
	else:
		maxInterest['balance'] -= extraPayoff;
		totalPaid += extraPayoff;
		finances = updateFinances(maxInterest, finances);
	return totalPaid;

def monthlyMinPay(finances, minPayment):
	for i in range(len(finances)):
		finances[i]['balance'] -= (minPayment[i] - finances[i]['rate']*finances[i]['balance']);
	return finances;

def minimumPayments(finances):
	minPayment = [];
	for i in range(len(finances)):
		minPayment.append(finances[i]['rate']*finances[i]['balance'] + finances[i]['balance']*.01);
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
			## print "Deleting ", finances[i];
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