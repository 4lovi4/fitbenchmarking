"""
Compares the current results with a set of expected results.
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
# File change history is stored at: <https://github.com/mantidproject/mantid>.
# Code Documentation is available at: <http://doxygen.mantidproject.org>
# ==============================================================================


class SystemTest(unittest.TestCase):

    def path_to_results(self):

        current_dir = os.path.dirname(os.path.realpath(__file__))
        results_dir = os.path.join(current_dir, "results")

        return results_dir

    def path_to_expected_results_dir(self):

        current_dir = os.path.dirname(os.path.realpath(__file__))
        expected_results_dir = os.path.join(current_dir, "expected_results")

        return expected_results_dir

    def get_expected_results_paths_nist(self):

        expected_results_dir = self.path_to_expected_results_dir()
        nist_low_path = os.path.join(expected_results_dir, "nist_low")
        nist_average_path = os.path.join(expected_results_dir, "nist_average")
        nist_high_path = os.path.join(expected_results_dir, "nist_high")

        return nist_low_path, nist_average_path, nist_high_path

    def read_expected_results_nist(self):

        nist_low_path, nist_average_path, nist_high_path = \
        self.get_expected_results_paths_nist()

        with open(nist_low_path) as f:
            nist_low = f.read()
        with open(nist_average_path) as f:
            nist_average = f.read()
        with open(nist_high_path) as f:
            nist_high = f.read()

        return nist_low, nist_average, nist_high

    def get_expected_results_paths_neutron(self):

        expected_results_dir = self.path_to_expected_results_dir()
        neutron_path = os.path.join(expected_results_dir, "neutron")

        return neutron_path

    def read_expected_results_neutron(self):

        neutron_path = self.get_expected_results_paths_neutron()

        with open(neutron_path) as f:
            neutron = f.read()

        return neutron

    def get_results_paths_nist(self):

        results_dir = self.path_to_results()
        nist_tables_dir = os.path.join(results_dir, "nist", "tables")

        nist_low_dir = os.path.join(nist_tables_dir, "nist_lower")
        nist_average_dir = os.path.join(nist_tables_dir, "nist_average")
        nist_high_dir = os.path.join(nist_tables_dir, "nist_higher")

        nist_low_path = \
        os.path.join(nist_low_dir, "nist_lower_acc_weighted_table.txt")
        nist_average_path = \
        os.path.join(nist_average_dir, "nist_average_acc_weighted_table.txt")
        nist_high_path = \
        os.path.join(nist_high_dir, "nist_high_acc_weighted_table.txt")

        return nist_low_path, nist_average_path, nist_high_path

    def read_results_nist(self):

        nist_low_path, nist_average_path, nist_high_path = \
        self.get_results_paths_nist()

        with open(nist_low_path) as f:
            nist_low = f.read()
        with open(nist_average_path) as f:
            nist_average = f.read()
        with open(nist_high_path) as f:
            nist_high = f.read()

        return nist_low, nist_average, nist_high

    def get_results_paths_neutron(self):

        results_dir = self.path_to_results()
        neutron_tables_dir = os.path.join(results_dir, "neutron", "tables")
        neutron_path = \
        os.path.join(neutron_tables_dir, "neutron_data_acc_weighted_table.txt")

        return neutron

    def read_results_neutron(self):

        neutron_path = self.get_results_paths_neutron()

        with open(neutron_path) as f:
            neutron = f.read()

        return neutron


    def test_nist(self):

        expected_results = [self.read_expected_results_nist()]
        results = [self.read_results_nist()]

        self.assertEqual(expected_results[0], results[0])
        self.assertEqual(expected_results[1], results[1])
        self.assertEqual(expected_results[2], results[2])

    def test_neutron(self):

        expected_results = [self.read_expected_results_neutron()]
        results = [self.read_results_neutron()]

        self.assertEqual(expected_results[0], results[0])


if __name__ == "__main__":
    unittest.main()
