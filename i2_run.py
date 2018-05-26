import i2_parser as parser
import i2_interpreter as interp

filename = 'simple.txt'

data = open(filename).read()
prog = parser.parse(data)
if not prog:
	raise SystemExit
b = interp.Interpretator(prog)
try:
	b.run()
	raise SystemExit
except RuntimeError:
	pass
