import i2_parser as parser
import i2_interpreter as interp

filename = 'simple.i2'

data = open(filename).read()

parsed = parser.parse(data)
if not parsed:
	print('not prog')
	raise SystemExit

program = interp.Interpreter(parsed)
try:
	program.run()
	raise SystemExit
except RuntimeError:
	pass
