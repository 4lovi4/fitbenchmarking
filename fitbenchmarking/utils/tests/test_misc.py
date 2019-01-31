from __future__ import (absolute_import, division, print_function)

import unittest
import os, shutil

# Delete four lines below when automated tests ar enabled
import sys
test_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(os.path.normpath(test_dir))
main_dir = os.path.dirname(os.path.normpath(parent_dir))
sys.path.insert(0, main_dir)

from misc import get_minimizers
from misc import setup_fitting_problems

class CreateDirsTests(unittest.TestCase):

    def base_path(self):
        """
        Helper function that returns the path to
        /fitbenchmarking/benchmark_problems
        """

        current_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.dirname(os.path.normpath(test_dir))
        main_dir = os.path.dirname(os.path.normpath(parent_dir))
        root_dir = os.path.dirname(os.path.normpath(main_dir))
        bench_prob_dir = os.path.join(root_dir, 'benchmark_problems')

        return bench_prob_dir


    def all_neutron_problems(self):
        """
        Helper function that returns the names of all neutron problems.
        """

        neutron_problems = [['ENGINX193749_calibration_peak19.txt',
                             'ENGINX193749_calibration_peak20.txt',
                             'ENGINX193749_calibration_peak23.txt',
                             'ENGINX193749_calibration_peak5.txt',
                             'ENGINX193749_calibration_peak6.txt',
                             'ENGINX236516_vanadium_bank1_10brk.txt',
                             'ENGINX236516_vanadium_bank1_20brk.txt',
                             'EVS14188-90_Gaussian_peaks_1.txt',
                             'EVS14188-90_Gaussian_peaks_2.txt',
                             'GEMpeak1.txt',
                             'WISH17701_peak1.txt', 'WISH17701_peak2.txt',
                             'WISH17701_peak3.txt', 'WISH17701_peak4.txt',
                             'WISH17701_peak5.txt', 'WISH17701_peak6.txt',
                             'WISH17701_peak7.txt', 'WISH17701_peak8.txt',
                             'WISH17701_peak9.txt']]

        return neutron_problems


    def all_nist_problems(self):
        """
        Helper function that returns the names of all NIST problems.
        """

        nist_problems = [['Misra1a.dat', 'Chwirut2.dat', 'Chwirut1.dat',
                          'Lanczos3.dat', 'Gauss1.dat', 'Gauss2.dat',
                          'DanWood.dat', 'Misra1b.dat'],
                         ['Kirby2.dat', 'Hahn1.dat','MGH17.dat',
                          'Lanczos1.dat', 'Lanczos2.dat','Gauss3.dat',
                          'Misra1c.dat', 'Misra1d.dat','ENSO.dat'],
                         ['MGH09.dat', 'Thurber.dat', 'BoxBOD.dat', 'Rat42.dat',
                          'MGH10.dat', 'Eckerle4.dat', 'Rat43.dat',
                          'Bennett5.dat']]

        return nist_problems

    def get_minimizers_file(self):

        test_dir = os.getcwd()
        utils_dir = os.path.dirname(os.path.normpath(test_dir))
        fitbm_dir = os.path.dirname(os.path.normpath(utils_dir))
        minimizer_json = os.path.join(fitbm_dir, "minimizers.json")

        return minimizer_json

    def test_getMinimizers_load_correct_minimizers_mantid(self):

        software = 'mantid'

        minimiers = get_minimizers(software)
        minmizers_expected = \
        ["BFGS", "Conjugate gradient (Fletcher-Reeves imp.)",
         "Conjugate gradient (Polak-Ribiere imp.)", "Damped GaussNewton",
         "Levenberg-Marquardt", "Levenberg-MarquardtMD", "Simplex",
         "SteepestDescent", "Trust Region"]

        self.assertListEqual(minmizers_expected, minimiers)

    def test_getMinimizers_load_correct_minimizers_scipy(self):

        software = 'scipy'

        minimiers = get_minimizers(software)
        minmizers_expected = ["lm", "trf", "dogbox"]

        self.assertListEqual(minmizers_expected, minimiers)

    def test_setupFittingProblems_get_correct_nist_probs(self):

        data_dir = os.path.join(self.base_path(), 'NIST_nonlinear_regression')
        nist_problems = self.all_nist_problems()

        problem_groups = setup_fitting_problems(data_dir)
        problem_groups_expected = {'nist' : nist_problems}

        self.assertTrue(problem_groups_expected, problem_groups)

    def test_setupFittingProblems_get_correct_neutron_probs(self):

        data_dir = os.path.join(self.base_path(), 'Neutron')
        neutron_problems = self.all_neutron_problems()

        problem_groups = setup_fitting_problems(data_dir)
        problem_groups_expected = {'nist' : neutron_problems}

        self.assertTrue(problem_groups_expected, problem_groups)

if __name__ == "__main__":
    unittest.main()