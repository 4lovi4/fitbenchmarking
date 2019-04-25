"""
Main module of the tool, this holds the master function that calls
lower level functions to fit and benchmark a set of problems
for a certain fitting software.
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

import os
import json
from utils.logging_setup import logger

from parsing import parse
from utils import create_dirs, misc
from fitbenchmark_one_problem import fitbm_one_prob


def do_fitting_benchmark(group_name, software_options, data_dir,
                         use_errors=True, results_dir=None):
  """
  High level function that does the fitting benchmarking for a
  specified group of problems.

  @param software :: software used in fitting the problem, can be
                      e.g. mantid, scipy etc.
  @param data_dir :: directory that holds the problem group data
  @param use_errors :: whether to use errors on the data or not
  @param results_dir :: directory in which to put the results. None
                      means results directory is created for you

  @returns :: array of fitting results for the problem group and
              the path to the results directory
  """
  software = software_options['software']
  minimizers_list = software_options['minimizers_list']
  json_file = software_options['json_file']

  minimizers, software = misc.get_minimizers(software, minimizers_list, json_file)
  problem_groups = misc.setup_fitting_problems(data_dir, group_name)

  results_dir = create_dirs.results(results_dir)
  group_results_dir = create_dirs.group_results(results_dir, group_name)

  user_input = misc.save_user_input(software, minimizers, group_name,
                                    group_results_dir, use_errors)

  prob_results = None
  prob_results = \
      [do_fitbm_group(user_input, block) for block in problem_groups[group_name]]

  return prob_results, results_dir


def do_fitbm_group(user_input, problem_block):
  """
  Fit benchmark a specific group of problems.

  @param user_input :: all the information specified by the user
  @param problem_block :: array of paths to problem files in the group

  @returns :: array of result objects, per problem
  """

  results_per_problem = []
  for prob_file in problem_block:
    problem = parse.parse_problem_file(prob_file)
    results_prob = fitbm_one_prob(user_input, problem)
    results_per_problem.extend(results_prob)

  return results_per_problem
