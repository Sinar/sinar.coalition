# -*- coding: utf-8 -*-
from sinar.coalition.content.membership import IMembership  # NOQA E501
from sinar.coalition.testing import SINAR_COALITION_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class MembershipIntegrationTest(unittest.TestCase):

    layer = SINAR_COALITION_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'Coalition',
            self.portal,
            'parent_container',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_membership_schema(self):
        fti = queryUtility(IDexterityFTI, name='Membership')
        schema = fti.lookupSchema()
        self.assertEqual(IMembership, schema)

    def test_ct_membership_fti(self):
        fti = queryUtility(IDexterityFTI, name='Membership')
        self.assertTrue(fti)

    def test_ct_membership_factory(self):
        fti = queryUtility(IDexterityFTI, name='Membership')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IMembership.providedBy(obj),
            u'IMembership not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_membership_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='Membership',
            id='membership',
        )

        self.assertTrue(
            IMembership.providedBy(obj),
            u'IMembership not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('membership', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('membership', parent.objectIds())

    def test_ct_membership_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Membership')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id)
        )

    def test_ct_membership_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Membership')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'membership_id',
            title='Membership container',
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
