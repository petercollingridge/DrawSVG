import drawSVGGraph

def lineGraph():
    my_svg = drawSVGGraph.Graph()
    my_svg.addData({'A': [0.1, 0.16, 0.12, 0.05]})
    print my_svg.data
    my_svg.plot()
    return my_svg

def barChart():
    my_svg = drawSVGGraph.BarGraph()
    my_svg.addData({'A':10, 'B':20, 'C':12})
    my_svg.min_y = 0
    my_svg.gap_width = 40
    my_svg.plot()
    return my_svg

my_svg = lineGraph()	
my_svg.outputToFile('test.svg')
