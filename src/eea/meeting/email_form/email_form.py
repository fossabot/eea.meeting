from eea.meeting import _
from plone.z3cform.layout import wrap_form
from z3c.form import button, form, field
from eea.meeting.events.rules import SendEmailAddEvent
from zope.event import notify
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile
from eea.meeting.interfaces import IEmail
from plone import api
from zope.container.interfaces import INameChooser
from z3c.form.browser.checkbox import CheckBoxFieldWidget

class SendEmail(form.Form):

    fields = field.Fields(IEmail)
    ignoreContext = True

    fields['receiver'].widgetFactory = CheckBoxFieldWidget

    @button.buttonAndHandler(_('Send Email'), name='send_email')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            return False

        types = api.portal.get_tool('portal_types')
        type_info = types.getTypeInfo('eea.meeting.email')

        name_chooser = INameChooser(self.context)
        content_id = name_chooser.chooseName(data['subject'], self.context)

        obj = type_info._constructInstance(self.context, content_id)

        obj.title = data['subject']

        obj.sender = data['sender']
        obj.receiver = data['receiver']
        # obj.receiver2 = data['receiver2']
        obj.cc = data['cc']
        obj.subject = data['subject']
        obj.body = data['body']

        obj.reindexObject()

        notify(SendEmailAddEvent(self.context, data))

        redirect_url = "%s/@@email_sender_confirmation" % self.context.absolute_url()
        self.request.response.redirect(redirect_url)

SendEmailView = wrap_form(SendEmail, index=FiveViewPageTemplateFile("send_email.pt"))