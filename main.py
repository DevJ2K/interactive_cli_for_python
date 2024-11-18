from CLI import CLI

cli = CLI()

cli.add_option("option1", "Option n*1", False)
cli.add_option("option2", "Option n*2", True)
cli.add_option("option3", "Option n*3", True)
cli.add_option("option4", "Option n*4", False)
cli.add_option("option5", "Option n*5", False)
cli.add_option("option6", "Option n*6", False)

# print(cli)
cli.run()
