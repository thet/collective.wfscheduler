# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from collective.wfscheduler.testing import COLLECTIVE_WFSCHEDULER_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.wfscheduler is properly installed."""

    layer = COLLECTIVE_WFSCHEDULER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.wfscheduler is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.wfscheduler'))

    def test_browserlayer(self):
        """Test that ICollectiveWfschedulerLayer is registered."""
        from collective.wfscheduler.interfaces import (
            ICollectiveWfschedulerLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveWfschedulerLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_WFSCHEDULER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.wfscheduler'])

    def test_product_uninstalled(self):
        """Test if collective.wfscheduler is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.wfscheduler'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveWfschedulerLayer is removed."""
        from collective.wfscheduler.interfaces import \
            ICollectiveWfschedulerLayer
        from plone.browserlayer import utils
        self.assertNotIn(
           ICollectiveWfschedulerLayer,
           utils.registered_layers())
