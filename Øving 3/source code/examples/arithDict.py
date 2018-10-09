'''Fancier format string example, with locals().'''

x = 20
y = 30
sum = x + y
prod = x * y
formatStr = '{row} + {y} = {sum}; {row} * {y} = {prod}.'
equations = formatStr.format(**locals())
print(equations)
