#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram

def plot_dendrogram(model, **kwargs):

    plt.figure(figsize=(5,60))
    children = model.children_
    distance = np.arange(children.shape[0])
    no_of_observations = np.arange(2, children.shape[0]+2)
    linkage_matrix = np.column_stack(
        [children, distance, no_of_observations]).astype(float)
    dendrogram(linkage_matrix, orientation='right', leaf_font_size=14, **kwargs)
    plt.show()