from CLI import CLI

cli = CLI()

cli.add_option("option1", "dest", False)
cli.add_option("option2", "dest", True)
cli.add_option("option3", "dest", True)
cli.add_option("option4", "dest", False)
cli.add_option("option5", "dest", False)
cli.add_option("option6", "dest", False)

# print(cli)
cli.run()
