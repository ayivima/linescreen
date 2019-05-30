"""

If your script has more than a set number of lines,
your code lines are leaking :)

screen counts the lines of code, and 'yells' if the 
limit is exceeded. The 'yelling' behaviour can be silenced
The default limit of 500 can be overridden.
Finally, limits can be applied to physical or logical lines.

USAGE: lineleak.py [-h] [-l LIMIT] [-s] [-p] filename

positional arguments:
  filename              The name of the file to lint.

optional arguments:
  -h, --help            show this help message and exit
  -l, --limit			Sets the line limit.
  -s, --stopyell        Overrides limit enforcement, and 
						returns just the number of lines 
						in the script.
  -p, --physical        Enforces limit on physical lines 
						instead of logical lines. It is 
						only useful if limit is enforced


(c) Copyright 2019 

"""

__version__ = '0.9.7'

import re
import sys
import logging
import argparse
from tokenize import generate_tokens, open
from token import NEWLINE, STRING, OP, NAME, NL, COMMENT, ENDMARKER 


ENFORCE_LIMIT = 'enforce'
IGNORE_LIMIT = 'ignore'
LOGICAL_MODE = 'logical'
PHYSICAL_MODE = 'physical'
LIMIT_REACHED = 'reached'
LIMIT_NOT_REACHED = 'not reached'

#WARNINGS & MESSAGES
LLY404 = ("\n\t| {}-LINE {} LIMIT EXCEEDED!\n"
		 "\t| {} has {} {} lines.\n"
		 "\t| Limit was exceeded at line [{}].\n")
		 
LLY405 = "\n\t| {} has no live code.\n"
		 
LLI200 = "\n\t{} has: \n\t{} {} lines \n\t{} {} lines.\n"

LLI201 = "NUMBER OF LINES WITHIN LIMIT."


class screen:

	def __init__(self, filename=None,
				 mode=LOGICAL_MODE, limit=500,
				 limit_behaviour=ENFORCE_LIMIT,
				 count_lines=False):
		
		self.filename = filename
		self.mode = mode.lower()
		self.limit = limit
		self.limit_behaviour = limit_behaviour
		self.limit_status = LIMIT_NOT_REACHED
		self.leak_line = None
		self.logical_line_count = None
		self.physical_line_count = None
		self.tokens = []
		
		try:
			# overriding default IO open with tokenize.open()
			# for automatic encoding detection
			with open(filename) as f:
				for token in generate_tokens(f.readline):
					self.tokens.append(token)
		except FileNotFoundError:
			#...enter code here
			pass
			
		# COUNT THE LINES
		self._counter()
		
		# CHECK FOR LIMIT, AND YELL IF LIMIT PASSED
		line_count = self.logical_line_count if \
					 self.mode==LOGICAL_MODE else self.physical_line_count
				
		if limit_behaviour==ENFORCE_LIMIT:
			self._yell()
		else:
			self._show_count()
				
					
	def _counter(self):
		"""
		Counts the logical lines and physical lines
		of the script, and documents the first line 
		that breaks the limit for easy reference.
		
		"""
		
		# getting the last line of code.
		# the last line number should be the first item 
		# of the third item(a tuple, of course) in the last token
		last_line_no = self.tokens[-1][2][0]
		
		prev_token_type = None
		prev_line_no = None
		log_line_count = 0
		
		physical_line_deductions = 0
		
		for token_type, token_value, a, b, c in self.tokens:
			
			start_line_num = a[0]
			end_line_num = b[0]
			phy_line_count = start_line_num - physical_line_deductions
			
			# making necessary adjustments for physical and logical line counts
			# when blank lines, comments, and docstrings are encountered.
			# NOTE: docstrings not considered in count.
			if token_type==NEWLINE:
				log_line_count += 1
				
			elif ((token_type==NL and start_line_num!=prev_line_no)
				or token_type==COMMENT
				or token_type==ENDMARKER):
				physical_line_deductions += 1
				
			elif (token_type==STRING
				and token_value.startswith(('"""', "'''"))
				and prev_token_type != OP):
					log_line_count -= 1
					if end_line_num==start_line_num:
						physical_line_deductions += 1
					else:
						physical_line_deductions += end_line_num - start_line_num + 1
			
			# checking for leak line while limit is not reached.
			# check stops if limit has been reached
			if self.limit_status==LIMIT_NOT_REACHED:
				if  ((log_line_count > self.limit and self.mode==LOGICAL_MODE)
					or (phy_line_count > self.limit and self.mode==PHYSICAL_MODE)
					and token_type not in (NL, COMMENT, STRING)):
						self.limit_status=LIMIT_REACHED
						self.leak_line = start_line_num
			
			prev_token_type = token_type
			prev_line_no = start_line_num
		
		
		self.physical_line_count = last_line_no - physical_line_deductions
		self.logical_line_count = log_line_count
	
	def _show_count(self):
		sys.stdout.write(LLI200.format(
							self.filename, self.physical_line_count, 
							PHYSICAL_MODE, self.logical_line_count, 
							LOGICAL_MODE
							)
						)
	
	
	def _yell(self):
		line_count = self.logical_line_count if \
					 self.mode==LOGICAL_MODE else \
					 self.physical_line_count
		
		if self.limit_status==LIMIT_REACHED:
			logging.warning(
				LLY404.format(
					self.limit, self.mode.upper(), self.filename, 
					line_count, self.mode, self.leak_line
				)
			)
		else:
			if line_count:
				sys.stdout.write(LLI201)
				self._show_count()
				
			else:
				logging.warning(LLY405.format(self.filename,))
		
	
		

def _main():
	
	parser = argparse.ArgumentParser()
	parser.add_argument("filename",  help="The name of the file to lint.")
	parser.add_argument("-l", "--limit", type=int, help="Sets the line limit.")
	
	parser.add_argument(
		"-s", "--silence", action="store_true", 
		help="Overrides limit enforcement, "
			 "and returns just the number of lines "
			 "in the script."
	)
	
	parser.add_argument(
		"-p", "--physical", action="store_true", 
		help="Enforces limit on physical "
			 "lines instead of logical lines. "
			 "It is only useful if limit is enforced"
	)
						
	args = parser.parse_args()
	
	#setting up screen 
	filename = args.filename
	limit = args.limit if args.limit else 500
	limit_behaviour = IGNORE_LIMIT if args.silence else ENFORCE_LIMIT
	mode = PHYSICAL_MODE if args.physical else LOGICAL_MODE
	
	screen(filename, mode, limit, limit_behaviour)
	

if __name__ == '__main__':
    _main()	
	
			