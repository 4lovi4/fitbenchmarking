"""
Fittng and utility functions for the scipy fitting algorithms.
"""
# Copyright &copy; 2016 ISIS Rutherford Appleton Laboratory, NScD
# Oak Ridge National Laboratory & European Spallation Source
#
# This file is part of Mantid.
# Mantid is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Mantid is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# File change history is stored at:
# <https://github.com/mantidproject/fitbenchmarking>.
# Code Documentation is available at: <http://doxygen.mantidproject.org>
from __future__ import (absolute_import, division, print_function)

from scipy.optimize import curve_fit
import numpy as np
import sys, re, copy, time

from fitting import misc
from fitting import mantid
from fitting.plotting import plot_helper
from utils.logging_setup import logger

MAX_FLOAT = sys.float_info.max

def benchmark(problem, data, function, minimizers, cost_function):

    min_chi_sq, best_fit = MAX_FLOAT, None
    results_problem = []

    for minimizer in minimizers:
        status, fitted_y, fin_function_def, runtime = \
        fit(data, function, minimizer, cost_function)
        chi_sq, min_chi_sq, best_fit = \
        chisq(status, data, fitted_y, min_chi_sq, best_fit)
        individual_result = \
        misc.create_result_entry(problem, status, chi_sq, runtime, minimizer,
                                 function, fin_function_def)

        results_problem.append(individual_result)

    return results_problem, best_fit

def fit(data, function, minimizer, cost_function):

    popt, t_start, t_end = None, None, None
    func_callable = function[0]
    initial_params = function[1]

    try:
        t_start = time.clock()
        popt = execute_fit(func_callable, data, initial_params, minimizer,
                           cost_function)
        t_end = time.clock()
    except(RuntimeError, ValueError) as err:
        logger.error("Warning, fit failed. Going on. Error: " + str(err))

    status, fitted_y, fin_function_def, runtime = \
    parse_result(func_callable, popt, t_start, t_end)

    return status, fitted_y, fin_function_def, runtime

def execute_fit(function, data, initial_params, minimizer, cost_function):

    popt, pcov = None, None
    if cost_function == 'least squares':
        popt, pcov = curve_fit(f=function.__call__, xdata=data[0],
                               ydata=data[1], sigma=data[2], p0=initial_params,
                               method=minimizer)
    elif cost_function == 'unweighted least squares':
        popt, pcov = curve_fit(f=function.__call__, xdata=data[0],
                               ydata=data[1], p0=initial_params,
                               method=minimizer)
    return popt

def parse_result(function, popt, t_start, t_end):

    status = 'failed'
    fin_function_def, fitted_y, runtime = None, None, np.nan
    if not popt is None:
        status = 'success'
        fitted_y = create_fitted_ydata(function, data_x, popt)
        fin_function_def = create_final_function_def(problem, popt)
        runtime = t_end - t_start

    return status, fitted_y, fin_function_def, runtime

def chisq(status, data, fitted_y, min_chi_sq, best_fit):

    if status != 'failed':
        differences = fitted_y - data[1]
        chi_sq = misc.compute_chisq(differences)
        if chi_sq < min_chi_sq and not chi_sq == np.nan:
            best_fit = plot_helper.data(minimizer_name, data[0], fitted_y)
            min_chi_sq = chi_sq
    else:
        chi_sq = np.nan

    return chi_sq, min_chi_sq, best_fit

def create_final_function_def(problem, popt):

    fin_function_def = problem.equation

    find_float = re.compile("[-+]?[0-9]*\.?[0-9]+")
    for idx in range(len(popt)):
        fin_function_def = find_float.sub(popt[idx], fin_function_def,  idx)

    return fin_function_def

def create_fitted_ydata(function, data_x, popt):

    parameter_names = get_all_parameter_names(problem)
    for idx in range(0, len(popt)):
        function[parameter_names[idx]] = popt[idx]

    fitted_y = function(data_x)

    return fitted_y

def get_neutron_initial_param_names(function_string, parameter_names):

    while True:
        comma = function_string.find(',')
        equal = function_string.find('=', comma)
        if equal == -1: break
        parameter_names.append(function_string[comma+1:equal-1])

    return parameter_names

def get_all_parameter_names(problem):

    functions = problem.equation.split(';')
    parameter_names = []
    for function_string in functions:
        parameter_names = \
        get_neutron_initial_param_names(function_string, parameter_names)

    return parameter_names


def prepare_data(problem, use_errors):

    if use_errors:
        data = np.array([np.copy(problem.data_x), np.copy(problem.data_y),
                         np.copy(problem.data_e)])
        cost_function = 'least squares'
    else:
        data = np.array(np.copy(problem.data_x), np.copy(problem.data_y))
        cost_function = 'unweighted least squares'

    return data, cost_function

def function_definitions(problem):

    if problem.type == 'nist':
        return nist_func_definitions(problem.equation, problem.starting_values)
    elif problem.type == 'neutron':
        return neutron_func_definitions(problem.equation)
    else:
        RuntimeError("Your desired algorithm is not supported yet!")

def nist_func_definitions(function, startvals):

    startvals = np.array(startvals, dtype=object)
    params = ", ".join(param for param in startvals[:, 0])

    function = function.replace("exp", "np.exp")

    function_defs = []
    for values in starting_values[:, 1]:
        exec "def fitting_function(x, " + params + "): return " + function
        function_defs.append([fitting_function, values])

    return function_defs

def get_neutron_func_params(function, function_params):

    first_comma = function.find(',')
    if first_comma != -1:
        function_params.append(function[first_comma+1:])
    else:
        function_params.append('')

    function_params[-1] = function_params[-1].replace(',', ', ')

    return function_params

def get_all_neutron_func_params(functions_string):

    functions = functions_string.split(';')
    function_params = []
    for function in functions:
        function_params = get_neutron_func_params(function, function_params)

    return function_params

def get_neutron_func_names(function, function_names):

    first_comma = function.find(',')
    if first_comma != -1:
        function_names.append(function[5:first_comma])
    else:
        function_names.append(function[5:])

    return function_names

def get_all_neutron_func_names(functions_string):

    functions = functions_string.split(';')
    function_names = []
    for function in functions:
        function_names = get_neutron_func_names(function, function_names)

    return function_names

def make_neutron_fit_function(func_name, fit_function):

    func_obj = mantid.gen_func_obj(func_name)
    if fit_function == None: fit_function = func_obj
    else: fit_function += func_obj

    return fit_function

def find_neutron_params(param_set, params):

    start = 0
    while True:
        comma = param_set.find(',', start)
        if comma == -1: break;
        equal = param_set.find('=', start)
        parameter = param_set[equal+1:comma-1]
        params.append(parameter)
        start = comma + 1

    return params

def get_neutron_initial_params_values(function_params):

    params = []
    for param_set in function_params:
        start = 0
        find_neutron_params(param_set, params)

    return params

def neutron_func_definitions(functions_string):

    function_names = get_all_neutron_func_names(functions_string)
    function_params = get_all_neutron_func_params(functions_string)
    fit_function = None
    for name in function_names:
        fit_function = make_neutron_fit_function(name, fit_function)

    params = get_neutron_initial_params_values(function_params)
    function_defs = [[fit_function, params]]

    return function_defs
