import os
import unittest

fbscript = {}
fbscript_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__),
                 os.pardir,
                 'fitbenchmarking'))

try:
    exec(fbscript_path, fbscript)
except SyntaxError:
    execfile(fbscript_path, fbscript)

run = fbscript['run']
get_parser = fbscript['get_parser']


class TestExampleScripts(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # get curdir and store for teardown
        self.cwd = os.getcwd()

        # get rootdir of repo
        root_dir = os.path.join(os.path.dirname(__file__),
                                os.pardir,
                                os.pardir)

        # chdir to root dir
        os.chdir(root_dir)

    @classmethod
    def tearDownClass(self):
        os.chdir(self.cwd)

    def test_run_with_options(self):
        run(['examples/benchmark_problems/simple_tests'],
            options_file='examples/options_template.ini')

    def test_run_no_options(self):
        run(['examples/benchmark_problems/simple_tests'])

    def test_arg_parse(self):
        parser = get_parser()

        options_file = 'some_file/with_options'
        problem_sets = ['problems_1', 'problems2/*']

        args = parser.parse_args(['-o', options_file] + problem_sets)

        self.assertEqual(args.options_file, options_file)
        self.assertEqual(args.problem_sets, problem_sets)
