import PySVG

my_svg = PySVG.SVG({'width':600})
my_svg.attributes['height'] = 400

my_svg.addChildElement('Text', {'id':'text-1', 'x':10, 'y':15}, 'This is a child')
my_svg.addChildElement('rect', {'id':'rect-2', 'x':20, 'y':25, 'width':20, 'height':25, 'fill':'blue'})

fout = file('test.svg', 'w')
fout.write(my_svg.output())