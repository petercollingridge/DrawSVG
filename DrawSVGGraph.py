import math
from DrawSVG import SVG

#       *** To Do **
#   Allow x-values to be defined
#       Fix read data to file to work with this
#   Align axis values
#   Get axis to work for numbers < 0
#   Get axis divisions to work for numbers < 1
#   Add tick marks to axes
#   Add data labels - with mouseover?
#   Get text alignments work with different font-sizes?

class Graph(SVG):
    """ Plots series of (x,y) data on a SVG line graph. """
    
    def __init__(self, attributes=None):
        SVG.__init__(self, attributes)
        
        self.data = {}
        self.colours = ['#000000']
        self.colours = ['#0060e5', '#001060', '#e52060', '#a00030', '#00c020', '#006010']
        
        self.left_pad  = 10.5
        self.right_pad = 10.5
        self.upper_pad = 10.5
        self.lower_pad = 10.5
        self.origin_x = self.left_pad
        self.origin_y = self.lower_pad
        
        # Set default values if not already defined
        self.attributes['width'] = self.attributes.get('width', 400)
        self.attributes['height'] = self.attributes.get('height', 400)
        
        # Axis options
        self.x_axis = True
        self.y_axis = True
        self.x_gridlines = True
        self.y_gridlines = True
        self.x_axis_units = True
        self.y_axis_units = True
        self.x_axis_label = None
        self.y_axis_label = None
        
        # These are automatically generated based on the data but can be predefined
        self.min_x = None
        self.max_x = None
        self.div_x = None
        self.min_y = None
        self.max_y = None
        self.div_y = None
        
        self._addDefaultStyles()
        
    def _addDefaultStyles(self):
        """ Set default styles to style dictionary"""
    
        self.addStyle('.background', {'fill':'none'})
        self.addStyle('.axis', {'stroke':'#111', 'stroke-width':0.5})
        self.addStyle('.axis-label', {'font-size': '14px', 'font-family': 'Arial', 'text-anchor': 'middle'})
        self.addStyle('.axis-units', {'font-size':'10px', 'font-family':'Arial'})
        self.addStyle('.y-axis-text', {'text-anchor': 'end'})
        self.addStyle('.gridlines', {'stroke':'black', 'stroke-width':0.5, 'fill':'none', 'opacity':0.5})
        self.addStyle('.data-series', {'stroke-width':1, 'fill':'none', 'opacity':1})

    def addDataFromFile(self, filename):
        """ Read in a tab-delimited file with a heading row and add to self.data dictionary """
    
        try:
            fin = open(filename, 'r')
        except IOError:
            print "Could not open file", filename
            return
        
        headings = fin.readline().rstrip('\n').split('\t')
        for h in headings:
            self.data[h] = []
        
        # Should treat first column as x value (unless only one column)
        for line in fin.readlines():
            temp = line.rstrip('\n').split('\t')
            for i, h in enumerate(headings):
                self.data[h].append(float(temp[i]))
        
    def output(self):
        self._getDataDivisions()
        self._determinePlottingFunctions()
        self._addBackground()
        self._addAxes()
        self._drawAxisUnits()
        self._drawGridlines()
        self._plotData()
        return SVG.output(self)

    def _getDataDivisions(self):
        if not self.data:
            return

        x_data = [data[0] for series in self.data.values() for data in series]
        y_data = [data[1] for series in self.data.values() for data in series]
    
        if not self.min_x: self.min_x = min(x_data)
        if not self.max_x: self.max_x = max(x_data)
        if not self.max_y: self.max_y = max(y_data)
        if not self.min_y: self.min_y = min(y_data)
        
        #   Calculate reasonable division for x-axis
        if not self.div_x:
            span_x = self.max_x - self.min_x
            self.div_x = math.pow(10, int(math.log(max([self.max_x, -self.min_x]), 10)))
            if self.max_x/self.div_x > 5:
                self.div_x *= 2
            elif self.max_x/self.div_x < 3:
                self.div_x *= 0.5

        self.x_divisions = [x*self.div_x for x in range(-int(math.ceil(-self.min_x / self.div_x)), int(math.ceil(self.max_x / self.div_x))+1)]
        self.min_x = self.x_divisions[0]

        #   Calculate reasonable division for y-axis        
        if not self.div_y:
            span_y = self.max_y - self.min_y
            self.div_y = math.pow(10, int(math.log(max([self.max_y, -self.min_y]), 10)))
            if span_y/self.div_y > 4:
                self.div_y *= 2
            elif span_y/self.div_y < 3:
                self.div_y *= 0.5

        self.y_divisions = [y*self.div_y for y in range(-int(math.ceil(-self.min_y / self.div_y)), int(math.ceil(self.max_y / self.div_y))+1)]
        self.min_y = self.y_divisions[0]

    def _determinePlottingFunctions(self):
        if self.x_axis_label:
            self.origin_y += 20
        if self.y_axis_label:
            self.origin_x += 20
        
        # Should calculate based on unit length
        if self.x_axis_units:
            self.origin_y += 16
        if self.y_axis_units:
            self.origin_x += 16
            
        self.chart_width  = self.attributes['width'] - self.right_pad - self.origin_x
        self.chart_height = self.attributes['height'] - self.upper_pad - self.origin_y
        x_scaling_factor = self.chart_width  * 1.0 / (self.max_x - self.min_x)
        y_scaling_factor = self.chart_height * 1.0 / (self.y_divisions[-1] - self.y_divisions[0])
        
        # Functions for converting x and y values into coordinates on the SVG
        self.f_x = lambda x: self.origin_x + x_scaling_factor * (x - self.x_divisions[0])
        self.f_y = lambda y: self.attributes['height'] - self.origin_y - y_scaling_factor * (y - self.y_divisions[0])

    def _addBackground(self):
        if self.children[0].children['.background'].get('fill', 'none') != 'none':
            self.addChildElement('rect',
                                {'class':'background',
                                'x':0, 'y':0,
                                'width':self.attributes['width'],
                                'height':self.attributes['height']})

    def _addAxes(self):    
        if self.x_axis_label:
            x = 0.5*(self.origin_x + self.attributes['width'] - self.right_pad)
            y = self.attributes['height'] - self.lower_pad
            self.addChildElement('text',
                                {'class':'axis-label', 'x': x, 'y': y},
                                self.x_axis_label)

        if self.y_axis_label:
            x = self.left_pad
            y = 0.5*(self.attributes['height'] - self.origin_y + self.upper_pad)
            self.addChildElement('text',
                                {'class':'axis-label', 'x': 0, 'y': y,
                                'transform': 'translate(%.1f) rotate(-90, 0, %.1f)' % (x+5, y)},
                                self.y_axis_label)

        # Add tick marks/values
        if self.x_axis:
            self.addChildElement('line',
                                {'class': 'axis',
                                'x1': self.origin_x,
                                'y1': self.attributes['height'] - self.origin_y,
                                'x2': self.attributes['width'] - self.right_pad,
                                'y2': self.attributes['height'] - self.origin_y})

        if self.y_axis:
            self.addChildElement('line',
                                {'class': 'axis',
                                'x1': self.origin_x,
                                'y1': self.attributes['height'] - self.origin_y,
                                'x2': self.origin_x,
                                'y2': self.upper_pad})

    def _drawGridlines(self):
        if self.x_gridlines or self.y_gridlines:
            gridline_group = self.addChildElement('g', {'class': 'gridlines'})

        if self.x_gridlines:
            for x in self.x_divisions[1:-1]:
                gridline_x = int(self.f_x(x)) + 0.5
                gridline_group.addChildElement('line',
                                               {'x1': gridline_x,
                                                'y1': self.attributes['height'] - self.origin_y,
                                                'x2': gridline_x,
                                                'y2': self.attributes['height'] - self.origin_y - self.chart_height})

        if self.y_gridlines:
            for y in self.y_divisions[1:-1]:
                gridline_y = int(self.f_y(y)) + 0.5
                gridline_group.addChildElement('line',
                                               {'x1': self.origin_x,
                                                'y1': gridline_y,
                                                'x2': self.origin_x + self.chart_width,
                                                'y2': gridline_y})

    def _drawAxisUnits(self):
        label_group = self.addChildElement('g', {'class': 'axis-units y-axis-text'})
        
        if abs(self.y_divisions[1]) < 1:
            y_to_string = lambda y: '%.1f' % y
        else:
            y_to_string = lambda y: '%d' % y
        
        for y in self.y_divisions:
            label_group.addChildElement('text', {'x': self.origin_x-3, 'y': self.f_y(y)+3}, y_to_string(y))
        return

        #   x-axis labels
        if abs(self.div_x) < 1:
            x_to_string = lambda x: '%.1f' % x
        else:
            x_to_string = lambda x: '%d' % x

        x = self.min_x
        while x < self.max_x:
            x_string = x_to_string(x)
            path += '    <text x="%.1f" y="%.1f">' % (self.f_x(x) - 4*len(x_string), self.origin_y + 12)
            path += x_string
            path += '</text>\n' 
            x += self.div_x
        path += '  </g>\n'

        return path
        
    def _plotData(self):
        """ Create <path> of straight lines for each series of data """
        
        for series, (name, data) in enumerate(self.data.items()):
            path = 'M%.1f %1f' % (self.f_x(data[0][0]), self.f_y(data[0][1]))
            for x, y in data[1:]:
                path += ' L%.1f %1f' % (self.f_x(x), self.f_y(y))
                
            self.addChildElement('path',
                                {'class': 'data-series',
                                 'stroke': self.colours[series],
                                 'd': path})

class BarGraph(Graph):
    """ Plots a horizontal bar chart. """

    def __init__(self, attributes=None):
        Graph.__init__(self, attributes)
        
        self.x_gridlines = False
        self.x_axis_units = False
        self.gap_width = 2

        self.addStyle('.bar', {'fill': '#888', 'opacity': 0.7})
        self.addStyle('.bar:hover', {'opacity': 1})

    def addDataFromFile(self, filename):
        """ Read in a tab-delimited file with a heading row and add to self.data dictionary """
    
        try:
            fin = open(filename, 'r')
        except IOError:
            print "Could not open file", filename
            return
        
        for line in fin.readlines():
            (key, value) = line.rstrip().split('\t')
            self.data[key] = float(value)

    def output(self):
        self._getDataDivisions()
        self._determinePlottingFunctions()
        self._addBackground()
        self._addAxes()
        self._drawAxisUnits()
        self._drawGridlines()
        self._plotData()
        return SVG.output(self)

    def _getDataDivisions(self):      
        if not self.data:
            return

        if not self.max_x: self.max_x = len(self.data)
        if not self.min_x: self.min_x = 0

        y_data = self.data.values()
        if not self.max_y: self.max_y = max(y_data)
        if not self.min_y: self.min_y = min(y_data)

        #   Calculate reasonable division for y-axis        
        if not self.div_y:
            span_y = self.max_y - self.min_y
            self.div_y = math.pow(10, int(math.log(max([self.max_y, -self.min_y]), 10)))
            if span_y/self.div_y > 4:
                self.div_y *= 2
            elif span_y/self.div_y < 3:
                self.div_y *= 0.5

        self.y_divisions = [y*self.div_y for y in range(-int(math.ceil(-self.min_y / self.div_y)), int(math.ceil(self.max_y / self.div_y))+1)]

    def _plotData(self):
        bar_width = (self.chart_width - self.gap_width) * 1.0 / len(self.data)
        bar_group = self.addChildElement('g', {'transform': 'translate(%d %d) scale(1, -1)' % (self.origin_x, self.attributes['height'] - self.origin_y)})
        
        for n, value in enumerate(self.data.values()):
            bar_group.addChildElement('rect',
                                     {'class': 'bar',
                                      'x': self.gap_width + n*bar_width,
                                      'y': 0,
                                      'width': bar_width-self.gap_width,
                                      'height': value})


if __name__ == '__main__':
    g = BarGraph({'width':500, 'height':300})

    g.addStyle('.background', {'fill': '#eee'})
    g.x_axis_label = "Subjects"
    g.y_axis_label = "Sentence / Video"

    g.addDataFromFile('sentence_counts.txt')
    g.outputToFile("test")
