import drawSVG
from math import floor, pow, log10


def get_max_divisions(position_1, position_2):
    return max(2, floor(abs(position_2 - position_1) / 25))

def getTickSize(start_value, end_value, max_divisions, min_unit=0):
    unit_value = max(min_unit, pow(10, floor(log10(end_value - start_value) - 1)))

    #  Increase unit value only using nice numbers
    if unit_value < end_value / 20:
        unit_value *= 2
    if unit_value < end_value / 16:
        unit_value *= 1.25

    while unit_value < end_value / max_divisions:
        unit_value *= 2

    return unit_value


def create_bar_chart(data, width=300, height=200):
    svg = drawSVG.SVG({ 'width': width, 'height': height })

    padding_top = 2
    padding_right = 2
    padding_left = 38
    padding_base = 18

    x1 = padding_left
    x2 = width - padding_right
    y1 = padding_top
    y2 = height - padding_base
    graph_width = x2 - x1
    graph_height = y2 - y1

    svg.addStyle('.axis', { 'fill': 'none', 'stroke': 'black' })
    svg.addStyle('.gridlines', { 'fill': 'none', 'stroke': '#aaa' })

    # Draw gridlines
    gridlines = svg.add('g', { 'class': 'gridlines' })

    max_value = max(data.values())
    tick_size = getTickSize(0, max_value, 5)
    num_ticks = int(round(max_value / tick_size))

    y_scale = lambda y: y2 - graph_height * y / max_value

    for i in range(1, num_ticks):
        y = round(y_scale(i * tick_size)) - 0.5
        gridlines.add('path', { 'd': "M{} {}H{}".format(x1, y, x2) })

    # Draw axes
    path = 'M{} {} V{} H{}'.format(x1 - 0.5, y1, y2 + 0.5, x2)

    svg.add('path', { 'd': path, 'class': 'axis' })

    return svg


if __name__ == '__main__':
    data = {
        'the': 23014366,
        'and': 11260177,
        'of': 10968008,
        'to': 10691399,
        'a': 9392485,
        'in': 7661696,
        'that': 5416929,
        'i': 4334454,
        'it': 4062843,
        'is': 3878929,
    }

    svg = create_bar_chart(data)
    svg.write('test.svg')
