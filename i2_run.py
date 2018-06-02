import i2_parser as parser
import i2_interpreter as interp

filename = 'simple.i2'

data = open(filename).read()
print('--- code ---')
print(data)

prog = parser.parse(data)
if not prog:
	print('not prog')
	raise SystemExit


b = interp.Interpretator(prog)
try:
	b.run()
	raise SystemExit
except RuntimeError:
	pass
