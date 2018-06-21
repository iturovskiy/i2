import i2_interpreter as interp
import i2_parser as parser

filename = 'simple_test.i2'
filename2 = 'simple_fib.i2'
filename3 = 'simple_buble.i2'
filename5 = 'simple_rec.i2'
filename6 = 'simple_laby.i2'

data = open(filename).read()

parsed = parser.parse(data)
if not parsed:
	print('Something went wrong - not parsed')
	raise SystemExit

program = interp.Interpreter(parsed)
try:
	exitcode = program.run()
	if exitcode is not None:
		print('-Exit code ', exitcode)
	raise SystemExit
except RuntimeError:
	pass
