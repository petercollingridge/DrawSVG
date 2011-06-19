import PySVG

my_svg = PySVG.SVG({'width':600})
my_svg.attributes['height'] = 400

# Adding child elements all at once
my_svg.addChildElement('Text', {'id':'text-1', 'x':10, 'y':15}, 'This is a child')
my_svg.addChildElement('rect', {'id':'rect-1', 'x':20, 'y':25, 'width':20, 'height':25})

# Adding a child element piecemeal
new_rect = PySVG.SVG_Element('rect', {'id':'rect-2', 'x':100, 'y':25})
new_rect.attributes['height'] = 50
new_rect.attributes['width'] = 80
my_svg.children.append(new_rect)

# Styling
my_svg.addStyle('rect', ('fill', 'green'), ('stroke-width', 2), ('stroke', 'black'))

# Write output to file
fout = file('test.svg', 'w')
fout.write(my_svg.output())