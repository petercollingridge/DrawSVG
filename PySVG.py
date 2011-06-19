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
        self.children.append(SVG_Element(type, attributes, child))    
    
    def output(self):
        svg_string = '<%s' % (self.type)
        
        for key, value in self.attributes.items():
            svg_string += ' %s="%s"' % (key, value)
        
        if not self.children:
            svg_string += '/>'
        else:
            svg_string += '>\n'
            
            for child in self.children:
                if isinstance(child, SVG_Element):
                    svg_string += child.output()
                else:
                    svg_string += '%s\n' % child
                
            svg_string += '</%s>\n' % (self.type)
            
        
        return svg_string

class SVG(SVG_Element):
    """ SVG element, output includes XML document string. """
    
    def __init__(self, attributes=None):
        SVG_Element.__init__(self, 'svg', attributes)
        self.attributes['version'] = 1.1
        self.attributes['xmlns'] = 'http://www.w3.org/2000/svg'
    
    def output(self):
        svg_string  = '<?xml version="1.0" standalone="no"?>\n'
        svg_string += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
        
        svg_string +=  SVG_Element.output(self)
            
        return svg_string