import termios
import fcntl
import sys
import os
from Colors import *

class CLIError(Exception):
	pass

class CLI_OneSelection:
	def __init__(self, title: str = "") -> None:
		self.__title: str = title
		self.__options: dict[str, list[str, bool]] = {}
		self.__index: int = 0
		self.__buffer = ""
		self.__LINE_UP = '\033[1A'
		self.__LINE_CLEAR = '\x1b[2K'

	def __str__(self) -> str:
		if len(self.__options) == 0:
			return ""
		content = ""
		print(f"{BHWHITE}{self.__title}{RESET}", end="")
		for i, value in zip(range(len(self.__options)), self.__options.values()):
			if self.__index == i:
				content += f" {BHCYAN}{UCYAN}{value[0]}{RESET}"
			else:
				content += f" {value[0]}"
			if i < len(self.__options) - 1:
				content += f" {BLACK}/{RESET}"
		return content

	def add_option(self, name: str, description: str, value: bool = False):
		if type(name) != str:
			raise CLIError("Invalid name type.")
		if type(description) != str:
			raise CLIError("Invalid description type.")
		if type(value) != bool:
			raise CLIError("Invalid value type.")
		if (len(name)) == 0:
			raise CLIError("Name is empty.")
		if (len(description)) == 0:
			raise CLIError("Description is empty.")
		self.__options[name] = [description, value]

	def remove_options(self, *name: str):
		if len(name) == 0:
			return
		for i in range(len(name)):
			try:
				self.__options.pop(name[i])
			except:
				print(f"Invalid key to remove '{name[i]}'...")

	def get_options(self, full: bool = False):
		if full:
			return self.__options
		opts = {}
		for key, value in self.__options.items():
			opts[key] = value[1]
		return opts

	def get_selection(self):
		for key, value in self.__options.items():
			if value[1] == True:
				return key
		return None

	def __get_key(self) -> str | None:
		key = None
		c = sys.stdin.read(1)
		if c:
			self.__buffer += c
			# Detect Escape Only
			if self.__buffer == "\x1b":
				c = sys.stdin.read(1)
				if c == "":
					key = 'Escape'
					self.__buffer = ""
				else:
					self.__buffer += c
			# Detect Arrow
			elif self.__buffer.startswith("\x1b["):
				if len(self.__buffer) == 3:
					if self.__buffer == "\x1b[A":
						key = 'Up'
					elif self.__buffer == "\x1b[B":
						key = 'Down'
					elif self.__buffer == "\x1b[C":
						key = 'Right'
					elif self.__buffer == "\x1b[D":
						key = 'Left'
					self.__buffer = ""
			# Detect other character
			elif not self.__buffer.startswith("\x1b"):
				key = repr(self.__buffer)
				self.__buffer = ""
		return key

	def __print_error(self, e: Exception):
		print(f"{BHRED}Error{RESET}")
		print(f"{BRED}Name: {type(e).__name__}{RESET}")
		if str(e) != "":
			print(f"{BRED}Message: {e}{RESET}")

	def __print_option(self):
		# for _ in range(len(self.__options) + 1):
		print(self.__LINE_UP, end=self.__LINE_CLEAR)
		print(self)

	def __handle_input(self, key: str):
		if key == 'Left':
			if self.__index == 0:
				self.__index = len(self.__options) - 1
			else:
				self.__index -= 1
			pass
		elif key == 'Right':
			if self.__index + 1 == len(self.__options):
				self.__index = 0
			else:
				self.__index += 1
			pass
		elif key == repr('\n'):
			for i, key in zip(range(len(self.__options)), self.__options.keys()):
				if self.__index == i:
					self.__options[key][1] = not self.__options[key][1]
					break
			return 'exit'
		else:
			return None
		self.__print_option()

	def run(self):
		if len(self.__options) == 0:
			return print("You haven't added any options.")

		fd = sys.stdin.fileno()
		oldterm = termios.tcgetattr(fd)
		newattr = termios.tcgetattr(fd)
		newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
		termios.tcsetattr(fd, termios.TCSANOW, newattr)

		oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

		try:
			print(self)
			while True:
				try:
					key = self.__get_key()
					if key != None:
						val = self.__handle_input(key=str(key))
						if val == 'exit':
							break
				except IOError:
					pass
				except KeyboardInterrupt:
					break
				except Exception as e:
					self.__print_error(e)
					break
		finally:
			termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
			fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

if __name__ == "__main__":
	cli = CLI_OneSelection(title="Which option you want ?")

	cli.add_option("Option1", "Option 1")
	cli.add_option("Option2", "Option 2")
	cli.add_option("Option3", "Option 3")
	# print(cli)
	cli.run()
	print(cli.get_selection())
