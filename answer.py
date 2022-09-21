from __future__ import print_function
import sys
import os
import inspect
from make_colors import make_colors
from getpass import getpass
if sys.version_info.major < 3:
	print(make_colors("This is only support for Python 3.7+ (>=3.7)", 'lw', 'r'))
	sys.exit()
if sys.platform == 'win32':
	print("youre are running on windows OS, this script support colored text, but sometimes on windows not supported, do you want keep on colored text support it [y/n]: ")
	if q == 'n' or not q:
		os.environ.update({'MAKE_COLORS':'0'})
import re
import time
try:
	from . import progressbar
except:
	try:
		import progressbar
	except:
		print(make_colors("install `progressbar2` module", 'ly'))
		a = os.system('pip install progressbar2')	
		if a:
			print(make_colors("it's seem error while on installing progressbar2 module !"))
		
import traceback
try:
	import requests
except:
	# print(make_colors("please install requests module before", 'ly') + " " + make_colors("(`pip install requests`)", 'lg'))
	# sys.exit()
	print(make_colors("install `requests` module", 'ly'))
	a = os.system('pip install requests')
	if a:
		print(make_colors("it's seem error while on installing requests module !"))
		q = input(make_colors("Do you want to continue, or you want to install `requests` module manually ? [y/[n|enter]]:", 'r', 'lw') + " ")
		if q == 'y':
			sys.exit()
from configset import configset
try:
	from debug import debug
except:
	try:
		from .debug import debug
	except:
		print(make_colors("install `pydebugger` module", 'ly'))
		a = os.system('pip install pydebugger')
		if a:
			print(make_colors("it's seem error while on installing pydebugger module !"))
		from pydebugger.debug import debug

import sqlite3 as sqlite
import ast
import json
import time
import argparse
try:
	from . import get_version
except:
	try:
		import get_version
	except:
		import importlib.machinery
		get_version = importlib.machinery.SourceFileLoader('get_version', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'get_version.py')).load_module()

# from multiprocessing import Process
# import concurrent.futures

class Check(object):
	def __init__(self):
		super(Check, self)

	@classmethod
	# def check(self, parens: str) -> bool:
	def check(self, parens):
		parens_map ={'(':')','{':'}','[':']'}
		stack = []
		for paren in parens:
			if paren in parens_map:  # is open
				debug(paren = paren)
				stack.append(paren)
				debug(stack = stack)
			elif paren in parens_map.values():  # is close
				debug(paren1 = paren)
				debug(stack1 = stack)
				if (not stack) or (paren != parens_map[stack.pop()]):
					return False
		return not stack

class Table(object):

	url = "https://gql.tokopedia.com/graphql/headerMainData"
	configname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'answer.ini')
	config = configset(configname)
	CONFIG = config
	update = False
	db_type = 'sqlite'
	prefix='{variables.task} >> {variables.subtask}'
	variables={'task': '--', 'subtask': '--'}

	categorie_name_list = []
	categorie_name = []
	sub_categorie_name = []
	sub_sub_categorie_name = []

	bar = progressbar.ProgressBar(widget_kwargs=dict(fill='█'), prefix = prefix, variables = variables, max_value = 100, max_error = False)

	payload = [{"operationName":"headerMainData","variables":{},"query":"query headerMainData {\n  dynamicHomeIcon {\n    categoryGroup {\n      id\n      title\n      desc\n      categoryRows {\n        id\n        name\n        url\n        imageUrl\n        type\n        categoryId\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  categoryAllListLite {\n    categories {\n      id\n      name\n      url\n      iconImageUrl\n      isCrawlable\n      children {\n        id\n        name\n        url\n        isCrawlable\n        children {\n          id\n          name\n          url\n          isCrawlable\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}]

	def __init__(self):
		super(Table, self)

	@classmethod
	def get_update(self):
		return requests.post(self.url, headers = {'content-type':'application/json'}, json = self.payload).json()

	@classmethod
	def pg_config(self):
		db_config = "dbname={} user={} password={} port={} host={}".format(
			self.CONFIG.get_config('database', 'name'),
			self.CONFIG.get_config('database', 'username'),
			self.CONFIG.get_config('database', 'password'),
			self.CONFIG.get_config('database', 'port', '5432'),
			self.CONFIG.get_config('database', 'host', '127.0.0.1'),
		)
		debug(test = re.findall("= | = ", db_config))
		if not "= " in re.findall("= | = ", db_config) and not " = " in re.findall("= | = ", db_config):
			debug(db_config = db_config)
			return db_config

	@classmethod
	def connection(self, db_type = 'sqlite'):
		db_type = db_type or self.CONFIG.get_config('database', 'type')
		errors = []
		conn = None
		def SQL(table_name, main = False):
			if main:
				if self.update:
					return 'DROP TABLE IF EXISTS {};CREATE TABLE IF NOT EXISTS {} (id int NOT NULL, name VARCHAR(200) NOT NULL, url VARCHAR(500) NOT NULL, iconImageUrl VARCHAR(500), isCrawlable INT NOT NULL, __typename VARCHAR(50) NOT NULL)'.format(table_name, table_name)
				return 'CREATE TABLE IF NOT EXISTS {} (id int NOT NULL, name VARCHAR(200) NOT NULL, url VARCHAR(500) NOT NULL, iconImageUrl VARCHAR(500), isCrawlable INT NOT NULL, __typename VARCHAR(50) NOT NULL)'.format(table_name)

			else:
				if self.update:
					return 'DROP TABLE IF EXISTS {};CREATE TABLE IF NOT EXISTS {} (id int NOT NULL, name VARCHAR(200) NOT NULL, url VARCHAR(500) NOT NULL, iconImageUrl VARCHAR(500), isCrawlable INT NOT NULL, __typename VARCHAR(50) NOT NULL, parent_id INT NOT NULL)'.format(table_name, table_name)
				return 'CREATE TABLE IF NOT EXISTS {} (id int NOT NULL, name VARCHAR(200) NOT NULL, url VARCHAR(500) NOT NULL, iconImageUrl VARCHAR(500), isCrawlable INT NOT NULL, __typename VARCHAR(50) NOT NULL, parent_id INT NOT NULL)'.format(table_name)

		if db_type == 'sqlite':
			try:
				import sqlite3 as sqlite
				conn = sqlite.connect(self.CONFIG.get_config('sqlite', 'name', 'answer.db3'))
			except Exception as e:
				print(make_colors('sqlite3 setup, but error:', 'ly'))
				print(make_colors(str(e), 'lw', 'r'))
				return False
		elif db_type == 'mysql':
			driver_status = True
			try:
				import mysql.connector
				self.CONFIG.write_config('database', 'mysql', 'driver', 'mysql.connector')
				config = {
					'user': self.CONFIG.get_config('database', 'mysql', 'username', 'test'),
					'password': self.CONFIG.get_config('database', 'mysql', 'password', 'password'),
					'host': self.CONFIG.get_config('database', 'mysql', 'host', '127.0.0.1'),
					'database': self.CONFIG.get_config('database', 'mysql', 'dbname', 'answer'),
					'raise_on_warnings': self.CONFIG.get_config('database', 'mysql', 'dbname', 'True'),
				}

				conn = mysql.connector.connect(**config)
			except ImportError:
				errors.append("No mysql-connector-python module ! (`pip install mysql-connector-python`)")
				driver_status = False
			except Exception as e:
				print(make_colors('mysql-connector-python installed but error:', 'ly'))
				print(make_colors(str(e), 'lw', 'r'))
				driver_status = False
			if not driver_status:
				try:
					import MySQLdb
					self.CONFIG.write_config('database', 'mysql', 'driver', 'MySQLdb')
					conn = MySQLdb.connect(
						self.CONFIG.get_config('database', 'mysql', 'host', '127.0.0.1'),
						self.CONFIG.get_config('database', 'mysql', 'username', 'test'),
						self.CONFIG.get_config('database', 'mysql', 'password', 'password'),
						self.CONFIG.get_config('database', 'mysql', 'dbname', 'answer'),
					)
				except ImportError:
					errors.append("No MySQL-python module ! (`pip install MySQL-python`)")
					driver_status = False
				except Exception as e:
					print(make_colors('MySQL-python installed but error:', 'ly'))
					print(make_colors(str(e), 'lw', 'r'))
					driver_status = False
			if not driver_status:
				print(make_colors("error to connect to mysql database !", 'lw', 'r') + ", " + make_colors("please make sure your connector/driver [`mysql-connector-python` or `MySQLdb`] installed.", 'ly'))
				return False

		elif db_type == 'postgresql':
			try:
				import psycopg2
				db_config = self.pg_config()
				conn = psycopg2.connect(db_config)
			except ImportError:
				errors.append("No psycopg2 module ! (`pip install psycopg2`)")
				return False
			except Exception as e:
				print(make_colors('psycopg2 installed but error:', 'ly'))
				print(make_colors(str(e), 'lw', 'r'))
				return False

		print(make_colors("youre using database:", 'lg') + " " + make_colors(db_type, 'b', 'lc'))
		cursor = conn.cursor()
		self.bar.max_value = 4

		# print(make_colors("create table", 'lg') + " " + make_colors("`categories` ...", 'lc'))
		task = make_colors("create table", 'lg')
		subtask = make_colors("categories", 'lc') + " "
		self.bar.update(1, task = task, subtask = subtask)
		query = SQL('categories', True)
		debug(query = query)
		if db_type == 'sqlite':
			for i in query.split(";"):
				cursor.execute(i)
		else:
			cursor.execute(query)
		# print(make_colors("create table", 'lg') + " " + make_colors("`sub_categories` ...", 'lc'))
		task = make_colors("create table", 'lg')
		subtask = make_colors("sub_categories", 'lc') + " "
		self.bar.update(2, task = task, subtask = subtask)
		query = SQL('sub_categories')
		if db_type == 'sqlite':
			for i in query.split(";"):
				cursor.execute(i)
		else:
			cursor.execute(query)
		# print(make_colors("create table", 'lg') + " " + make_colors("`sub_sub_categories` ...", 'lc'))
		task = make_colors("create table", 'lg')
		subtask = make_colors("sub_sub_categories", 'lc') + " "
		self.bar.update(3, task = task, subtask = subtask)
		query = SQL('sub_sub_categories')
		if db_type == 'sqlite':
			for i in query.split(";"):
				cursor.execute(i)
		else:
			cursor.execute(query)
		# print(make_colors("create table", 'lg') + " " + make_colors("`sub_sub_sub_categories` ...", 'lc'))
		task = make_colors("create table", 'lg')
		subtask = make_colors("sub_sub_sub_categories", 'lc') + " "
		self.bar.update(4, task = task, subtask = subtask)
		query = SQL('sub_sub_sub_categories')
		if db_type == 'sqlite':
			for i in query.split(";"):
				cursor.execute(i)
		else:
			cursor.execute(query)
		conn.commit()

		return conn

	@classmethod
	def get_table_name(self, level):
		table_name = 'categories'
		if level > 0:
			for i in range(0, level):
				table_name = 'sub_' + table_name
		return table_name

	@classmethod
	def insert_db(self, data, conn = None, level = 0):
		'''
			data (dict) {field_name1: value_1, field_namex: valuex}
			conn (driver object)
			level (int) in 1,2,3
		'''

		def SQL(table_name, data):
			fields = list(data.keys())
			debug(fields = fields)
			
			if data.get('children') or data.get('children') == []:
				# data.pop('children')
				fields.remove('children')
				data = {i:data.get(i) for i in data if not i == 'children' }

			debug(data = data)
			data = list(data.values())

			data = ["'{}'".format(i) for i in data]
			debug(fields = fields)
			debug(data = data)
			SQL = "INSERT INTO {} ({}) VALUES ({})".format(table_name, ", ".join(fields), ", ".join(data))
			debug(SQL = SQL)
			return SQL

		conn = conn or self.connection(self.db_type)
		if not conn:
			print(make_colors("ERROR connection/driver !", 'lw', 'r'))
			return False
		cursor = conn.cursor()
		table_name = 'categories'
		if level > 0:
			for i in range(0, level):
				table_name = 'sub_' + table_name
		# print(make_colors("TABLE NAME:", 'lc') + " " + make_colors(table_name, 'ly'))
		debug(table_name = table_name)
		debug(data = data)
		cursor.execute(SQL(table_name, data))
		conn.commit()
		return conn

	@classmethod
	def get_data_from_file(self):
		data = False
		if not os.path.isfile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data.txt')):
			print(make_colors("data not found !", 'lw', 'r'))
			print(make_colors("update data ....", 'lc'))
			with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data.txt'), 'w') as datafile:
				datafile.write(str(self.get_update()))
		elif os.path.isfile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data.txt')) and len(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data.txt'), 'r').readlines()) < 10:
			with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data.txt'), 'w') as datafile:
				datafile.write(str(self.get_update()))
		
		with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data.txt'), 'r') as data:
			try:
				data = ast.literal_eval(data.read())
			except Exception as e:
				print(make_colors("Invalid DATA [1] !", 'lw', 'r'))
				print(make_colors("error [1]:", 'lw', 'r') + " " + make_colors(str(e), 'ly'))
				try:
					data = json.loads(data.read().encode('utf-8'))
				except Exception as e:
					print(make_colors("Invalid DATA [2] !", 'lw', 'r'))
					print(make_colors("error [2]:", 'lw', 'r') + " " + make_colors(str(e), 'ly'))
					return False
		return data

	@classmethod
	def navigator(self, db_type = 'sqlite', data = None):
		'''
		dbtype (str): sqlite, mysql, postgresql
		data (dict): data on dictionary or json
		'''
		self.db_type = db_type
		# data = None

		if not data:
			data = self.get_data_from_file()

		if not data:
			print(make_colors("No DATA !", 'lw', 'r'))
			return False
		data1 = data[0].get('data').get('categoryAllListLite').get('categories')
		data2 = sorted(data1, key = lambda k: k.get('id'))
		data_insert = []

		# self.update = True
		conn = self.connection(db_type)

		def insert_child(parent_id, data, level, categorie_name = ''):
			'''
				data (list) from data.get('children')
				level (int) for sub_ (prefix) table
			'''
			self.bar.max_value = len(data)
			for x in data:
				task = make_colors("insert table", 'lc')
				subtask = make_colors(self.get_table_name(level), 'ly') + " [" + make_colors(categorie_name, 'lg') + "] "
				self.bar.update(data.index(x), task = task, subtask = subtask)

				if x.get('children') or x.get('children') == []:
					data1 = {i:x.get(i) for i in x if not i == 'children' }
				else:
					data1 = x

				debug(data1 = data1)
				data1.update({'parent_id': parent_id})
				debug(level_0 = level)
				self.insert_db(data1, conn, level)

				if x.get('children'):
					# level += 1
					debug(level_1 = level)
					insert_child(x.get('id'), x.get('children'), level + 1, x.get('name'))
					# time.sleep(1)
				self.bar.max_value = len(data)

				# time.sleep(1)

		self.bar.max_value = len(data2)
		for i in data2:
			task = make_colors("insert table", 'lc')
			subtask = make_colors("categories", 'ly') + " "
			self.bar.update(data2.index(i), task = task, subtask = subtask)

			self.insert_db(i, conn, 0)
			if i.get('children'):
				# print(make_colors("INSERT CHILD", 'lw', 'r'))
				insert_child(i.get('id'), i.get('children'), 1, i.get('name'))
			self.bar.max_value = len(data2)
			# time.sleep(1)
			# print(".", end='')

	@classmethod
	def show_name_categories(self, data, n = 0):
		if not data:
			return ''
		if not data[n].get('name') in self.categorie_name_list:
			print(make_colors(str(n + 1).zfill(len(str(len(data)))) + ".") + " " + make_colors(data[n].get('name'), 'ly'))
			self.categorie_name_list.append(data[n].get('name'))
		if n == len(data) - 1:
			return False
		else:
			n += 1
			return self.show_name_categories(data, n)

	@classmethod
	def setup_db(self):
		password = ''
		db_type = input(make_colors("Database Type", 'lc') + " [" + make_colors("sqlite, mysql, postgresql | default: sqlite", 'lg') + "]: ") or 'sqlite'
		if db_type: self.CONFIG.write_config('database', 'type', db_type)
		dbname = input(make_colors("Database Name", 'ly') + ": ")
		if dbname:
			self.CONFIG.write_config('database', 'name', dbname)
			self.CONFIG.write_config('database', db_type, dbname)
		username = input(make_colors("Database Username", 'lc') + " :")
		if username: self.CONFIG.write_config('database', 'username', username)
		while 1:
			password = getpass(make_colors("Database Password", 'ly') + " " + make_colors("[password not showing]", 'lr') + " :")
			if not password:
				print(make_colors("password can't be empty ! [x/q = exit]", 'lw', 'r'))
			else:
				if password in ('q', 'x'):
					sys.exit()
				break
		if password: self.CONFIG.write_config('database', 'password', password)
		hostname = input(make_colors("Database Hostname", 'lm') + " [" + make_colors("default: 127.0.0.1", 'lg') + "]: ") or '127.0.0.1'
		if hostname: self.CONFIG.write_config('database', 'host', host)
		port = input(make_colors("Database Port", 'lm') + " [" + make_colors("default: 127.0.0.1", 'lg') + "]: ")
		if port: self.CONFIG.write_config('database', 'port', port)

	@classmethod
	def show_no_loop(self, data, n = 0, m = 0, x = 0, categorie_name = None):
		if not data:
			return ''
		if categorie_name:
			data = list(filter(lambda k: k.get('name').lower() == categorie_name.lower(), data))
		if not data[n].get('name') in self.categorie_name:
			print(make_colors(str(n + 1).zfill(len(str(len(data)))) + ".") + " " + make_colors(data[n].get('name'), 'ly'))
			self.categorie_name.append(data[n].get('name'))
			debug(m = m)
			debug(len_m1 = len(data[n].get('children')))
		
		if m < len(data[n].get('children')):
			if not data[n].get('children')[m].get('name') in self.sub_categorie_name:
				print(" " * 3 + make_colors(data[n].get('children')[m].get('name'), 'lg'))
				self.sub_categorie_name.append(data[n].get('children')[m].get('name'))

			debug(n = n, m = m, x = x, len_data_m = len(data[n].get('children')[m].get('children')))
			if x < len(data[n].get('children')[m].get('children')):
				if data[n].get('children')[m].get('children'):
					if not data[n].get('children')[m].get('children')[x].get('name') in self.sub_sub_categorie_name:
						print(" " * 6 + make_colors(data[n].get('children')[m].get('children')[x].get('name'), 'ly'))
						self.sub_sub_categorie_name.append(data[n].get('children')[m].get('children')[x].get('name'))
						
					x += 1
					return self.show_no_loop(data, n, m, x)
			else:
				x = 0
				m+=1
				return self.show_no_loop(data, n, m, x)
		else:
			if n == len(data) - 1:
				return False
			else:
				n+=1
				m=0
				x=0
				return self.show_no_loop(data, n, m, x)

def print_code(codes = None):
	try:
		from rich.console import Console
		from rich.syntax import Syntax
	except:
		try:
			print(make_colors('pip install rich ....', 'lc'))
			a = os.system('pip install rich')
			if a:
				print(make_colors("it's seem error while on installing `rich` module", 'lw', 'r') + ", " + make_colors("install `rich` module before to view code script !", 'ly'))
				return False
		except:
			print(make_colors("it's seem error while on installing `rich` module", 'lw', 'r') + ", " + make_colors("install `rich` module before to view code script !", 'ly'))
			print(make_colors("ERROR:", 'lw', 'r'))
			print(make_colors(traceback.format_exc(), 'ly'))
			return False
	if codes:
		codes = inspect.getsource(codes)
	else:
		codes = inspect.getsource(Table.show_no_loop)
	# print(codes)
	syntax = Syntax(codes, "python", theme='monokai', line_numbers = True, tab_size=2, code_width = 130)
	console = Console()
	console.print(syntax)

def print_me():
	from rich import box
	from rich.columns import Columns
	from rich.console import Console
	from rich.panel import Panel
	from rich.tree import Tree

	console = Console(record=True, width=100)

	tree = Tree("🤓 [link=https://github.com/cumulus13]Hadi Cahyadi", guide_style="bold cyan")
	python_tree = tree.add("🐍 Python expert", guide_style="green")
	python_tree.add("⭐ [link=https://github.com/willmcgugan/rich]Rich (contributor)")
	python_tree.add("⭐ [link=https://pypi.org/pydebugger]PyDebugger")
	python_tree.add("⭐ [link=https://github.com/cumulus13]etc")
	full_stack_tree = tree.add("🔧 Full-stack developer")
	full_stack_tree = tree.add("🔧 DevOps")
	full_stack_tree = tree.add("🔧 Analyst")
	full_stack_tree = tree.add("🔧 Security Specialist")
	full_stack_tree = tree.add("🔧 Network Specialist")
	full_stack_tree = tree.add("🔧 Debugger")
	full_stack_tree = tree.add("🔧 Tester")
	full_stack_tree = tree.add("🔧 Server Admin")
	tree.add("📘 Author")

	about = """\
	I'm a freelace software developer, i'm on expert on python and several language.

	[green]Contact me [bold link=mailto:cumulus13@gmail.com]mail[/]"""

	panel = Panel.fit(
	    about, box=box.DOUBLE, border_style="blue", title="[b]Hi there", width=60
	)

	console.print(Columns([tree]))

	CONSOLE_HTML_FORMAT = """\
	<pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">{code}</pre>
	"""


def usage():
	configname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'answer.ini')
	config = configset(configname)
	CONFIG = config

	description = make_colors('this script use `sqlite database for default`, if you want prefer use mysql or postgresql database you can change on config file: `answer.ini` or you can use "--setting" option', 'b', 'lc')
	parser = argparse.ArgumentParser(description = description)
	parser.add_argument('-c', '--check', help = 'Check for valid string containt bracket / valid json [interactive]', action = 'store_true')
	parser.add_argument('-C', '--checking', help = 'Check for valid string containt bracket / valid json', action = 'store')
	parser.add_argument('-s', '--show', help = 'Show json data (all) or you can use "-S" or "--show-by" to show only categorie name', action = 'store_true')
	parser.add_argument('-S', '--show-by', help = 'Show categorie by name', action = 'store')
	parser.add_argument('--setting', help = 'Change setting', action = 'store_true')
	parser.add_argument('-u', '--update', help = 'Update data (all) from internet [take a while] or you can update spesific categorie name with "-U" or "--update-category"', action = 'store_true')
	parser.add_argument('-U', '--update-category', action = 'store', help = "update only to spesific categorie name with exists data.txt if no data then get from internet first")
	parser.add_argument('-l', '--list-category', action = 'store_true', help = 'Show all of categories name')
	parser.add_argument('-d', '--debug', help = 'Show debug process/variable', action = 'store_true')
	parser.add_argument('-dd', '--debug-detach', help = 'Show debug process/variable on new window/terminal', action = 'store_true')
	parser.add_argument('--use-for', action = 'store_true', help = "use for in in looping to show categories and sub categories")
	parser.add_argument('-v', '--version', help = 'show this program version', action = 'store_true')

	if len(sys.argv) == 1:
		parser.print_help()
		print("\n")
		print_me()
	else:
		args = parser.parse_args()
		if args.setting:
			Table.setup_db()
			print(make_colors("please restart !", 'b', 'lc'))
			sys.exit()			
		if args.use_for:
			os.environ.update({'USER_FOR':'1'})
		if args.debug:
			os.environ.update({'DEBUG':'1'})
		elif args.debug_detach:
			os.environ.update({'DEBUG_SERVER':'1'})
			os.system("xterm -e 'export DISPLAY=0.0;python {}'".format(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'debug.py')))

		data = None
		if args.version:
			print(make_colors("version:", 'b', 'lc') + " " + make_colors(get_version.get(), 'b', 'ly'))
			sys.exit()
		if args.update:
			data = Table.get_update()
			data1 = data[0].get('data').get('categoryAllListLite').get('categories')
			data2 = sorted(data1, key = lambda k: k.get('id'))
			data = data2
		elif args.update_category:
			data = Table.get_data_from_file()
			if not data:
				data = Table.get_update()
			data1 = data[0].get('data').get('categoryAllListLite').get('categories')
			data2 = sorted(data1, key = lambda k: k.get('id'))
			data2 = list(filter(lambda k: k.get('name') == args.update_category, data2))
			data = data2
		if args.show_by:
			data = data or Table.get_data_from_file()
			debug(data = data)
			if not data:
				data = Table.get_update()
			data1 = data[0].get('data').get('categoryAllListLite').get('categories')
			data2 = sorted(data1, key = lambda k: k.get('id'))
			data = data2
			debug(data = data)
			data = list(filter(lambda k: k.get('name').lower() == args.show_by.lower(), data))[0]
			debug(data = data, debug = 1)
			if data:
				print("\n")
				print(make_colors(data.get('name'), 'b', 'ly'))
				if not data.get('children'):
					print(make_colors("No Sub Category DATA !", 'lw', 'r'))
				else:
					for c in data.get('children'):
						print(" " * 3 + make_colors(c.get('name'), 'lg'))
						if c.get('children'):
							for x in c.get('children'):
								print(" " * 6 + make_colors(x.get('name'), 'ly'))

			else:
				print(make_colors("No DATA !", 'lw', 'r'))

		if args.list_category or args.show:
			data = data or Table.get_data_from_file()
			debug(data = data)
			if not data:
				data = Table.get_update()
			data1 = data[0].get('data').get('categoryAllListLite').get('categories')
			data2 = sorted(data1, key = lambda k: k.get('id'))
			data = data2
			debug(data = data)
			if data:
				n = 1
				debug(data = data)
				# data = list(filter(lambda k: k.get('name').lower() == 'buku', data))
				if not os.getenv('USER_FOR') == '1':
					Table.show_name_categories(data)
					# Table.show_no_loop(data)
				else:
					for i in data:
						print(make_colors(str(n).zfill(len(str(len(data)))) + ".") + " " + make_colors(i.get('name'), 'ly'))
						n+=1
				q = input(make_colors("Do you want to show sub/child category, select number categorie:", 'b', 'lc') + " ")
				if q:
					print("\n")
					if q.isdigit():
						if int(q) <= len(data):
							print(make_colors(data[int(q) - 1].get('name'), 'b', 'ly'))
							if os.getenv('USER_FOR') == '1':
								data = list(filter(lambda k: k.get('name') == data[int(q) - 1].get('name'), data))[0]
								debug(data = data)
								if not data.get('children'):
									print(make_colors("No Sub Category DATA !", 'lw', 'r'))
								else:
									for c in data.get('children'):
										print(" " * 3 + make_colors(c.get('name'), 'lg'))
										if c.get('children'):
											for x in c.get('children'):
												print(" " * 6 + make_colors(x.get('name'), 'ly'))
							else:
								Table.show_no_loop(data, categorie_name = Table.categorie_name_list[int(q) - 1])			

				if not os.environ.get('USER_FOR'):
					print("\n")
					print(make_colors("##############################################################################################################", 'r', 'lw'))
					print(make_colors("#", 'r', 'lw') + make_colors(" this script not using 'while for in, etc' for show this categories and sub items                           ", 'lc') + make_colors("#", 'r', 'lw'))
					print(make_colors("#", 'r', 'lw') + make_colors(" if you want try use 'for in' just type with '--use-for' or `export/set USER_FOR=1` on terminal/cmd/console ", 'lc') + make_colors("#", 'r', 'lw'))
					print(make_colors("##############################################################################################################", 'r', 'lw'))
					print("\n")
					print_code()

			else:
				print(make_colors("No DATA !", 'lw', 'r'))

		exit = False
		if args.check:
			q = None
			while 1:
				q = input(make_colors("Input any text or type 'q' or 'x' for exit:", 'lc') + " ")
				if q:
					if q in ('q', 'x'):
						exit = True
						break
					else:
						check = Check.check(q)
						if check:
							print(make_colors("TRUE", 'b', 'ly'))
						else:
							print(make_colors("FALSE", 'lw', 'r'))
			print_code(Check.check)
			if exit:
				sys.exit()
		elif args.checking:
			check = Check.check(args.checking)
			if check:
				print(make_colors("TRUE", 'b', 'ly'))
			else:
				print(make_colors("FALSE", 'lw', 'r'))
		elif args.show:
			if not CONFIG.get_config('database', 'type') == 'sqlite' and CONFIG.get_config('database', 'type') in ('mysql', 'postgresql'):
				Table.navigator(CONFIG.get_config('database', 'type'), data)

		print_me()

if __name__ == '__main__':
	# if len(sys.argv) == 2:
	# 	print('input :', sys.argv[1])
	# 	print('output:', Check.check(sys.argv[1]))
	# else:
	# 	#text = 'abcd(ex45[[({{uuuu}})000]ccc'
	# 	# text = 'abcd(ex45[[({{uuuu}})000]])ccc'

	# 	text1 = "123{abcd[123(45)dd]bb}sss"
	# 	text2 = "123{abcd[123(45)dd]bb}}sss"
	# 	print('test 1 input :', text1)
	# 	print('test 2 input :', text2)

	# 	print('test 1 output:', Check.check(text1))
	# 	print('test 2 output:', Check.check(text2))

	# Table.navigator('postgresql')
	# Table.update = True
	# Table.navigator()
	usage()
	# Table.setup_db()
	# print_me()
	# print_code(Check.check)