#!/usr/bin/python
""" Chieh Lee Aug 2017 """


import csv, re, sys, os


class AllPossCombinatoin:

	def __init__(self, f):
		self.f = open(f, 'rb')
		""" File object of csv file, read only, open in binary mode"""
		
		self.csvreader = csv.reader(self.f, delimiter=',')
		""" csvreader object, delimiter = ',' """
		
		self.fl = list(self.csvreader)
		""" csv file in list """
		
		self.priceformat = r'\$\d+(\.\d{2})?$'
		""" Price string regex pattern """
		
		self.target_price = self.make_target_price()
		""" Price string regex pattern """		
		
		self.items = self.make_items()
		""" Price string regex pattern """
		
	output = []

	def make_target_price(self):
		"""
		Extract 'Target Price' from given csv file, return the first element
		of the processed csv list varaible if the key string is "Target Price" and
		the price element match self.priceformat

		Parameters
		----------
		arg1 : self

		Returns
		-------
		List
			len = 2, the first element of the processed csv list
		"""
		if len(self.fl[0]) != 2:
			print 'extra unknown variable in the entry, format: \'Target price, $xx.xx\''
			exit(1)
		elif not re.search(self.priceformat, self.fl[0][1]):
			print self.fl[0][1], 'does not match the price format %s' % '$xxx.xx or $xxx'
			exit(1)
		return self.fl[0]

	def make_items(self):
		"""
		Extract other items from given csv file, return the list of the processed 
		csv list varaible if price element match self.priceformat

		Parameters
		----------
		arg1 : self

		Returns
		-------
		List 
			List of List(len=2)
			the rest element of the processed csv list match the pattern
		"""
		items = []
		bad_entry = False
		for item in self.fl[1:]:
			if len(item) == 2:
				if not re.search(self.priceformat, item[1]):
					print item, 'does not match the price format %s' % '$xxx.xx'
					exit(1)
				else:
					items.append(item)
			elif len(item) != 2 and len(item) != 0:
				print 'Bad Entry: ', item
				bad_entry = True
		if bad_entry:
			exit(1)
		else:
			return items


	def extract_int(self, item):
		"""
		given list (len=2) of item, price extract the integer

		Example:
		----------
		['item name', '$9.99'] -> 999

		Parameters
		----------
		arg1 : self
		arg2 : List
			List len=2, second element match pattern of self.priceformat

		Returns
		-------
		int
		"""
		p = re.findall(r'\d+', item[1])
		if len(p) == 1:
			return int(p[0]+'00')
		else:
			return int(p[0]+p[1]) #take away $ sign

	def convert_to_money(self, i):
		"""
		given list (len=2) of item, price extract the integer

		Example:
		----------
		999 -> ['item name', '$9.99']

		Parameters
		----------
		arg1 : self
		arg2 : List
			List len=2, second element match pattern of self.priceformat

		Returns
		-------
		int
		"""
		istr = str(i)
		return '$' + istr[:-2] + '.' + istr[-2:]


	def countf_helper(self, tp, items, c, sindex):
		"""
		helper function for countf

		Parameters
		----------
		arg1 : self
		arg2 : int
			target price			
		arg3 : ListOfInt
			List of item price (int)
		arg4 : ListOfInt
			each element represent occurance of each item price
		arg5 : int
			start index for current resursion
		"""
		if sindex >= len(items):
			return
		count = tp / items[sindex]
		for i in reversed([x+1 for x in range(count)]):
			cc = list(c) # initiate output count for each loop
			ttp = tp - (items[sindex]*i) # calculate total price for each pool
			cc[sindex] = i
			if ttp == 0:
				self.output.append(list(cc))
			else:
				for j in range(sindex+1, len(items)):
					self.countf_helper(ttp, items, cc, j)

	def countf(self, tp, items, c, sindex):
		"""
		Call resursion of outter scope and inner scope to calculate all possible
		combination that sums match the target price

		Parameters
		----------
		arg1 : self
		arg2 : int
			target price			
		arg3 : ListOfInt
			List of item price (int)
		arg4 : ListOfInt
			each element represent occurance of each item price
		arg5 : int
			start index for current resursion

		Example
		-------
		item = [1,2,3]
		result = self.output = [[2,1,0], [1,0,1]] which means:
		(1 * 2) + (2 * 1) = target price  and
		(1 * 1) + (3 * 1) = target price

		Returns
		-------
		void
			result will be a mutation in class variable, self.output. self.output 
			is LisfOfLIst, elements of outer List are ListOfInt, represents the 
			matching combination. Element of inner list are Int, represent the 
			occurance of each item.
		"""
		if sindex >= len(items):
			return
		self.countf_helper(tp, items, c, sindex)
		self.countf(tp, items, [0]*len(items), sindex+1)

	def print_all_combination(self):
		"""
		print all combination in console

		Parameters
		----------
		arg1 : self

		Returns
		-------
		void
			print all combination in console, format:
			Combination x:
			----------------------------------------
			y-name * x-y-counts  : y-price
			...
			...
			----------------------------------------
		"""
		tp = self.extract_int(self.target_price)
		ip = [self.extract_int(x) for x in self.items]
		self.countf(tp, ip, [0]*len(ip), 0)
		if not self.output:
			print 'No combination of dishes that is equal to the target price'
		else:
			i = 1
			print
			for x in self.output:
				print 'Combination %s:' % i
				i += 1
				print '----------------------------------------'
				for y in range(len(self.items)):
					if x[y] != 0:
						print self.items[y][0], '*', x[y], ' : ', \
							self.convert_to_money(self.extract_int(self.items[y])*x[y])
				print '----------------------------------------'
				print 


if __name__ == "__main__":
	if len(sys.argv) == 1:
		print "Please insert file path as: ./c.py path.csv"
		exit(1)
	elif not os.path.exists(sys.argv[1]):
		print "File path invalid: ", sys.argv[1]
		exit(1)
	elif len(sys.argv) > 2:
		print "Input arguments invalid: ./c.py path.csv"
	else:
		path = sys.argv[1]
		c = AllPossCombinatoin(path)
		c.print_all_combination()

