# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style('ticks', {'axis.grid': True,})


def run():
    n_sims = 10000

    pass

    # fig, ax = plt.subplots(figsize=(3.94, 2.76))
    # ax.plot(list_S, [i/1000. for i in list_Q])
    #
    # ax.set_ylabel('Permissible fire load [MW]')
    # ax.set_xlabel('Separation distance between combustibles\n and wall with windows [m]')
    # ax.set_xticks(ticks=np.arange(0, 10 + 0.001, 1))
    # ax.set_yticks(ticks=np.arange(0, 20 + 0.001, 2))
    # ax.grid(color='grey', linestyle='--', linewidth=.5)
    # ax.legend().set_visible(False)
    # # ax.legend(prop={'size': 7})
    # fig.tight_layout()
    # plt.show()
    # fig.savefig(
    #     'test.png',
    #     transparent=True,
    #     bbox_inches='tight',
    #     dpi=300
    # )