# -*- coding: utf-8 -*-
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE,
    PloneSandboxLayer,
)

import sinar.coalition


class SinarCoalitionLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=sinar.coalition)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'sinar.coalition:default')


SINAR_COALITION_FIXTURE = SinarCoalitionLayer()


SINAR_COALITION_INTEGRATION_TESTING = IntegrationTesting(
    bases=(SINAR_COALITION_FIXTURE,),
    name='SinarCoalitionLayer:IntegrationTesting',
)


SINAR_COALITION_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(SINAR_COALITION_FIXTURE,),
    name='SinarCoalitionLayer:FunctionalTesting',
)
