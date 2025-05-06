# -*- coding: utf-8 -*-
from sinar.coalition.content.coalition import ICoalition  # NOQA E501
from sinar.coalition.testing import SINAR_COALITION_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class CoalitionIntegrationTest(unittest.TestCase):

    layer = SINAR_COALITION_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_coalition_schema(self):
        fti = queryUtility(IDexterityFTI, name='Coalition')
        schema = fti.lookupSchema()
        self.assertEqual(ICoalition, schema)

    def test_ct_coalition_fti(self):
        fti = queryUtility(IDexterityFTI, name='Coalition')
        self.assertTrue(fti)

    def test_ct_coalition_factory(self):
        fti = queryUtility(IDexterityFTI, name='Coalition')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            ICoalition.providedBy(obj),
            u'ICoalition not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_coalition_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Coalition',
            id='coalition',
        )

        self.assertTrue(
            ICoalition.providedBy(obj),
            u'ICoalition not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('coalition', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('coalition', parent.objectIds())

    def test_ct_coalition_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Coalition')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_coalition_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Coalition')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'coalition_id',
            title='Coalition container',
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
