"""
Functions that creates the tables and the visual display pages.
"""

from __future__ import (absolute_import, division, print_function)
from collections import OrderedDict
import copy
import logging
import os
import pandas as pd
import pypandoc

from fitbenchmarking.resproc import visual_pages
from fitbenchmarking.utils import create_dirs
from fitbenchmarking.utils.logging_setup import logger

# Some naming conventions for the output files
FILENAME_SUFFIX_ACCURACY = 'acc'
FILENAME_SUFFIX_RUNTIME = 'runtime'


def save_results_tables(options, results, group_name):
    """
    Saves the results of the fitting to html/rst tables.

    :param options : The options used in the fitting problem and plotting
    :type options : fitbenchmarking.utils.options.Options
    :param results : results nested array of objects
    :type results : list[list[list]]
    :param group_name : name of the problem group
    :type group_name : str
    """

    software = options.software
    if not isinstance(software, list):
        software = [software]
    minimizers = [options.minimizers[s] for s in software]
    minimizers = sum(minimizers, [])

    results_dir = options.results_dir
    use_errors = options.use_errors

    weighted_str = 'weighted' if use_errors else 'unweighted'

    tables_dir = create_dirs.restables_dir(results_dir, group_name)
    linked_problems = \
        visual_pages.create_linked_probs(results, group_name, results_dir)

    table_suffix = [FILENAME_SUFFIX_ACCURACY, FILENAME_SUFFIX_RUNTIME]
    table_names = []
    for suffix in table_suffix:
        table_names.append(os.path.join(tables_dir,
                                        '{0}_{1}_{2}_table.'.format(
                                            group_name,
                                            suffix,
                                            weighted_str)))
    generate_tables(results, minimizers,
                    linked_problems, table_names,
                    table_suffix)

    logging.shutdown()


def generate_tables(results_per_test, minimizers,
                    linked_problems, table_names,
                    table_suffix):
    """
    Generates accuracy and runtime tables, with both normalised and absolute
    results, and summary tables in both rst and html.

    :param results_per_test : results nested array of objects
    :type results_per_test : list[list[list]]
    :param minimizers : array with minimizer names
    :type minimizers : list
    :param linked_problems : rst links for supporting pages
    :type linked_problems : list[str]
    :param table_name : list of table names
    :type table_name : list
    :param table_suffix : set output to be runtime or accuracy table
    :type table_suffix : str
    """

    results_dict, html_links = create_results_dict(results_per_test,
                                                   linked_problems)
    preproccess_data(results_dict)
    table = create_pandas_dataframe(results_dict, minimizers, table_suffix)
    render_pandas_dataframe(table, minimizers, html_links, table_names)


def create_results_dict(results_per_test, linked_problems):
    """
    Generates a dictionary used to create HTML and RST tables.

    :param results_per_test : results nested array of objects
    :type results_per_test : list[list[list]]
    :param linked_problems : rst links for supporting pages
    :type linked_problems : list[str]

    :return : tuple(results, html_links)
               dictionary of results objects and
               html links for rending
    :rtype : tuple(dict, list)
    """

    count = 1
    prev_name = ''
    template = '<a target="_blank" href="{0}">{1}</a>'
    results = OrderedDict()
    html_links = []

    for prob_results, link in zip(results_per_test, linked_problems):
        name = prob_results[0].problem.name
        if name == prev_name:
            count += 1
        else:
            count = 1
        prev_name = name
        prob_name = name + ' ' + str(count)
        url = link.split('<')[1].split('>')[0]
        html_links.append(template.format(url, prob_name))
        results[prob_name] = [result for result in prob_results]
    return results, html_links


def preproccess_data(data):
    """
    Helper function that preprocesses data into the right format for printing

    :param data: dictionary of results objects
    :type data: dict
    """
    for results in data.values():
        min_chi_sq = min([r.chi_sq for r in results])
        min_runtime = min([r.runtime for r in results])
        for r in results:
            r.min_chi_sq = min_chi_sq
            r.min_runtime = min_runtime
            r.set_normalised_data()
            r.set_colour_scale()


def create_pandas_dataframe(table_data, minimizers, table_suffix):
    """
    Generates pandas data frame.

    :param table_data : dictionary containing results, i.e.,
                            {'prob1': [result1, result2, ...],
                             'prob2': [result1, result2, ...], ...}
    :type table_data : dict
    :param minimizers : list of minimizers (column headers)
    :type minimizers : list
    :param table_suffix : set output to be runtime or accuracy table
    :type table_suffix : list


    :return : dict(tbl, tbl_norm, tbl_combined) dictionary of
               pandas DataFrames containing results.
    :rtype : dict{pandas DataFrame, pandas DataFrame}
    """

    # This function is only used in the mapping, hence, it is defined here.
    def select_table(value, table_suffix):
        '''
        Selects either accuracy or runtime table.
        '''
        value.table_type = table_suffix
        value = copy.copy(value)
        return value

    tbl = pd.DataFrame.from_dict(table_data, orient='index')
    tbl.columns = minimizers
    results = {}
    for suffix in table_suffix:
        results[suffix] = tbl.applymap(lambda x: select_table(x, suffix))
    return results


def render_pandas_dataframe(table_dict, minimizers, html_links, table_names):
    """
    Generates html and rst page from pandas dataframes.

    :param table_dict : dictionary of DataFrame of the results
    :type table_dict : dict(pandas DataFrame, ...)
    :param minimizers : list of minimizers (column headers)
    :type minimizers : list
    :param html_links : html links used in pandas rendering
    :type html_links : list
    :param table_names : list of table names
    :type table_names : list
    """

    def colour_highlight(value):
        '''
        Colour mapping for visualisation of table
        '''
        colour = value.colour

        return 'background-color: {0}'.format(colour)

    for name, table in zip(table_names, table_dict.values()):
        table.index = html_links
        table_style = table.style.applymap(colour_highlight)
        with open(name + 'html', "w") as f:
            f.write(table_style.render())

        # pypandoc can be installed without pandoc
        try:
            output = pypandoc.convert_file(name + 'html', 'rst')
            with open(name + 'rst', "w") as f:
                f.write(output)
        except ImportError:
            print('RST tables require Pandoc to be installed')
