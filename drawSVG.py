#   ***To do**
#   Allow multiple style elements with links to be added
#   Scripts
#   Prefered order for output
#   Automatic id generation
#   Get element by id


class SVG_Element:
    """ Generic element with attributes and potential child elements.
        Outputs as <type attribute dict> child </type>."""

    indent = 4

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
        """
            Create an element with given type and atrributes,
            and append to self.children.
            Returns the child element.
        """

        child = SVG_Element(type, attributes, child)
        self.children.append(child)
        return child

    def output(self, nesting=0):
        indent = ' ' * nesting * self.indent

        svg_string = indent + '<%s' % (self.type)

        for key, value in self.attributes.iteritems():
            svg_string += ' %s="%s"' % (key, value)

        if not self.children:
            svg_string += '/>'
        else:
            svg_string += '>'

            new_line = False
            for child in self.children:
                if isinstance(child, SVG_Element):
                    svg_string += '\n' + child.output(nesting + 1)
                    new_line = True
                else:
                    svg_string += child

            if new_line:
                svg_string += '\n' + indent + '</%s>' % (self.type)
            else:
                svg_string += '</%s>' % (self.type)

        return svg_string


class SVG(SVG_Element):
    """ SVG element with style element and output that includes XML document string. """

    def __init__(self, attributes=None):
        SVG_Element.__init__(self, 'svg', attributes)
        self.attributes['version'] = 1.1
        self.attributes['baseProfile'] = 'full'
        self.attributes['xmlns'] = 'http://www.w3.org/2000/svg'
        self.attributes['xmlns:xlink'] = 'http://www.w3.org/1999/xlink'

        style_element = SVG_Style_Element()
        self.styleDict = style_element.children
        self.children.append(style_element)

    def addStyle(self, element, attributes):
        """
            Add style to element in self.style.children using a dictionary in
            form {selector: value}
        """

        if element not in self.styleDict:
            self.styleDict[element] = {}
        self.styleDict[element].update(attributes)

    def outputToFile(self, filename):
        """ Prints output to a given filename. Add a .svg extenstion if not given. """

        import os
        if os.path.splitext(filename)[1] == '.svg':
            f = file(filename, 'w')
        else:
            f = file("%s.svg" % filename, 'w')

        f.write(self.output())

    def output(self):
        return SVG_Element.output(self)

    def write(self, filename=None):
        """ Write output to file if given a filename, otherwise return output as a string. """

        if not filename:
            return self.output()
        else:
            self.outputToFile(filename)


class SVG_Style_Element(SVG_Element):
    def __init__(self):
        self.children = {}

    def output(self, nesting=0):
        if not self.children:
            return ''

        style_string = '\n<style>\n'

        for element, style in self.children.items():
            style_string += '  %s{\n' % element

            for key, value in style.items():
                style_string += '    %s:\t%s;\n' % (key, value)
            style_string += '  }\n'

        style_string += '  </style>\n'

        return style_string
