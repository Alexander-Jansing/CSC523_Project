import sys

##This program will pay off debts by minimum payments only
def payLoans(file):
	payOffs = getPayOffs(file[2]);
	finances = readFile(file[1]);
	totalDebt = sumDebt(finances);
	totalPaid = 0;
	##printThings(finances);
	for i in range(len(payOffs)):
		if len(finances) == 0:
			break;
		loopTotal = 0;
		minPayment = minimumPayments(finances);
		finances = monthlyMinPay(finances, minPayment);
		for payment in minPayment:
			totalPaid += sum(payment);
	print "It costs you $", totalPaid, "to pay off $", totalDebt, " in loans by only paying minimum payments.";

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