from math import pow, floor

import drawSVG
from utils import get_max_divisions, get_tick_size


def create_bar_chart(data, width=300, height=200, x_axis_label=None, y_axis_label=None):
    svg = drawSVG.SVG({
        'viewBox': "0 0 {} {}".format(width, height)
    })

    padding_top = 10
    padding_right = 1
    padding_left = 50
    padding_base = 40

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
    svg.addStyle('.dots circle', { 'fill': '#888', 'opacity': '0.6' })
    svg.addStyle('.bars rect:hover', { 'fill': 'rgb(255, 0, 175)', 'opacity': '0.95' })

    # Create groups for adding elements to
    gridlines = svg.add('g', { 'class': 'gridlines' })
    dots = svg.add('g', { 'class': 'dots' })
    tick_labels_y = svg.add('g', { 'class': 'tick-labels tick-labels-y' })
    bar_labels = svg.add('g', { 'class': 'tick-labels tick-labels-x' })

    # Draw gridlines and y-axis labels
    min_value = min(min(item['values']) for item in data)
    max_value = max(max(item['values']) for item in data)

    # Calculate tick size and number
    tick_size, min_value, max_value = get_tick_size(min_value, max_value, 8)
    num_ticks = int(round((max_value * 1.05 - min_value) / tick_size))

    y_scale = lambda y: y2 - graph_height * (y - min_value) / (max_value - min_value)

    for i in range(0, num_ticks + 1):
        value = min_value + i * tick_size
        y = round(y_scale(value)) - 0.5

        print(value, y)

        if i > 0:
            gridlines.add('path', { 'd': "M{} {}H{}".format(x1, y, x2) })
        tick_labels_y.add('text', { 'x': x1 - 4, 'y': y }, "{0:.0f}".format(value))

    # Add y-axis label
    if y_axis_label:
        transform = "translate({} {}) rotate(-90)".format(2, (y2 - y_scale (num_ticks * tick_size)) / 2)
        svg.add('text', { 'class': 'y-axis-label', 'transform': transform }, y_axis_label)

    # Add x-axis label
    if x_axis_label:
        svg.add('text', { 'class': 'tick-labels-x', 'x': (x1 + x2) / 2, 'y': height - 16 }, x_axis_label)

    # Add bars
    gap = 1
    r = 5
    bar_width = floor((graph_width - 4) / len(data))
    bar_x = x1 + (graph_width - bar_width * len(data)) / 2 + bar_width / 2
    bar_width -= gap

    for i, item in enumerate(data):
        for value in item['values']:
            y = round(y_scale(value))
            dots.add('circle', { 'cx': bar_x, 'cy': y, 'r': r })

        if bar_width > 20 or i % 2:
            bar_labels.add('text', { 'x': bar_x, 'y': y2 + 6}, item['name'])

        bar_x += bar_width + gap

    # Draw axes
    path = 'M{} {} H{}'.format(x1 - 0.5, y2 + 0.5, x2)
    svg.add('path', { 'd': path, 'class': 'axis' })

    return svg


if __name__ == '__main__':
    data = [
        {
            'name': 'bl*nder',
            'values': [19, 1977, 107, 64, 602],
            'labels': ['a', 'e', 'i', 'o', 'i']
        }, {
            'name': 'b*lling',
            'values': [95, 22, 1898, 117, 21],
            'labels': ['a', 'e', 'i', 'o', 'u']
        }, {
            'name': 'p*tting',
            'values': [1062, 528, 536, 437, 31110],
            'labels': ['a', 'e', 'i', 'o', 'u']
        },
    ]

    data = [
        {
            'name': 'bl*nder',
            'values': [-16.8, -12.1, -15.1, -15.6, -13.3],
            'labels': ['a', 'e', 'i', 'o', 'i']
        }, {
            'name': 'b*lling',
            'values': [-15.2, -16.6, -12.2, -15.0, -16.7],
            'labels': ['a', 'e', 'i', 'o', 'u']
        }, {
            'name': 'p*tting',
            'values': [-12.8, -13.5, -13.5, -13.7, -9.4],
            'labels': ['a', 'e', 'i', 'o', 'u']
        },
    ]

    svg = create_bar_chart(
        data,
        height=225,
        x_axis_label="Letter",
        y_axis_label="Count"
    )

    svg.write('test.svg')
