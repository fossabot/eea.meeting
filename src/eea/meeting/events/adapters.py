from plone.stringinterp.adapters import BaseSubstitution
from eea.meeting import _
from eea.meeting.interfaces import IMeeting


class SetEmailSubstitution(BaseSubstitution):

    attribute = u''

    def __init__(self, context, **kwargs):
        super(SetEmailSubstitution, self).__init__(context, **kwargs)
        self._session = None

    @property
    def session(self):
        """ User session
        """
        if self._session is None:
            sdm = getattr(self.context, 'session_data_manager', None)
            self._session = sdm.getSessionData(create=False) if sdm else {}
        return self._session

    @property
    def sender(self):
        """Email sender"""
        return self.session.get('sender', '')

    @property
    def receiver(self):
        """Email receiver"""
        return ','.join(self.session.get('receiver', []) or [])

    @property
    def subject(self):
        """Email subject"""
        return self.session.get('subject', '')

    @property
    def body(self):
        """Email body"""
        return self.session.get('body', '')

    @property
    def cc(self):
        """Email cc addresses"""
        return ','.join(self.session.get('cc', []) or [])

    def safe_call(self):
        """ Safe call
        """
        return getattr(self, self.attribute, u'')


class SetEmailSender(SetEmailSubstitution):
    category = _(u'Email Send')
    description = _(u'Email sender address')
    attribute = u'sender'


class SetEmailReceiver(SetEmailSubstitution):
    category = _(u'Email Send')
    description = _(u'Email receiver address')
    attribute = u'receiver'


class SetEmailSubject(SetEmailSubstitution):
    category = _(u'Email Send')
    description = _(u'Email subject')
    attribute = u'subject'


class SetEmailBody(SetEmailSubstitution):
    category = _(u'Email Send')
    description = _(u'Email body')
    attribute = u'body'


class SetEmailCC(SetEmailSubstitution):
    category = _(u'Email Send')
    description = _(u'Email CC addresses')
    attribute = u'cc'


class SetMeetingContactEmail(BaseSubstitution):
    category = _(u'eea.meeting')
    description = _(u'Meeting contact email')

    def safe_call(self):
        """ Safe call
        """
        try:
            email = self.context.contact_email
        except Exception:
            email = ''

        return email


class SetMeetingURL(BaseSubstitution):
    category = _(u'eea.meeting')
    description = _(u'Finds the closest meeting and returns it\'s URL.')

    def safe_call(self):
        """ Safe call
        """
        def find_meeting(context):
            return (
                IMeeting.providedBy(context) and context
                or find_meeting(context.aq_parent)
            )

        meeting = find_meeting(self.context)
        return meeting.absolute_url() if meeting else ''


class SetEmailReceiverOnApproved(BaseSubstitution):
    category = _(u'Approve Subscriber')
    description = _(u'Subscriber Email')

    def safe_call(self):
        """ Safe call
        """
        try:
            email = self.context.email
        except Exception:
            email = ''

        return email


class SetNameReceiverOnApproved(BaseSubstitution):
    category = _(u'Approve Subscriber')
    description = _(u'Subscriber Name')

    def safe_call(self):
        """ Safe call
        """
        try:
            return self.context.get_details().get('fullname', 'user')
        except Exception:
            name = 'user'

        return name


class SetMeetingPlaceOnApproved(BaseSubstitution):
    category = _(u'Approve Subscriber')
    description = _(u'Meeting place')

    def safe_call(self):
        """ Safe call
        """
        try:
            location = self.context.aq_parent.aq_parent.location
        except Exception:
            location = ""

        return location


class SetMeetingTitleOnApproved(BaseSubstitution):
    category = _(u'Approve Subscriber')
    description = _(u'Meeting title')

    def safe_call(self):
        """ Safe call
        """
        if self.context.portal_type == 'eea.meeting.subscriber':
            """ This is the case for approving a subscriber:
                - Thank you for your registration
            """
            meeting = self.context.aq_parent.aq_parent

        elif self.context.portal_type == 'eea.meeting':
            """ This is the case for new subscriber registered:
                - A new participant has registered to the meeting
                - You have registered to the meeting
            """
            meeting = self.context

        try:
            title = meeting.title
        except Exception:
            title = ""

        return title
