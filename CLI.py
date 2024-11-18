import termios
import fcntl
import sys
import os
from Colors import *

class CLIError(Exception):
	pass

class CLI:
	def __init__(self, title: str) -> None:
		# Use a dictionary instead of list, it will be more practical to remove or retrieve options from the CLI.
		self.title: str = title
		# self.options: list[tuple[str, bool]] = []
		self.options: dict[str, list[str, bool]] = {}
		self.index: int = 0
		self.fd = sys.stdin.fileno()
		pass

	def __str__(self) -> str:
		if len(self.options) == 0:
			return ""
		content = ""
		print(self.title)
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

		# WITH LIST
		# for i in range(len(self.options)):
		# 	if self.index == i:
		# 		content += BHCYAN
		# 		content += "❯  "
		# 		content += RESET
		# 	else:
		# 		content += "   "
		# 	color = BHGREEN if self.options[i][1] == True else BHRED
		# 	content += f"[{color}*{RESET}] "
		# 	if self.index == i:
		# 		content += f"{BHCYAN}- {UCYAN}{self.options[i][0]}{RESET}\n"
		# 	else:
		# 		content += f"- {self.options[i][0]}\n"

		# return content[:-1]

	def add_option(self, name: str, description: str, value: bool = False):
		self.options[name] = [description, value]

	def remove_option(self, *name: str):
		if len(name) == 0:
			return
		print(name)
		for i in range(len(name)):
			try:
				self.options.pop(name[i])
			except:
				print(f"Key '{name[i]}' not exist.")

	def test(self):
		LINE_UP = '\033[1A'
		LINE_CLEAR = '\x1b[2K'

		import time
		print(self)

		time.sleep(1)
		self.index = 2
		for _ in range(len(self.options) + 1):
			print(LINE_UP, end=LINE_CLEAR)
		print(self)

		time.sleep(1)
		self.index = 1
		for _ in range(len(self.options) + 1):
			print(LINE_UP, end=LINE_CLEAR)
		print(self)

		time.sleep(1)

	def run():
		pass

if __name__ == "__main__":
	cli = CLI(title="Select an option.")

	cli.add_option("Option1", "Option 1")
	cli.add_option("Option2", "Option 2", True)
	cli.add_option("Option3", "Option 3", True)
	cli.add_option("Option4", "Option 4", False)

	# print(cli)
	# cli.test()
	cli.remove_option("Salut", "les", "amis")
	cli.remove_option("Option2")
	print(cli)


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
