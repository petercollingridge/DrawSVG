#   ***To do**
#   Make style an SVG_Element
#   Allow multiple style elements with links to be added
#   Scripts
#   Prefered order for output
#   Nesting parameter
#   Automatic id generation
#   Get element by id

class SVG_Element:
    """ Generic element with attributes and potential child elements.
        Outputs as <type attribute dict> child </type>."""
    
    def __init__(self, type, attributes=None, child=None):
        self.type = type
        
        if attributes:
            self.attributes = attributes
        else:
            self.attributes = {}
        
        if child:
            self.children = [child]
        else:
            self.children = []
    
    def addChildElement(self, type, attributes=None, child=None):
        child_element = SVG_Element(type, attributes, child)
        self.children.append(child_element)
        return child__element
    
    def output(self, nesting=0):
        svg_string = ' '*nesting + '<%s' % (self.type)
        
        for key, value in self.attributes.items():
            svg_string += ' %s="%s"' % (key, value)
        
        if not self.children:
            svg_string += '/>\n'
        else:
            svg_string += '>\n'
            
            for child in self.children:
                if isinstance(child, SVG_Element):
                    svg_string += child.output(nesting+1)
                else:
                    svg_string += ' '*(nesting+1) + '%s\n' % child
                
            svg_string += ' '*nesting + '</%s>\n' % (self.type)
            
        
        return svg_string

class SVG(SVG_Element):
    """ SVG element, output includes XML document string. """
    
    def __init__(self, attributes=None):
        SVG_Element.__init__(self, 'svg', attributes, SVG_Style_Element())
        self.attributes['version'] = 1.1
        self.attributes['xmlns'] = 'http://www.w3.org/2000/svg'
        self.attributes['xmlns:xlink'] = 'http://www.w3.org/1999/xlink'

    def addStyle(self, element, *args):
        """ Add style to self.style dictionary
            in the form addStyle(element (parameter1, value1), (parameter2, value2)) """
   
        if element not in self.children[0].styles:
            self.children[0].styles[element] = {}

        for (key, value) in args:
            self.children[0].styles[element][key] = value
    
    def output(self):
        svg_string  = '<?xml version="1.0"  encoding="UTF-8" standalone="no"?>\n'
        svg_string += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
        
        svg_string +=  SVG_Element.output(self)
            
        return svg_string
    
class SVG_Style_Element(SVG_Element):
    def __init__(self):
        self.styles = {}
        
    def output(self, nesting=0):
        if not self.styles:
            return
        
        style_string = '<style>\n'
      
        for element, style in self.styles.items():
            style_string += '  %s{\n' % element
            
            for key, value in style.items():
                style_string += '    %s:\t%s;\n' % (key, value)
            style_string += '  }\n'
        
        style_string += '  </style>\n\n'
        
        return style_string
