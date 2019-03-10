from math import pow, floor, log10

import drawSVG
from examples.results_to_graph import results
from utils import get_max_divisions, get_tick_size


def create_bar_chart(data, width=300, height=200, **kwargs):
    svg = drawSVG.SVG({
        'viewBox': "0 0 {} {}".format(width, height)
    })

    padding_top = 10
    padding_right = 1
    padding_left = 65
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
    svg.addStyle('.bars text, .tick-labels', { 'font-size': '0.9rem' })
    svg.addStyle('.tick-labels-y', { 'text-anchor': 'end', 'dominant-baseline': 'middle' })
    svg.addStyle('.bars text, .tick-labels-x', { 'text-anchor': 'middle', 'dominant-baseline': 'hanging' })
    svg.addStyle('.y-axis-label', { 'text-anchor': 'middle', 'dominant-baseline': 'hanging' })
    svg.addStyle('.bars rect', { 'fill': '#888', 'opacity': '0.6' })
    svg.addStyle('.bars text', { 'cursor': 'default' })
    svg.addStyle('.bars g:hover *', { 'fill': 'rgb(255, 0, 175)', 'opacity': '0.95' })

    svg.addStyle('.bars g text.hidden-value', { 'dominant-baseline': 'alphabetic', 'visibility': 'hidden', 'font-size': '0.7rem' })
    svg.addStyle('.bars g:hover text.hidden-value', { 'visibility': 'visible', 'fill': 'black', 'cursor': 'default' })

    # Create groups for adding elements to
    gridlines = svg.add('g', { 'class': 'gridlines' })
    bars = svg.add('g', { 'class': 'bars' })
    tick_labels_y = svg.add('g', { 'class': 'tick-labels tick-labels-y' })

    # Draw gridlines and y-axis labels
    min_value = 0
    max_value = max(item[1] for item in data)

    tick_size, min_value, max_value = get_tick_size(min_value, max_value, 8)
    num_ticks = int(round((max_value * 1.05 - min_value) / tick_size))

    y_scale = lambda y: y2 - graph_height * y / max_value

    for i in range(0, num_ticks + 1):
        value = i * tick_size
        y = round(y_scale(value)) - 0.5

        if i > 0:
            gridlines.add('path', { 'd': "M{} {}H{}".format(x1, y, x2) })

        if kwargs.get('format_y_ticks'):
            value = kwargs['format_y_ticks'](value)

        tick_labels_y.add('text', { 'x': x1 - 4, 'y': y }, value)

    # Add y-axis label
    y_axis_label = kwargs.get('y_axis_label')
    if y_axis_label:
        transform = "translate({} {}) rotate(-90)".format(2, (y_scale(num_ticks * tick_size / 2)))
        svg.add('text', { 'class': 'y-axis-label', 'transform': transform }, y_axis_label)

    # Add x-axis label
    x_axis_label = kwargs.get('y_axis_label')
    if x_axis_label:
        svg.add('text', { 'class': 'tick-labels-x', 'x': (x1 + x2) / 2, 'y': height - 16 }, x_axis_label)

    # Add bars
    gap = 1
    bar_width = floor((graph_width - 4) / len(data))
    bar_x = x1 + (graph_width - bar_width * len(data)) / 2
    bar_width -= gap

    for i, (name, value) in enumerate(data):
        y = round(y_scale(value))
        group = bars.add('g', { 'class': 'bar-group' })
        group.add('rect', { 'x': bar_x, 'y': y, 'width': bar_width, 'height': y2 - y })

        # if bar_width > 20 or i % 2:
        group.add('text', { 'x': bar_x + bar_width / 2, 'y': y2 + 6}, name)

        if kwargs.get('format_bar_value'):
            value = kwargs['format_bar_value'](value)
        group.add('text', { 'class': 'hidden-value', 'x': bar_x + bar_width / 2, 'y': y - 2}, value)

        bar_x += bar_width + gap

    # Draw axes
    path = 'M{} {} H{}'.format(x1 - 0.5, y2 + 0.5, x2)
    svg.add('path', { 'd': path, 'class': 'axis' })

    return svg


if __name__ == '__main__':
    data = results['ratio of starting to ending frequency']
    data = results['the x word']
    data = results['proportions_of_letters_that_can_be_replaced']
    data = results['number of times a letter can be swapped']

    # Sort by value
    sorted_data = [item for item in sorted(data.items(), key=lambda item: -item[1])]

    # Sort by key
    # sorted_data = [item for item in sorted(data.items(), key=lambda item: item[0])]

    # Divide by a million
    # sorted_data = [(item[0], item[1] / 1000000) for item in sorted_data]

    # The logarithm
    # sorted_data = [(item[0], log10(item[1])) for item in sorted_data]

    svg = create_bar_chart(
        sorted_data,
        width=800,
        height=250,
        x_axis_label="Letter",
        y_axis_label="Number of swaps",
        format_y_ticks=lambda x: "{:d}".format(x)
    )

    svg.write('test.svg')
