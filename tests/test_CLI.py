import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from CLI import CLI, CLIError

def test_add_valid_option():
	cli = CLI("")
	cli.add_option("option1", "dest", False)
	cli.add_option("option2", "dest", True)
	cli.add_option("option3", "dest", True)
	cli.add_option("option4", "dest", False)
	assert cli.options == {
		"option1": ["dest", False],
		"option2": ["dest", True],
		"option3": ["dest", True],
		"option4": ["dest", False],
	}

def test_add_invalid_option():
	cli = CLI("")
	with pytest.raises(CLIError):
		cli.add_option(123, "dest", False)
	with pytest.raises(CLIError):
		cli.add_option("opt", 123, True)
	with pytest.raises(CLIError):
		cli.add_option(None, "dest", True)
	with pytest.raises(CLIError):
		cli.add_option("opt", "dest", None)
	with pytest.raises(CLIError):
		cli.add_option("", "dest", None)
	with pytest.raises(CLIError):
		cli.add_option("opt", "", None)

def test_remove_options():
	cli = CLI("")
	cli.add_option("option1", "dest", False)
	cli.add_option("option2", "dest", True)
	cli.add_option("option3", "dest", True)
	cli.add_option("option4", "dest", False)
	cli.add_option("option5", "dest", False)
	cli.add_option("option6", "dest", False)

	cli.remove_options("option3", "option6", "option1")
	assert cli.options == {
		"option2": ["dest", True],
		"option4": ["dest", False],
		"option5": ["dest", False],
	}

