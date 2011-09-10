import drawSVG

def simplestExample():
    """ Create a valid svg document containing an empty svg element"""

    my_svg = drawSVG.SVG()
    return my_svg

def addRectElement():
    """ Create an svg document containing a rectangle """

    my_svg = drawSVG.SVG()
    #   Add the element: <rect x="20" y="25" width="20" height="25"/>
    my_svg.addChildElement('rect', {'x':20, 'y':40, 'width':80, 'height':50})
    return my_svg

def addRectElementInStages():

    my_svg = drawSVG.SVG()
    rect = my_svg.addChildElement('rect')
    rect.attributes['x'] = 20
    rect.attributes['y'] = 40
    rect.attributes['width'] = 80
    rect.attributes['height'] = 50
    
    return my_svg
    
def addSVGAttributes():
    """ Create an svg document with width=80, height=50 """
    
    # Can pass attributes during initialisation
    my_svg = drawSVG.SVG({'width':80})
    
    # Or can (re)define later
    my_svg.attributes['height'] = 50
    
    my_svg.addChildElement('rect', {'width':200, 'height':200})
    return my_svg
    
def addCSSStyling():
    my_svg = drawSVG.SVG({'width':200, 'height':100})
    my_svg.addStyle('rect', {'fill': 'green', 'stroke-width': 2, 'stroke': 'black'})
    my_svg.addChildElement('rect', {'x':20, 'y':40, 'width':80, 'height':50})
    my_svg.addChildElement('circle', {'cx':120, 'cy':40, 'r':25})
    return my_svg
    
def example2():
    my_svg = drawSVG.SVG({'width':600})
    my_svg.attributes['height'] = 400

    # Adding child elements all at once
    my_svg.addChildElement('Text', {'id':'text-1', 'x':10, 'y':15}, 'This is a child')
    my_svg.addChildElement('rect', {'id':'rect-1', 'x':20, 'y':25, 'width':20, 'height':25})

    # Adding a child element piecemeal
    new_rect = drawSVG.SVG_Element('rect', {'id':'rect-2', 'x':100, 'y':25})
    new_rect.attributes['height'] = 50
    new_rect.attributes['width'] = 80
    my_svg.children.append(new_rect)

    new_rect = drawSVG.SVG_Element('rect')
    new_rect.attributes = {'id':'rect-2', 'x':100, 'y':125}
    new_rect.attributes['height'] = 50
    new_rect.attributes['width'] = 80
    my_svg.children.append(new_rect)

    # Styling
    my_svg.addStyle('rect', ('fill', 'green'), ('stroke-width', 2), ('stroke', 'black'))

#my_svg = addRectElementInStages()
my_svg = addCSSStyling()
my_svg.outputToFile('test.svg')
