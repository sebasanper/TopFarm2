'''
Created on 16. apr. 2018

@author: mmpe
'''
import unittest
from topfarm.cost_models.fuga.py_fuga import PyFuga
import numpy as np
from threading import Thread
import threading
import time
from cost_models.fuga.pascal_dll import PascalDLL


fuga_path = r'C:\mmpe\programming\pascal\Fuga\Colonel/'

def test_parallel(id):
            pyFuga = PyFuga(fuga_path + "FugaLib/FugaLib.dll",
                      farm_name='Horns Rev 1',
                      turbine_model_path=fuga_path + 'LUT/', turbine_model_name='Vestas_V80_(2_MW_offshore)[h=67.00]',
                      tb_x=[423974, 424033], tb_y=[6151447, 6150889],
                      mast_position=(0, 0, 70), z0=0.0001, zi=400, zeta0=0,
                      farms_dir=fuga_path + 'LUT/Farms/', wind_atlas_path='Horns Rev 1\hornsrev0.lib')
            print (pyFuga.stdout_filename, id)
            for i in range(1):
                print(threading.current_thread(), id)
                np.testing.assert_array_almost_equal(pyFuga.get_aep([0, 0], [0, 200]), [14.044704, 16.753474, 0.401041, 0.838316])
                time.sleep(1)



class Test(unittest.TestCase):

    def get_fuga(self):
        return PyFuga(fuga_path + "FugaLib/FugaLib.dll",
                      farm_name='Horns Rev 1',
                      turbine_model_path=fuga_path + 'LUT/', turbine_model_name='Vestas_V80_(2_MW_offshore)[h=67.00]',
                      tb_x=[423974, 424033], tb_y=[6151447, 6150889],
                      mast_position=(0, 0, 70), z0=0.0001, zi=400, zeta0=0,
                      farms_dir=fuga_path + 'LUT/Farms/', wind_atlas_path='Horns Rev 1\hornsrev0.lib')
        
    

    def testCheckVersion(self):
        lib = PascalDLL(fuga_path + "FugaLib/FugaLib.dll")
        self.assertRaisesRegex(Exception, "This version of FugaLib supports interface version ", lib.CheckInterfaceVersion, 1)
        # PyFuga(fuga_path + "FugaLib/FugaLib.dll", fuga_path + "LUT/Farms/", "Horns Rev 1", fuga_path + "LUT/",
        #                (0, 0, 70), 0.0001, 400, 0, 'Horns Rev 1\hornsrev0.lib')

    def testSetup(self):
        pyFuga = self.get_fuga()
        self.assertEqual(pyFuga.get_no_tubines(), 2)
        self.assertIn("Loading", pyFuga.log)

    def testAEP(self):
        pyFuga = self.get_fuga()
        
        np.testing.assert_array_almost_equal(pyFuga.get_aep([0, 0], [0, 200]), [14.044704, 16.753474, 0.401041, 0.838316])
        np.testing.assert_array_almost_equal(pyFuga.get_aep([0, 200], [0, 0]), [16.714122, 16.753474, 0.477265, 0.997651])
        np.testing.assert_array_almost_equal(pyFuga.get_aep([0, 200], [0, 200]), [17.072517, 16.753474, 0.487499, 1.019043])
        np.testing.assert_array_almost_equal(pyFuga.get_aep_gradients([0, 200], [0, 200]), [[0.002905, -0.002905],
                                                                                            [-0.001673, 0.001673],
                                                                                            [0., 0.]])
        print (pyFuga.log)
 
    def test_parallel(self):
        from multiprocessing import Pool
 
        with Pool(5) as p:
            print(p.map(test_parallel, [1, 2]))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAEP']
    unittest.main()
