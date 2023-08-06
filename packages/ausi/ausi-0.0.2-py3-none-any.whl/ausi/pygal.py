import pandas as pd
import pygal


def create_xy_chart(df, group_key, x="x", y="y"):
    plot_data = pd.DataFrame(index=df[group_key])
    plot_data['value'] = tuple(zip(df[x], df[y]))
    plot_data['label'] = df.index
    plot_data['data'] = plot_data[['label', 'value']].to_dict('records')
    plot_dict = plot_data.groupby(plot_data.index).data.apply(list)

    xy_chart = pygal.XY(stroke=False)
    [xy_chart.add(entry[0], entry[1]) for entry in plot_dict.iteritems()]
    return xy_chart


def create_stacked_line(df):
    line_chart = pygal.StackedLine(fill=True, margin=100)
    line_chart.x_labels = df.index.astype(str)

    data = df.T.apply(list, axis=1)
    for entry in data.iteritems():
        line_chart.add(entry[0], entry[1])
    return line_chart


def create_indent_treemap(df):
    plot_data = pd.DataFrame(index=df.index)
    plot_data['value'] = df['lines']
    plot_data['relative_changes'] = df['changes'] / df['changes'].max()
    plot_data['color_alpha'] = df['ratio'] / df['ratio'].max()
    plot_data['label'] = df.index.str.split("/").str[-1] + \
						 '(l: ' + df['lines'].apply(str) + \
						 ', i: ' + df['indents'].apply(str) + \
						 ', r: ' + df['ratio'].apply('{:.2f}'.format) + \
						 ', c: ' + df['changes'].apply(str) + ')'
    plot_data['style'] = \
        plot_data['color_alpha'].apply(lambda x: 'fill: rgba(255,0,0,' + str(x) + '); ') + \
        plot_data['relative_changes'].apply(lambda x: 'stroke: rgba(0,0,0,' + str(x) + '); ') + \
        plot_data['relative_changes'].apply(lambda x: 'stroke-width: ' + str(10 * x) + ');')

    plot_data['data'] = plot_data.to_dict('records')
    plot_dict = plot_data.groupby(plot_data.index)['data'].apply(list)

    config = pygal.Config(show_legend=False)
    treemap = pygal.Treemap(config)
    [treemap.add(entry[0], entry[1]) for entry in plot_dict.iteritems()]
    return treemap
