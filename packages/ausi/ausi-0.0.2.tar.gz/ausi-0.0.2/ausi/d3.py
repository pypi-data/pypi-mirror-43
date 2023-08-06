import pandas as pd
import json
import html
import os
import numpy as np
from matplotlib import cm
from matplotlib.colors import rgb2hex
import pkg_resources


JSON_FILE_MARKER = "JSON_FILE_MARKER"


def create_json_file_name(output_file_name_prefix):
    json_file_name = output_file_name_prefix + ".json"
    return json_file_name


def create_visualization_html_from_template(visualization_type, output_file_name_prefix):
    resource_package = __name__
    resource_path = '/'.join(('d3_templates', visualization_type, 'template.html'))
    template = pkg_resources.resource_string(resource_package, resource_path)
    html_file = output_file_name_prefix + ".html"
    with open(html_file, mode='w', encoding='utf-8') as d3_file:
        html_as_string = template.decode("utf-8")
        html_as_string = html_as_string.replace("JSON_FILE_MARKER", create_json_file_name(output_file_name_prefix))
        d3_file.write(html_as_string)
    print("HTML file produced in '{}'".format(os.path.abspath(html_file)))


def create_json_file(json_data, output_file_name_prefix):
    json_file_name = create_json_file_name(output_file_name_prefix)
    json_string = json.dumps(json_data, indent=3)
    json_string = json_string.strip().replace("null", "")

    with open(json_file_name, mode='w', encoding='utf-8') as json_file:
        json_file.write(json_string)
    print("JSON file produced in '{}'".format(os.path.abspath(json_file_name)))


def escape_name(name):
        return html.escape(name.replace("$", "_innerClass_"))


def create_json_for_links(df, from_col, to_col, value_col=None):

    deps = df[[from_col, to_col]]
    if value_col:
        deps['value'] = df[value_col]
    # some algorithms need to have all target dependencies also on the source side
    additional_deps = pd.DataFrame()
    additional_deps['from'] = df[~df[to_col].isin(df[from_col])][to_col].unique()
    additional_deps['to'] = pd.np.nan
    all_deps = pd.concat([deps, additional_deps], ignore_index=True, sort=True)
    links = all_deps.dropna().copy()
    links['from'] = links['from'].apply(escape_name)
    links['to'] = links['to'].apply(escape_name)
    links.rename(columns={
        from_col: "source",
        to_col: "target"}, inplace=True)
    links_json = json.loads(links.to_json(orient='table', index=False))['data']
    return links_json


def create_json_for_nodes(df, from_col, group_col, to_col):
    from_nodes = df[[from_col]].copy()
    to_nodes = df[[to_col]].copy()
    to_nodes.rename(columns={to_col: from_col}, inplace=True)
    if group_col:
        # set optional group for colorizing a group of nodes that belong together somehow
        from_nodes['group'] = pd.factorize(df[group_col])[0]
        to_nodes['group'] = pd.factorize(df[group_col])[0]
    all_nodes = pd.concat([from_nodes, to_nodes], sort=False).drop_duplicates()
    nodes = pd.DataFrame(index=all_nodes.index)
    nodes['id'] = all_nodes[from_col].apply(escape_name)
    if group_col:
        nodes['group'] = all_nodes['group']
    nodes = nodes.drop_duplicates(subset=["id"])
    # we need to escape the $ sign because d3 can't handle this. $ signs are used by Java inner classes
    nodes = nodes.set_index('id')
    nodes_json = json.loads(nodes.to_json(orient='table'))['data']
    return nodes_json


def create_d3force(df, output_file_name_prefix, from_col="from", to_col="to", group_col=None, value_col=None):

    nodes_json = create_json_for_nodes(df, from_col, group_col, to_col)
    links_json = create_json_for_links(df, from_col, to_col, value_col)
    json_data = {'nodes': nodes_json, 'links': links_json}
    create_json_file(json_data, output_file_name_prefix)
    create_visualization_html_from_template('d3-force', output_file_name_prefix)


def create_json_nodes_imports(df, from_col = 'from', to_col='to'):

    deps = df.copy()
    deps[from_col] = deps[from_col].apply(escape_name)
    deps[to_col] = deps[to_col].apply(escape_name)
    additional_deps = pd.DataFrame()
    additional_deps[from_col] = deps[~deps[to_col].isin(deps[from_col])][to_col].unique()
    additional_deps[to_col] = pd.np.nan
    all_deps = pd.concat([deps[[from_col, to_col]], additional_deps], ignore_index=True)
    imports = all_deps.groupby(from_col)[[to_col]].agg(list)
    imports.rename(columns={ "to" : "chapters"}, inplace=True)
    imports.index.name = "id"
    imports.index = imports.index.map(escape_name)
    imports['name'] = imports.index
    json_data = json.loads(imports.to_json(orient='table'))['data']
    return json_data


def create_semantic_substrate(df, output_file_name_prefix, from_col="from", to_col="to"):

    nodes_import_json = create_json_nodes_imports(df, from_col, to_col)
    links_json = create_json_for_links(df, from_col, to_col)
    for entry in links_json:
        entry['chapters'] = "list"

    json_data = {'nodes': nodes_import_json, 'links': links_json}
    create_json_file(json_data, output_file_name_prefix)
    create_visualization_html_from_template('semantic_substrate', output_file_name_prefix)
    return json_data


def create_json_for_zoomable_circle_packing(
        plot_data,
        column_to_color_name,
        join_color_column_name,
        hierarchy_column_name,
        hierarchy_column_name_separator,
        size_column_name,
        value_column_name,
        output_file_name_prefix,
        color_column_name='color'):
    # create unique colors per values in column
    colored_column = plot_data[[column_to_color_name]].drop_duplicates()
    # shuffle names to color because otherwise the colors for subsequent data would be too similar
    colored_column = colored_column.sample(frac=1, random_state=0)
    rgb_colors = [rgb2hex(x) for x in cm.Spectral(np.linspace(0, 1, len(colored_column)))]
    colored_column[color_column_name] = rgb_colors

    temp_color_column_name = '_XXX' + color_column_name
    # add colored column to plot_data
    colored_plot_data = pd.merge(
        plot_data, colored_column,
        left_on=join_color_column_name,
        right_on=column_to_color_name,
        how='left',
        suffixes=['', temp_color_column_name])
    colored_plot_data.loc[colored_plot_data[column_to_color_name] == 'None', color_column_name] = "white"
    colored_plot_data.rename(columns={ temp_color_column_name : "gen_color_code"})
    colored_plot_data.head()

    json_data = {'name': 'flare', 'children': []}

    for row in colored_plot_data.iterrows():
        series = row[1]
        path, filename = os.path.split(series[hierarchy_column_name])

        last_children = None
        children = json_data['children']

        for path_part in path.split(hierarchy_column_name_separator):
            entry = None

            for child in children:
                if "name" in child and child["name"] == path_part:
                    entry = child
            if not entry:
                entry = {}
                children.append(entry)

            entry['name'] = path_part
            if not 'children' in entry:
                entry['children'] = []

            children = entry['children']
            last_children = children

        last_children.append({
            'name': filename + " [" + series[join_color_column_name] + ", " + "{:6.2f}".format(
                series[value_column_name]) + "]",
            'ratio': series[value_column_name],
            'size': series[size_column_name],
            'color': series[color_column_name]})

    create_json_file(json_data, output_file_name_prefix)
    create_visualization_html_from_template('zoomable_circle_package', output_file_name_prefix)



