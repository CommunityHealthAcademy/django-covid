from django import forms
from django.conf import settings
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FieldWithButtons, InlineCheckboxes
from crispy_forms.layout import Button, Layout, Fieldset, ButtonHolder, Submit, Div, HTML, Row, Field, Column

from orb.models import Tag, Resource, Category

from tinymce.models import HTMLField

    
class ResourceForm(forms.Form):
    title = forms.CharField(
                required=True,
                error_messages={'required': _('Please enter a title')},)
    organisations = forms.CharField(
                help_text=_('Comma separated if entering more than one organisation'),               
                required=True,
                error_messages={'required': _('Please enter at least one organisation')},)
    description = forms.CharField(
                widget=forms.Textarea,
                required=True,
                error_messages={'required': _('Please enter a description')},)
    image = forms.ImageField(
                required=False,
                error_messages={},)
    file = forms.FileField(
                required=False,
                error_messages={},)
    url = forms.CharField(
                required=False,
                error_messages={},)
    health_topic = forms.MultipleChoiceField(
                        label=_(u'Health domain'),
                        widget=forms.CheckboxSelectMultiple,
                        required=True,
                        error_messages={'required': _('Please select at least one health domain')},)
    resource_type = forms.MultipleChoiceField(
                        widget=forms.CheckboxSelectMultiple,
                        required=True,
                        error_messages={'required': _('Please select at least one resource type')},)
    audience = forms.MultipleChoiceField(
                        widget=forms.CheckboxSelectMultiple,
                        required=True,
                        error_messages={'required': _('Please select at least one audience')},)
    geography = forms.CharField(
                        required=True,
                        help_text=_('The geographic area the resource is designed for, may be region e.g. ("Africa", "East Africa") or country (e.g. "Ethiopia", "Mali"). Comma separated if entering more than one geography'), 
                        error_messages={'required': _('Please enter at least one geographical area')},)
    languages = forms.CharField(
                        required=True,
                        help_text=_('The languages the resource uses. Comma separated if entering more than one language'), 
                        error_messages={'required': _('Please enter at least one language')},)
    device = forms.MultipleChoiceField(
                        widget=forms.CheckboxSelectMultiple,
                        required=True,
                        error_messages={'required': _('Please select at least one device')},)
    license = forms.ChoiceField(
                        widget=forms.Select,
                        required=True,
                        error_messages={'required': _('Please select a license')},)
    other_tags = forms.CharField(
                        help_text=_('Please enter any other relevant tags for this resource, comma separated if entering more than one tag'),               
                        required=False,
                        )
    terms = forms.BooleanField(
                        label=_(u"Please tick the box to confirm that you have read the <a href='/resource/guidelines/' target='_blank'>guidelines</a> about submitting resources to ORB"),            
                        required=True,
                        error_messages={'required': _('Please tick the box to confirm that you have read the guidelines for submitting resources to ORB')})
    study_time_number = forms.IntegerField(
                            required=False,
                            label="",)
    study_time_unit = forms.CharField(
                                        label="",
                                        widget=forms.Select(choices=Resource.STUDY_TIME_UNITS),
                                        required=False,)

    
    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
                'title',
                'organisations',
                'description',
                'image',
                Row (HTML('<hr>')),
                Row (HTML(_(u'<p class="col-lg-offset-2">Please either upload a file and/or submit a url. Our preference is that the actual resource file is uploaded, but if you submit a url, please ensure this is a direct download for the resource.</p>'))),
                'file',
                'url',
                Row (HTML('<hr>')),
                'health_topic',
                Row (HTML('<hr>')),
                'resource_type',
                Row (HTML('<hr>')),
                Div( 
                    Div( 
                        HTML('<label class="control-label" style="float:right; padding-right:10px;">Study Time</label>'), 
                        css_class='col-lg-2 ' 
                    ), 
                    Div( 
                        Field('study_time_number'), 
                        css_class='col-lg-2' 
                    ), 
                    Div( 
                        Field('study_time_unit'), 
                        css_class='col-lg-2'
                    ), 
                    css_class='row', 
                ),
                Row (HTML('<hr>')),
                'audience',
                Row (HTML('<hr>')),
                'geography',
                Row (HTML('<hr>')),
                'languages',
                Row (HTML('<hr>')),
                'device',
                Row (HTML('<hr>')),
                'license',
                Row (HTML('<hr>')),
                'other_tags',
                Row (HTML('<hr>')),
                'terms',
                Row (HTML('<hr>')),
                Div(
                   Submit('submit', _(u'Submit'), css_class='btn btn-default'),
                   css_class='col-lg-offset-2 col-lg-8',
                ),
            )
        
    def clean(self):
        cleaned_data = self.cleaned_data
        file = cleaned_data.get("file")
        url = cleaned_data.get("url")
        
        if self._errors:
            raise forms.ValidationError( _(u"Please correct the errors below and resubmit the form."))
        if file is None and not url:
            raise forms.ValidationError( _(u"Please submit a file and/or a url for this resource"))
        if cleaned_data.get("study_time_number") is not None and cleaned_data.get("study_time_number") != 0 and cleaned_data.get("study_time_unit") is None:
            raise forms.ValidationError( _(u"You have entered a study time, but not selected a unit."))
            
        
        return self.cleaned_data
    
    def clean_file(self):
        file = self.cleaned_data['file']
        try:
            if file:
                file_type = file.content_type.split('/')[0]

                if len(file.name.split('.')) == 1:
                    raise forms.ValidationError(_(u'File type is not supported'))

                if file_type in settings.TASK_UPLOAD_FILE_TYPES:
                    if file._size > settings.TASK_UPLOAD_FILE_MAX_SIZE:
                        raise forms.ValidationError(_(u'Please keep filesize under %(max_size)s. Current filesize %(actual_size)s') % {'max_size':filesizeformat(settings.TASK_UPLOAD_FILE_MAX_SIZE), 'actual_size': filesizeformat(file._size)})
                else:
                    raise forms.ValidationError(_(u'File type is not supported'))
        except:
            pass

        return file
    
    def clean_url(self):
        url = self.cleaned_data['url']
        validate = URLValidator()
        if url:
            print "checking url" 
            try:
                validate(url)
            except ValidationError:
                raise forms.ValidationError( _(u"This does not appear to be a valid Url"))
        return url
        
class SearchForm(forms.Form): 
    q = forms.CharField(
                required=True,
                error_messages={'required': _('Please enter something to search for')},)
    
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_method = "GET"
        self.helper.form_class = 'form-horizontal'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
                FieldWithButtons('q',Submit('submit', _(u'Go'), css_class='btn btn-default')),
            )
        
class HeaderSearchForm(forms.Form): 
    q = forms.CharField(label="Search:",
                required=False,
                error_messages={'required': _('Please enter something to search for')},)
    
    def __init__(self, *args, **kwargs):
        super(HeaderSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "GET"
        self.helper.form_action = 'orb_search'
        self.helper.form_show_labels = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-1'
        self.helper.field_class = 'col-lg-4 navbar-right'
        self.helper.layout = Layout(
                                    FieldWithButtons('q',Submit('submit', _(u'Search'), css_class='btn btn-default')),
                                    )
        
class TagFilterForm(forms.Form):
    health_topic = forms.MultipleChoiceField(
                        widget=forms.CheckboxSelectMultiple,
                        required=False,)
    resource_type = forms.MultipleChoiceField(
                        widget=forms.CheckboxSelectMultiple,
                        required=False,)
    audience = forms.MultipleChoiceField(
                        widget=forms.CheckboxSelectMultiple,
                        required=False,)
    geography = forms.MultipleChoiceField(
                        widget=forms.CheckboxSelectMultiple,
                        required=False,)
    language = forms.MultipleChoiceField(
                        widget=forms.CheckboxSelectMultiple,
                        required=False,)
    device = forms.MultipleChoiceField(
                        widget=forms.CheckboxSelectMultiple,
                        required=False,)
    license = forms.MultipleChoiceField(
                        widget=forms.CheckboxSelectMultiple,
                        required=False,)
    
    def __init__(self, *args, **kwargs):
        super(TagFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        #self.helper.form_method = "GET"
        #self.helper.form_action = 'orb_tags_filter_results'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
                'health_topic',
                Row (HTML('<hr>')),
                'resource_type',
                Row (HTML('<hr>')),
                'audience',
                Row (HTML('<hr>')),
                'geography',
                Row (HTML('<hr>')),
                'language',
                Row (HTML('<hr>')),
                'device',
                Row (HTML('<hr>')),
                'license',
                Row (HTML('<hr>')),
                Div(
                   Submit('submit', _(u'Go'), css_class='btn btn-default'),
                   css_class='col-lg-offset-2 col-lg-8',
                ),
            )
    def clean(self):
        empty = True
        
        for name,slug in settings.TAG_FILTER_CATEGORIES:
            tag_ids = self.cleaned_data.get(name)
            if tag_ids:
                empty = False
        
        if empty:
            raise forms.ValidationError( _(u"Please select at least one tag to filter on"))
            
        return self.cleaned_data
    
class ResourceRejectForm(forms.Form):
    criteria = forms.MultipleChoiceField(
                        widget=forms.CheckboxSelectMultiple,
                        required=True,)
    notes = forms.CharField(
                    widget=forms.Textarea,
                    required=True,
                    error_messages={'required': _('Please enter a reason as to why the resource has been rejected')},
                    help_text = _('The text you enter here will be included in the email to the submitter of the resource, so please bear this in mind when explaining your reasoning.'),
                    label=_(u"Reason for rejection")
                    )
    
    def __init__(self, *args, **kwargs):
        super(ResourceRejectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
                                    'criteria',
                                    'notes',
                                    Div(
                                       Submit('submit', _(u'Submit'), css_class='btn btn-default'),
                                       css_class='col-lg-offset-2 col-lg-8',
                                    ),
                                )