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
    max_value = max(item[1] for item in data)
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

    for i, (name, value) in enumerate(data):
        y = round(y_scale(value))
        bars.add('rect', { 'x': bar_x, 'y': y, 'width': bar_width, 'height': y2 - y })

        if bar_width > 20 or i % 2:
            bar_labels.add('text', { 'x': bar_x + bar_width / 2, 'y': y2 + 6}, name)

        bar_x += bar_width + gap

    # Draw axes
    path = 'M{} {} H{}'.format(x1 - 0.5, y2 + 0.5, x2)
    svg.add('path', { 'd': path, 'class': 'axis' })

    return svg


if __name__ == '__main__':
    data = {
        'the': 6.17,
        'and': 3.02,
        'of': 2.94,
        'to': 2.87,
        'a': 2.52,
        'in': 2.05,
        'that': 1.45,
        'i': 1.16,
        'it': 1.09,
        'is': 1.04,
    }
    # Sort by value
    sorted_data = [item for item in sorted(data.items(), key=lambda item: -item[1])]

    data = {3: 78568162, 2: 64014624, 1: 13726939, 4: 67147137, 5: 42197602, 6: 30494576, 7: 27318266, 9: 12919188, 8: 19025650, 10: 8444737, 11: 4575234, 13: 1340132, 14: 499104, 12: 2404650, 15: 130590, 16: 33624, 17: 11537, 18: 1425, 19: 121, 20: 16, 21: 5}
    data = { key: value * 100.0 / 372853319 for key, value in data.items() }
    # Sort by key
    sorted_data = [item for item in sorted(data.items(), key=lambda item: item[0])]

    svg = create_bar_chart(sorted_data)
    svg.write('test.svg')
