"""Specific views for person entities

:organization: Logilab
:copyright: 2003-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"

from logilab.mtconverter import xml_escape

from cubicweb import _
from cubicweb.predicates import is_instance, score_entity
from cubicweb.web import action
from cubicweb.web.views import baseviews, primary, uicfg, vcard
from cubicweb.web.facet import AttributeFacet

_pvs = uicfg.primaryview_section

for attr in ('civility', 'firstname', 'surname'):
    _pvs.tag_attribute(('Person', attr), 'hidden')

_pvs.tag_subject_of(('Person', 'use_email', '*'), 'attributes')
_pvs.tag_subject_of(('Person', 'primary_email', '*'), 'hidden')

_pvdc = uicfg.primaryview_display_ctrl
_pvdc.tag_attribute(('Person', 'description'),
                    {'showlabel': False, 'order': 0})
_pvdc.tag_attribute(('Person', 'use_email'),
                    {'order': 2, 'vid': 'csv', 'label': 'use_email'})


class HRSView(baseviews.CSVView):
    __regid__ = 'person.hrs'
    separator = u'<hr/>'


class PersonPrimaryView(primary.PrimaryView):
    __select__ = is_instance('Person')

    def render_entity_title(self, entity):
        self.w(u'<h1>%s</h1>' % xml_escape(entity.name(civility=True)))


class PersonTextView(baseviews.TextView):
    __select__ = is_instance('Person')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(entity.name())


class PersonEmailView(baseviews.EntityView):
    """display emails sent or received by one of this person's addresses"""
    __regid__ = 'emails'
    __select__ = is_instance('Person')
    title = _('emails')

    def cell_call(self, row, col=0):
        entity = self.cw_rset.get_entity(row, col)
        self.w(u'<h3>')
        self.w(self._cw._('emails sent or received by %s')
               % xml_escape(entity.dc_title()))
        self.w(u'</h3>')
        done = set()
        if getattr(entity, 'primary_email', None):
            email = entity.primary_email[0]
            email.view('shortprimary', w=self.w, skipeids=done)
            pemaileid = email.eid
        else:
            pemaileid = None
        for email in getattr(entity, 'use_email', ()):
            if email.eid == pemaileid:
                continue
            email.view('shortprimary', w=self.w, skipeids=done)


class VCardPersonView(vcard.VCardCWUserView):
    """export a person information as a vcard"""
    __select__ = is_instance('Person')

    def vcard_content(self, entity):
        w = self.w
        who = u'%s %s' % (entity.surname or '',
                          entity.firstname or '')
        w(u'FN:%s\n' % who)
        w(u'N:%s;;;;\n' % who)
        w(u'TITLE:%s\n' % who)
        # XXX
        # if entity.address:
        #    w(u'ADR;TYPE=WORK,POSTAL,PARCEL:;;%s\n' % ';'.join(entity.address.splitlines()))
        for phone in getattr(entity, 'phone', ()):
            ptype = vcard.VCARD_PHONE_TYPES.get(phone.type, phone.type.upper())
            w(u'TEL;TYPE=%s;VOICE:%s\n' % (ptype, phone.number))
        for email in getattr(entity, 'use_email', ()):
            w(u'EMAIL;TYPE=INTERNET:%s\n' % email.address)


# actions ####################################################################

class AddPersonFromEmailAction(action.LinkToEntityAction):
    __regid__ = 'addperson-fromemail'
    __select__ = (is_instance('EmailAddress')
                  & score_entity(lambda x: not x.reverse_use_email))

    title = _('add Person use_email EmailAddress object')
    target_etype = 'Person'
    rtype = 'use_email'
    target = 'subject'


# facets #####################################################################

class CivilityFacet(AttributeFacet):
    __regid__ = 'civility-facet'
    __select__ = is_instance('Person')
    rtype = 'civility'


def registration_callback(vreg):
    vreg.register_all(globals().values(), __name__)
    if 'addressbook' in vreg.config.cubes():
        for rtype in ('phone', 'im_address', 'postal_address'):
            _pvs.tag_subject_of(('Person', rtype, '*'), 'attributes')
        _pvdc.tag_attribute(('Person', 'phone'), {'order': 1, 'vid': 'csv'})
        _pvdc.tag_attribute(('Person', 'im_address'), {'order': 3, 'vid': 'csv'})
        _pvdc.tag_attribute(('Person', 'postal_address'),
                            {'order': 4, 'vid': 'person.hrs'})

        _afs = uicfg.autoform_section
        _afs.tag_subject_of(('Person', 'phone', '*'), 'main', 'inlined')
        _afs.tag_subject_of(('Person', 'postal_address', '*'), 'main', 'inlined')
        _afs.tag_subject_of(('Person', 'im_address', '*'), 'main', 'inlined')
