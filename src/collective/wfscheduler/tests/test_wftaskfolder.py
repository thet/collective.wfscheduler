# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from collective.wfscheduler.interfaces import IWFTaskFolder
from collective.wfscheduler.testing import COLLECTIVE_WFSCHEDULER_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class WFTaskFolderIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_WFSCHEDULER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='WFTaskFolder')
        schema = fti.lookupSchema()
        self.assertEqual(IWFTaskFolder, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='WFTaskFolder')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='WFTaskFolder')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IWFTaskFolder.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='WFTaskFolder',
            id='WFTaskFolder',
        )
        self.assertTrue(IWFTaskFolder.providedBy(obj))
