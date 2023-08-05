#!/usr/bin/env python3
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.

import os
import unittest
import shutil
from ipykernel.tests.utils import assemble_output, execute, wait_for_idle
from sos_notebook.test_utils import sos_kernel, get_result, get_display_data, \
    clear_channels

class TestMatlabKernel(unittest.TestCase):
    #
    # Beacuse these tests would be called from sos/test, we
    # should switch to this directory so that some location
    # dependent tests could run successfully
    #
    def setUp(self):
        self.olddir = os.getcwd()
        if os.path.dirname(__file__):
            os.chdir(os.path.dirname(__file__))

    def tearDown(self):
        os.chdir(self.olddir)
    
    @unittest.skipIf(not shutil.which('matlab'), 'Matlab not installed')
    def testGetPythonDataFrameFromMatlab(self):
        # Python -> Matlab/Matlab
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            # create a data frame
            execute(kc=kc, code='''
import pandas as pd
import numpy as np
import scipy.io as sio
arr = np.random.randn(1000)
arr[::10] = np.nan
df = pd.DataFrame({'column_{0}'.format(i): arr for i in range(10)})
''')
            clear_channels(iopub)
            execute(kc=kc, code="%use MATLAB")
            wait_for_idle(kc)
            #_, stderr = assemble_output(iopub)
            #self.assertEqual(stderr, '')
            execute(kc=kc, code="%get df")
            wait_for_idle(kc)
            execute(kc=kc, code="display(size(df))")
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip().split(), ['1000', '10'])
            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)

    @unittest.skipIf(not shutil.which('matlab'), 'Matlab not installed')
    def testGetPythonDataFromMatlab(self):
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            execute(kc=kc, code='''
null_var = None
num_var = 123
import numpy
import scipy.io as sio
num_arr_var = numpy.array([1, 2, 3])
logic_var = True
logic_arr_var = [True, False, True]
float_var = [1.2, 2.1]
char_var = '1"23'
char_arr_var = ['1', '2', '3']
list_var = [1, 2, '3']
dict_var = dict(a=1, b=2, c='3')
set_var = {1, 2, '3'}
mat_var = numpy.matrix([[1,2],[3,4]])
recursive_var = {'a': {'b': 123}, 'c': True}
''')
            wait_for_idle(kc)
            execute(kc=kc, code='''
%use MATLAB
%get null_var num_var num_arr_var logic_var logic_arr_var char_var char_arr_var mat_var set_var list_var dict_var recursive_var float_var
%dict -r
%put null_var num_var num_arr_var logic_var logic_arr_var char_var char_arr_var mat_var set_var list_var dict_var recursive_var float_var
%use sos
%dict null_var num_var num_arr_var logic_var logic_arr_var char_var char_arr_var mat_var set_var list_var dict_var recursive_var float_var
                ''')
            res = get_result(iopub)
            self.assertEqual(res['null_var'], None)
            self.assertEqual(res['num_var'], 123)
            self.assertEqual(list(res['num_arr_var']), [1,2,3], "Got {}".format(res['num_arr_var']))
            self.assertEqual(res['logic_var'], True)
            self.assertEqual(res['logic_arr_var'], [True, False, True])
            self.assertEqual(res['char_var'], '1"23')
            self.assertEqual(list(res['float_var']), [1.2, 2.1])
            self.assertEqual(list(res['list_var']), [1,2,'3'], 'Got {}'.format(res['list_var']))
            self.assertEqual(res['dict_var'], {'a': 1, 'b': 2, 'c': '3'})
            self.assertTrue(len(res['set_var']) ==3 and '3' in res['set_var'] and 1 in res['set_var'] and 2 in res['set_var'])

            self.assertEqual(res['mat_var'].shape, (2,2))
            self.assertEqual(res['recursive_var'],  {'a': {'b': 123}, 'c': True})
            #self.assertEqual(res['char_arr_var'], ['1', '2', '3'])

    @unittest.skipIf(not shutil.which('matlab'), 'Matlab not installed')
    def testPutMatlabDataToPython(self):
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            execute(kc=kc, code="""
%use MATLAB
null_var = NaN
num_var = 123
num_arr_var = [1, 2, 3]
logic_var = true
logic_arr_var = [true, false, true]
char_var = '1"23'
char_arr_var = ['1'; '2'; '3']
mat_var = [1:3; 2:4]
""")
            wait_for_idle(kc)
            execute(kc=kc, code="""
%dict -r
%put null_var num_var num_arr_var logic_var logic_arr_var char_var char_arr_var mat_var
%dict null_var num_var num_arr_var logic_var logic_arr_var char_var char_arr_var mat_var
""")
            res = get_result(iopub)
            self.assertEqual(res['null_var'], None)
            self.assertEqual(res['num_var'], 123)
            self.assertEqual(list(res['num_arr_var']), [1,2,3])
            self.assertEqual(res['logic_var'], True)
            self.assertEqual(res['logic_arr_var'], [True, False, True])
            self.assertEqual(res['char_var'], '1"23')
            #self.assertEqual(res['named_list_var'], {'a': 1, 'b': 2, 'c': '3'})
            self.assertEqual(res['mat_var'].shape, (2,3))
            self.assertEqual(res['char_arr_var'], ['1', '2', '3'])
            #self.assertEqual(res['recursive_var'], {'a': 1, 'b': {'c': 3, 'd': 'whatever'}})
            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)


if __name__ == '__main__':
    unittest.main()

