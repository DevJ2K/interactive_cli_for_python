import termios
import fcntl
import sys
import os
import time

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
