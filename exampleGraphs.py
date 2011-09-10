import drawSVGGraph

def barChart():
    my_svg = drawSVGGraph.BarGraph()
    my_svg.addData({'A':10, 'B':20, 'C':12})
    my_svg.min_y = 0
    my_svg.gap_width = 40
    my_svg.plot()
    return my_svg

my_svg = barChart()	
my_svg.outputToFile('test.svg')
