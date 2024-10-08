from django import forms
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from crispy_forms.bootstrap import FieldWithButtons

from tinymce.widgets import TinyMCE

from notes.models import STATUS_OPTIONS

class NoteForm(forms.Form):
    url = forms.CharField(required=False)
    title = forms.CharField(required=True)
    description = forms.CharField(widget=TinyMCE(), required=False)
    tags = forms.CharField(
                required=True,
                error_messages={'required':
                                _('Please enter at least one tag')},)
    status = forms.ChoiceField(
        choices=STATUS_OPTIONS,
        required=True,
    )
    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
                'title',
                'url',
                'description',
                'tags',
                'status',
                Div(
                   Submit('submit', _(u'Save'), css_class='btn btn-default'),
                   css_class='col-lg-offset-2 col-lg-4',
                ),
            )


class SearchForm(forms.Form):
    q = forms.CharField(
        required=True,
        error_messages={'required':
                        _(u'Please enter something to search for')},)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_method = "GET"
        self.helper.form_class = 'form-horizontal'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            FieldWithButtons('q', Submit('submit', _(u'Go'),
                                         css_class='btn btn-default')))
