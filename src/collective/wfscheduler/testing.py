# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.wfscheduler


class CollectiveWfschedulerLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.wfscheduler)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.wfscheduler:default')


COLLECTIVE_WFSCHEDULER_FIXTURE = CollectiveWfschedulerLayer()


COLLECTIVE_WFSCHEDULER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_WFSCHEDULER_FIXTURE,),
    name='CollectiveWfschedulerLayer:IntegrationTesting'
)


COLLECTIVE_WFSCHEDULER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_WFSCHEDULER_FIXTURE,),
    name='CollectiveWfschedulerLayer:FunctionalTesting'
)


COLLECTIVE_WFSCHEDULER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_WFSCHEDULER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveWfschedulerLayer:AcceptanceTesting'
)
