import os
import sys
import math
from drawSVG import SVG

#       *** To Do **
#   Don't plot lines that exceed a given min or max
#   Add commandline interface that allows options to be set
#   Fix axis positions for numbers < 0
#   Fix axis divisions for numbers < 1
#   Fix alignment when y-axis values are negatives or floats
#   Add tick marks to axes
#   Add data labels - with mouseover?
#   Fix text alignments when using different font-sizes?
#   Add series markers

class Graph(SVG):
    """ Plots series of (x,y) data on a SVG line graph. """
    
    def __init__(self, attributes=None):
        SVG.__init__(self, attributes)
        
        self.data = {}
        self.series = []
        self.colours = ['#0060e5', '#001060', '#e52060', '#a00030', '#00c020', '#006010']
        
        self.left_pad  = 10.5
        self.right_pad = 16.5
        self.upper_pad = 10.5
        self.lower_pad = 10.5
        self.origin_x = self.left_pad
        self.origin_y = self.lower_pad
        
        # Set default values if not already defined
        self.attributes['width'] = self.attributes.get('width', 600)
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
        
        # These are automatically generated based on the data but can be overriden before plotting data
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
        self.addStyle('.x-axis-text', {'text-anchor': 'middle'})
        self.addStyle('.gridlines', {'stroke':'black', 'stroke-width':0.5, 'fill':'none', 'opacity':0.5})
        self.addStyle('.data-series', {'stroke-width':1, 'fill':'none', 'opacity':1})

    def addData(self, series_dict):
        """ Add a dictionary of data in the form of series_dict[name] = list_of_data. """
        
        for series_name, series_data in series_dict.items():
            self.series.append(series_name)
            self.data[series_name] = series_data
        
    def addDataFromFile(self, filename):
        """ Read in a tab-delimited file with a heading row and add to self.data dictionary """
    
        try:
            fin = open(filename, 'r')
        except IOError:
            print "Could not open file", filename
            return
        
        self.series = fin.readline().rstrip().split('\t')
        for h in self.series:
            self.data[h] = []
        
        for line in fin.readlines():
            temp = line.rstrip('\n').split('\t')
            for i, h in enumerate(self.series):
                self.data[h].append(float(temp[i]))
        
    def plot(self, *args):
        """ Given a list of series' names, plots those series with x values equal data indices i.e. 0 to len(data)-1. """
    
        if not len(args):
            y_series = self.series
        else:
            y_series = args
            
        x_series = range(max(len(self.data[series]) for series in self.series))
        self._createGraph(x_series, y_series)
        
    def plotXonY(self, x_series, *args):
        """ Given a list plots the first item in the list against all subsequent items in the list
            If not argument is passed then it plots the series """
    
        if not len(args):
            y_series = [series for series in self.series if series != x_series]
        else:
            y_series = args
        
        self._createGraph(self.data[x_series], y_series)

    def _createGraph(self, x_series, y_series):
        x_divisions, x_to_string = self._calculateDivisions(x_series, self.min_x, self.max_x, self.div_x)
        
        y_min = min(min(self.data[series]) for series in y_series)
        y_max = max(max(self.data[series]) for series in y_series)
        y_divisions, y_to_string = self._calculateDivisions([y_min, y_max], self.min_y, self.max_y, self.div_y)
        
        self._determinePlottingFunctions(x_divisions, y_divisions, y_to_string)
        self._addBackground()
        self._addAxes()
        self._drawAxisUnits(x_divisions, y_divisions, x_to_string, y_to_string)
        self._drawGridlines(x_divisions, y_divisions)
        
        for i, series in enumerate(y_series):
            self._plotData(x_series, self.data[series], i)

    def _calculateDivisions(self, data, d_min=None, d_max=None, d_div=None):
        """ Calculate a reasonable way to divide data for gridlines and units """
        
        if d_min is None:
            d_min = min(data)
        if d_max is None:
            d_max = max(data)
            
        if not d_div:
            d_div = math.pow(10, int(math.log(max([d_max, -d_min]), 10)))
            if d_max/d_div > 5:
                d_div *= 2
            elif d_max/d_div < 1:
                d_div *= 0.2
            elif d_max/d_div < 3:
                d_div *= 0.5
                
        magnitude = math.floor(math.log(d_div, 10))
        if magnitude < 0:
            to_string = '%%.%df' % (-magnitude)
        else:
            to_string = '%d'
        
        divisions = [n * d_div for n in range(-int(math.ceil(-d_min / d_div)), int(math.ceil(d_max / d_div))+1)]
        
        return divisions, to_string

    def _determinePlottingFunctions(self, x_divisions, y_divisions, y_to_string):
        """ Find where origin of graph should start and determine mapping from data to that region """
        
        # Make space for label if required
        if self.x_axis_label:
            self.origin_y += 20
        if self.y_axis_label:
            self.origin_x += 20
        
        # Make space for units if required
        if self.x_axis_units:
            self.origin_y += 12
        if self.y_axis_units:
            self.origin_x += 5 * max(len(y_to_string % y) for y in y_divisions)
            
        self.chart_width  = self.attributes['width'] - self.right_pad - self.origin_x
        self.chart_height = self.attributes['height'] - self.upper_pad - self.origin_y
        x_scaling_factor = self.chart_width  * 1.0 / (x_divisions[-1] - x_divisions[0])
        y_scaling_factor = self.chart_height * 1.0 / (y_divisions[-1] - y_divisions[0])
        
        # Functions for converting x and y values into coordinates on the SVG
        self.f_x = lambda x: self.origin_x + x_scaling_factor * (x - x_divisions[0])
        self.f_y = lambda y: self.attributes['height'] - self.origin_y - y_scaling_factor * (y - y_divisions[0])

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
                                {'class':'axis-label',
                                 'x': x,
                                 'y': y},
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

    def _drawAxisUnits(self, x_divisions, y_divisions, x_to_string, y_to_string):
        if self.x_axis_units or self.y_axis_units:
            axis_group = self.addChildElement('g', {'class': 'axis-units'})
    
        if self.x_axis_units:
            x_group = axis_group.addChildElement('g', {'class': 'x-axis-text'})

            for x in x_divisions:
                x_group.addChildElement('text', {'x': self.f_x(x), 'y': self.attributes['height'] - self.origin_y+12}, x_to_string % x)
        
        if self.y_axis_units:
            y_group = axis_group.addChildElement('g', {'class': 'y-axis-text'})
            
            for y in y_divisions:
                y_group.addChildElement('text', {'x': self.origin_x-3, 'y': self.f_y(y)+3}, y_to_string % y)

    def _drawGridlines(self, x_divisions, y_divisions):
        if self.x_gridlines or self.y_gridlines:
            gridline_group = self.addChildElement('g', {'class': 'gridlines'})

        if self.x_gridlines:
            for x in x_divisions[1:-1]:
                gridline_x = int(self.f_x(x)) + 0.5
                gridline_group.addChildElement('line',
                                               {'x1': gridline_x,
                                                'y1': self.attributes['height'] - self.origin_y,
                                                'x2': gridline_x,
                                                'y2': self.attributes['height'] - self.origin_y - self.chart_height})

        if self.y_gridlines:
            for y in y_divisions[1:-1]:
                gridline_y = int(self.f_y(y)) + 0.5
                gridline_group.addChildElement('line',
                                               {'x1': self.origin_x,
                                                'y1': gridline_y,
                                                'x2': self.origin_x + self.chart_width,
                                                'y2': gridline_y})

    def _plotData(self, x_data, y_data, series_n):
        """ Create <path> of straight lines for each series of data """
       
        # Filter data to prevent plotting lines < 1 px long
        data_bins = int(len(x_data)/self.chart_width)
        if data_bins > 1:
            y_data = [float(sum(y_data[n*data_bins:(n+1)*data_bins]))/data_bins for n in range(len(y_data)/data_bins)]
            x_data = [float(sum(x_data[n*data_bins:(n+1)*data_bins]))/data_bins for n in range(len(x_data)/data_bins)]

        # Filter to prevent drawing lines that exceed boundaries
        
        path = 'M' + ' '.join('%.1f,%.1f' % (self.f_x(x), self.f_y(y)) for x, y in zip(x_data, y_data))
        self.addChildElement('path', {'class': 'data-series', 'stroke': self.colours[series_n], 'd': path})

class BarGraph(Graph):
    """ Plots a horizontal bar chart. """

    def __init__(self, attributes=None):
        Graph.__init__(self, attributes)
        
        self.x_gridlines = False
        self.x_axis_units = False
        self.gap_width = 2

        self.addStyle('.bar', {'fill': '#aaa', 'opacity': 0.7})
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
            self.series.append(key)
            self.data[key] = float(value)

    def plot(self):
        x_divisions = self._calculateDivisions(range(len(self.series)), self.min_x, self.max_x, self.div_x)
        y_divisions = self._calculateDivisions(self.data.values(), self.min_y, self.max_y, self.div_y)
        
        self._determinePlottingFunctions(x_divisions, y_divisions)
        self._addBackground()
        self._addAxes()
        self._drawAxisUnits(x_divisions, y_divisions)
        self._drawGridlines(x_divisions, y_divisions)
        self._plotData(x_divisions, y_divisions)

    def _calculateDivisions(self, data, d_min=None, d_max=None, d_div=None):

        if d_min is None:
            d_min = min(data)
        if d_max is None:
            d_max = max(data)

        if not d_div:
            d_div = math.pow(10, int(math.log(max([d_max, -d_min]), 10)))
            if d_max/d_div > 5:
                d_div *= 2
            elif d_max/d_div < 3:
                d_div *= 0.5
                
        divisions = [n * d_div for n in range(-int(math.ceil(-d_min / d_div)), int(math.ceil(d_max / d_div))+1)]
        
        return divisions

    def _plotData(self, x_divisions, y_divisions):
        bar_width = (self.chart_width - self.gap_width) * 1.0 / len(self.data)
        scale = self.chart_height * 1.0 / (y_divisions[-1] - y_divisions[0])
        bar_group = self.addChildElement('g',
                                        {'transform': 'translate(%d %d) scale(1, -%.3f)' % (self.origin_x, self.attributes['height'] - self.origin_y, scale)})
        
        for n, bar in enumerate(self.series):
            bar_group.addChildElement('rect',
                                     {'class': 'bar',
                                      'x': n*bar_width + self.gap_width,
                                      'y': 0,
                                      'width': bar_width - self.gap_width,
                                      'height': self.data[bar]})


if __name__ == '__main__':
    if len(sys.argv) > 1:
        g = Graph()
        g.addDataFromFile(sys.argv[1])
        g.plot()
        
        if len(sys.argv) > 2:
            g.outputToFile(sys.argv[2])
        else:
            g.outputToFile(os.path.splitext(sys.argv[1])[0])
