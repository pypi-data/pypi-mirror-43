#! /usr/bin/env python3
from sys import stdout as sys_stdout
from platform import system as platform_sys


if platform_sys().lower() == 'linux':
	DEF_VISUAL = '\033[1m\033[94m[{}]\033[0m {}{}'
else:
	DEF_VISUAL = '[{}] {}{}'


def print_msg(ctx, msg, end='\n'):
	sys_stdout.write(DEF_VISUAL.format(ctx, msg, end))
	sys_stdout.flush()
