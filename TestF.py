class TestF:
	def __init__(self, choose: int) -> None:
		if choose == 0:
			self.func = self.__func_0
		if choose == 1:
			self.func = self.__func_1
		if choose == 2:
			self.func = self.__func_2
		pass

	def __func_0(self, params):
		print(f"Func 0 : {params}")

	def __func_1(self, params):
		print(f"Func 1 : {params}")

	def __func_2(self, params):
		print(f"Func 2 : {params}")


if __name__ == "__main__":
	t = TestF(1)
	t.func("hey")
