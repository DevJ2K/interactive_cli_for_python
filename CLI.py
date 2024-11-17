import termios
import fcntl
import sys
import os
from Colors import *


class CLI:
	def __init__(self) -> None:
		self.options: list[tuple[str, bool]] = []
		self.index = 0
		self.fd = sys.stdin.fileno()
		pass

	def __str__(self) -> str:
		if len(self.options) == 0:
			return ""
		content = ""
		# ❯
		for i in range(len(self.options)):
			if self.index == i:
				content += BHCYAN
				content += "❯  "
				content += RESET
			else:
				content += "   "
			color = BHGREEN if self.options[i][1] == True else BHRED
			content += f"[{color}*{RESET}] "
			if self.index == i:
				content += f"{BHCYAN}- {UCYAN}{self.options[i][0]}{RESET}\n"
			else:
				content += f"- {self.options[i][0]}\n"

		return content

	def add_option(self, option: str, value: bool = False):
		self.options.append((option, value))
		pass

	def remove_option(self, option: str):
		pass


	def run():
		pass

if __name__ == "__main__":
	cli = CLI()

	cli.add_option("Option 1")
	cli.add_option("Option 2", True)
	cli.add_option("Option 3", True)
	cli.add_option("Option 4", False)

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
