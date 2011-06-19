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
        
    def output(self):
        s = '<%s' % (self.type)
        
        for key, value in self.attributes.items():
            s += ' %s="%s"' % (key, value)
        
        if self.children:
            s += '>\n'
            for child in self.children:
                s += '%s\n' % (child)
            s += '</%s>' % (self.type)
        else:
            s += '/>'
        
        return s