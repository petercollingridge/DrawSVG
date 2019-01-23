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
    svg = drawSVG.SVG({
        'width': width,
        'viewBox': "0 0 {} {}".format(width, height)
    })

    padding_top = 5
    padding_right = 2
    padding_left = 38
    padding_base = 20

    x1 = padding_left
    x2 = width - padding_right
    y1 = padding_top
    y2 = height - padding_base
    graph_width = x2 - x1
    graph_height = y2 - y1

    # Add styles
    svg.addStyle('.axis', { 'fill': 'none', 'stroke': 'black' })
    svg.addStyle('.gridlines', { 'fill': 'none', 'stroke': '#ccc' })
    svg.addStyle('.tick-labels', { 'font-size': '0.9rem' })
    svg.addStyle('.tick-labels-y', { 'text-anchor': 'end', 'dominant-baseline': 'middle' })
    svg.addStyle('.tick-labels-x', { 'text-anchor': 'middle', 'dominant-baseline': 'hanging' })
    svg.addStyle('.y-axis-label', { 'text-anchor': 'middle', 'dominant-baseline': 'hanging' })
    svg.addStyle('.bars rect', { 'fill': '#888', 'opacity': '0.6' })
    svg.addStyle('.bars rect:hover', { 'fill': 'rgb(255, 0, 175)', 'opacity': '0.95' })

    # Create groups for adding elements to
    gridlines = svg.add('g', { 'class': 'gridlines' })
    bars = svg.add('g', { 'class': 'bars' })
    tick_labels_y = svg.add('g', { 'class': 'tick-labels tick-labels-y' })
    bar_labels = svg.add('g', { 'class': 'tick-labels tick-labels-x' })

    # Draw gridlines and y-axis labels
    max_value = max(data.values())
    tick_size = getTickSize(0, max_value, 8)
    num_ticks = int(round(0.5 + max_value / tick_size))
    y_scale = lambda y: y2 - graph_height * y / max_value

    for i in range(0, num_ticks):
        value = i * tick_size
        y = round(y_scale(value)) - 0.5

        if i > 0:
            gridlines.add('path', { 'd': "M{} {}H{}".format(x1, y, x2) })
        tick_labels_y.add('text', { 'x': x1 - 4, 'y': y }, "{0:.0f}".format(value))

    # Add y-axis label
    transform = "translate({} {}) rotate(-90)".format(2, (y2 - y_scale (num_ticks * tick_size)) / 2)
    svg.add('text', { 'class': 'y-axis-label', 'transform': transform }, "Frequency (%)")

    # Add bars
    gap = 2
    bar_width = floor((graph_width - 4) / len(data))
    bar_x = x1 + (graph_width - bar_width * len(data)) / 2
    bar_width -= gap

    for name, value in sorted(data.items(), key=lambda item: -item[1]):
        y = round(y_scale(value))
        bars.add('rect', { 'x': bar_x, 'y': y, 'width': bar_width, 'height': y2 - y })
        bar_labels.add('text', { 'x': bar_x + bar_width / 2, 'y': y2 + 6}, name)
        bar_x += bar_width + gap

    # Draw axes
    path = 'M{} {} H{}'.format(x1 - 0.5, y2 + 0.5, x2)
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

    percent_data = { key: value * 100.0 / 372853319 for key, value in data.items() }
    svg = create_bar_chart(percent_data)
    svg.write('test.svg')
