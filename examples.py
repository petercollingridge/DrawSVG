import PySVG

my_svg = PySVG.SVG({'width':600})
my_svg.attributes['height'] = 400

my_svg.addChildElement('rect', {'x':10, 'y':15, 'id':'rect-1'}, 'child')
print my_svg.output()