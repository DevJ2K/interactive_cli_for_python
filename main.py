from CLI import CLI

cli = CLI()

cli.add_option("Option 1")
cli.add_option("Option 2", True)
cli.add_option("Option 3", True)
cli.add_option("Option 4", False)

print(cli)
