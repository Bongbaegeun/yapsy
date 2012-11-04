import test_settings

import os 
import unittest

from yapsy.PluginManager import PluginManager

class ErrorTestCase(unittest.TestCase):
    """
    Test the handling of errors during plugin load.
    """

    def testTwoStepsLoadWithError(self):
        """
        Test loading the plugins in two steps in order to collect more
        deltailed informations and take care of an erroneous plugin.
        """
        spm = PluginManager(directories_list=[
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),"plugins")
                                ], plugin_info_ext="yapsy-error-plugin")
        # trigger the first step to look up for plugins
        spm.locatePlugins()
        # make full use of the "feedback" the loadPlugins can give
        # - set-up the callback function that will be called *before*
        # loading each plugin
        callback_infos = []
        def preload_cbk(i_plugin_info):
            callback_infos.append(i_plugin_info)
        # - gather infos about the processed plugins (loaded or not)
        loadedPlugins = spm.loadPlugins(callback=preload_cbk)
        self.assertEqual(len(loadedPlugins),1)
        self.assertEqual(len(callback_infos),1)
        self.assertTrue(isinstance(callback_infos[0].error,tuple))
        self.assertEqual(loadedPlugins[0],callback_infos[0])
        self.assertEqual(callback_infos[0].error[0],ImportError)
        # check that the getCategories works
        self.assertEqual(len(spm.getCategories()),1)
        sole_category = spm.getCategories()[0]
        # check the getPluginsOfCategory
        self.assertEqual(len(spm.getPluginsOfCategory(sole_category)),0)



suite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(ErrorTestCase),
        ])
