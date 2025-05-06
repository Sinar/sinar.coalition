# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
from plone.autoform import directives
# from collective import dexteritytextindexer
from plone.dexterity.content import Container
from plone.app.vocabularies.catalog import CatalogSource
# from plone.namedfile import field as namedfile
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from z3c.relationfield.schema import RelationChoice
from zope.interface import implementer
from sinar.coalition import _


class IMembership(model.Schema):
    """ Marker interface and Dexterity Python Schema for Membership
    """

    label = schema.TextLine(
        title=_('Label'),
        description=_("A label describing the membership eg. Member of SEA-ACN-Network"),
        required=True,)

    role = schema.TextLine(
        title=_('Role'),
        description=_("A role that the member fulfills in, eg. Co-Chair of SEA-ACN"),
        required=True,)

    # Coalition
    directives.widget('coalition', RelatedItemsFieldWidget,
                      pattern_options={'basePath': '/',
                                       'mode': 'auto',
                                       'favourites': [], })

    coalition = RelationChoice(title='Coalition',
                               source=CatalogSource(portal_type='Coalition'),
                               required=True,)

    # Organization
    directives.widget('organization', RelatedItemsFieldWidget,
                      pattern_options={'basePath': '/',
                                       'mode': 'auto',
                                       'favourites': [], })

    organization = RelationChoice(title='Organization',
                                  source=CatalogSource(portal_type='Organization'),
                                  required=True,)

    start_date = schema.Date(
        title=_('Start Date'),
        description=_('Date which this relationship began'),
        required=False,)

    end_date = schema.Date(
        title=_('End Date'),
        description=_('Date which this relationship ended'),
        required=False,)


@implementer(IMembership)
class Membership(Container):
    """ Content-type class for IMembership
    """

    @property
    def title(self):
        ''' return label'''
        return self.label

    @title.setter
    def title(self, value):
        ''' we wont set a title here'''

    @property
    def description(self):
        ''' return role'''
        return self.role

    @description.setter
    def description(self, value):
        ''' we wont set a title here'''
