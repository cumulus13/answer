#!/usr/bin/env python3

from __future__ import print_function
import os
import sys
import subprocess
#from pydebugger.debug import debug
from make_colors import make_colors
import re
try:
	from pause import pause
except:
	def pause():
		return input("enter to continue")

def show(windows):
	#print("windows =", windows)
	data = []
	wlist = os.popen("wmctrl -l").readlines()
	#debug(wlist = wlist)
	for i in wlist:
		data_found = []
		n = 1
		i = i.split("\n")[0]
		#debug(i = i)
		pattern = re.compile(r'(?P<w_id>.*).*(?P<d_id>\d+) (?P<c_id>.*?) (?P<title>.*)')
		#debug(pattern = pattern)
		w_id, d_id, c_id, title = pattern.match(i).groups()
		#debug(w_id = w_id)
		#debug(d_id = d_id)
		#debug(c_id = c_id)
		#debug(title = title)
		
		add = {'w_id':w_id, 'd_id':d_id, 'c_id':c_id, 'title': title}
		data.append(add)
		#debug(data = data)
		#debug(windows = windows)
		if isinstance(windows, list):
			for p in windows:
				# #debug(windows = windows)
				#debug(p = p)
				check = re.findall(p, title, re.I)
				#debug(check = check)
				if len(check) > 0:
					if check[0].strip().lower() in p.lower():
						data_found.append(n)
						n += 1
		
		elif isinstance(windows, str):
			windows = [windows]
			for p in windows:
				if re.findall(p, title, re.I):
					data_found.append(n)
					n += 1

		#debug(data_found = data_found)
		
		if len(list(set(data_found))) == len(windows):
			cmd = 'wmctrl -a "{}"'.format(title)
			# p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
			os.system(cmd)

		if os.getenv('DEBUG'):
			print("-"*130)

def usage():
	usage = """show.py [-h] [-l] [TITLES ...]

positional arguments:
  TITLES      containt titles show to

 optional arguments:
  -h, --help  show this help message and exit
  -l, --list  list all of active windows\n"""

	import argparse
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, usage = usage)
	# parser.add_argument('TITLES', action = 'store', help = "containt titles show to", nargs = '*')
	parser.add_argument('-l', '--list', action = 'store_true', help = "list all of active windows")
	if len(sys.argv) == 1:
		parser.print_usage()
		print("\n")
		os.system("wmctrl -l")
	else:
		if not '-l' in sys.argv[1:] or not '--list' in sys.argv[1:]:
			parser.add_argument('TITLES', action = 'store', help = "containt titles show to", nargs = '*')
		args = parser.parse_args()
		if args.list:
			os.system("wmctrl -l")
		if args.TITLES:
			show(args.TITLES)



if __name__ == '__main__':
	# show(["animesail", 'sublime'])
	usage()