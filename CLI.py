import termios
import fcntl
import sys
import os
from Colors import *

class CLIError(Exception):
	pass

class CLI:
	def __init__(self, title: str = "") -> None:
		self.title: str = title
		self.options: dict[str, list[str, bool]] = {}
		self.index: int = 0
		self.buffer = ""
		self.__LINE_UP = '\033[1A'
		self.__LINE_CLEAR = '\x1b[2K'

	def __str__(self) -> str:
		if len(self.options) == 0:
			return ""
		content = ""
		print(f"{BHWHITE}{self.title} (Press 'Enter' to continue){RESET}")
		for i, value in zip(range(len(self.options)), self.options.values()):
			if self.index == i:
				content += BHCYAN
				content += "❯  "
				content += RESET
			else:
				content += "   "
			color = BHGREEN if value[1] == True else BHRED
			content += f"[{color}*{RESET}] "
			if self.index == i:
				content += f"{BHCYAN}- {UCYAN}{value[0]}{RESET}\n"
			else:
				content += f"- {value[0]}\n"
		return content[:-1]

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
		self.options[name] = [description, value]

	def remove_options(self, *name: str):
		if len(name) == 0:
			return
		print(name)
		for i in range(len(name)):
			try:
				self.options.pop(name[i])
			except:
				print(f"Key '{name[i]}' not exist.")

	def get_options(self):
		opts = {}
		for key, value in self.options.items():
			opts[key] = value[1]
		return opts


	def __get_key(self) -> str | None:
		key = None
		c = sys.stdin.read(1)
		if c:
			self.buffer += c

			# Detect Escape Only
			if self.buffer == "\x1b":
				c = sys.stdin.read(1)
				if c == "":
					key = 'Escape'
					self.buffer = ""
				else:
					self.buffer += c

			# Detect Arrow
			elif self.buffer.startswith("\x1b["):
				if len(self.buffer) == 3:
					if self.buffer == "\x1b[A":
						key = 'Up'
					elif self.buffer == "\x1b[B":
						key = 'Down'
					elif self.buffer == "\x1b[C":
						key = 'Right'
					elif self.buffer == "\x1b[D":
						key = 'Left'
					self.buffer = ""

			# Detect other character
			elif not self.buffer.startswith("\x1b"):
				key = repr(self.buffer)
				self.buffer = ""
		return key

	def __print_error(self, e: Exception):
		print(f"{BHRED}Error{RESET}")
		print(f"{BRED}Name: {type(e).__name__}{RESET}")
		if str(e) != "":
			print(f"{BRED}Message: {e}{RESET}")

	def __print_option(self):
		for _ in range(len(self.options) + 1):
			print(self.__LINE_UP, end=self.__LINE_CLEAR)
		print(self)

	def __handle_input(self, key: str):
		if key == 'Up':
			if self.index == 0:
				self.index = len(self.options) - 1
			else:
				self.index -= 1
			pass
		elif key == 'Down':
			if self.index + 1 == len(self.options):
				self.index = 0
			else:
				self.index += 1
			pass
		elif key == repr(' '):
			for i, key in zip(range(len(self.options)), self.options.keys()):
				if self.index == i:
					self.options[key][1] = not self.options[key][1]
					break
		elif key == repr('\n'):
			return 'exit'
		else:
			return None
		self.__print_option()

	def run(self):
		if len(self.options) == 0:
			print("Please an some option.")
			return
		fd = sys.stdin.fileno()

		oldterm = termios.tcgetattr(fd)
		newattr = termios.tcgetattr(fd)
		newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
		termios.tcsetattr(fd, termios.TCSANOW, newattr)

		oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

		try:
			buffer = ""
			print(self)
			while True:
				try:
					key = self.__get_key()
					if key == None:
						continue
					else:
						val = self.__handle_input(key=str(key))
						if val == 'exit':
							break
						# print(f"Pressed : {key}")
						continue
				except IOError:
					pass
				except KeyboardInterrupt:
					print("KeyBoard Interrupt")
					break
				except Exception as e:
					self.__print_error(e)
					break
		finally:
			# print("Clean fd...")
			termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
			fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

if __name__ == "__main__":
	cli = CLI(title="Select an option.")

	cli.add_option("Option1", "Option 1", False)
	cli.add_option("Option2", "Option 2", False)
	cli.add_option("Option3", "Option 3", False)
	cli.add_option("Option4", "Option 4", False)
	cli.run()
	print(cli.get_options())


if __name__ == "2__main__":
	fd = sys.stdin.fileno()

	oldterm = termios.tcgetattr(fd)
	newattr = termios.tcgetattr(fd)
	newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
	termios.tcsetattr(fd, termios.TCSANOW, newattr)

	oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

	try:
		buffer = ""
		while True:
			try:
				c = sys.stdin.read(1)
				if c:
					buffer += c
					# print(f"{buffer} | {repr(c)}")

					# Detect Escape Only
					if buffer == "\x1b":
						# time.sleep(0.01)
						c = sys.stdin.read(1)
						if c == "":
							print("Escape pressed")
							buffer = ""
						else:
							buffer += c

					# Detect Arrow
					elif buffer.startswith("\x1b["):
						if len(buffer) == 3:
							if buffer == "\x1b[A":
								print("Up arrow pressed")
							elif buffer == "\x1b[B":
								print("Down arrow pressed")
							elif buffer == "\x1b[C":
								print("Right arrow pressed")
							elif buffer == "\x1b[D":
								print("Left arrow pressed")
							buffer = ""

					# Detect other character
					elif not buffer.startswith("\x1b"):
						print(f"Got character: {repr(buffer)}")
						buffer = ""

					else:
						pass
			except IOError:
				print("Here")
				pass
			except KeyboardInterrupt:
				print("KeyBoard Interrupt")
				break
	finally:
		termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
