# -*- coding: utf-8 -*-

import i2_interpreter as interp
import i2_parser as parser

filename1 = 'simple_test.i2'
filename2 = 'simple_fib.i2'
filename3 = 'simple_rec.i2'
filename0 = 'laby_algo.i2'

data = open(filename1).read()

parsed = parser.parse(data)
if not parsed:
	print('Something went wrong - not parsed')
	raise SystemExit

program = interp.Interpreter(parsed)
try:
	exitcode = program.run()
	if exitcode is None:
		exitcode = 'nothing';
	print('\n\nFunction "work" has returned:', exitcode)
	raise SystemExit
except RuntimeError:
	pass
