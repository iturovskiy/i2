import i2_interpreter as interp
import i2_parser as parser

filename = 'simple.i2'
filename2 = 'simple2.i2'

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
