"""
Miscellaneous functions and utilites for fitting.
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

import os, json

def get_minimizers(algorithm):
    """
    Gets the a
    """
    current_path = os.path.dirname(os.path.realpath(__file__))
    fitbm_path = os.path.abspath(os.path.join(current_path, os.pardir))
    minimizers_dir = os.path.join(fitbm_path, "fitting")
    minimizers_json = os.path.join(minimizers_dir, "minimizers.json")
    all_minimizers = json.load(open(minimizers_json))
    minimizers = all_minimizers[algorithm]

    return minimizers
