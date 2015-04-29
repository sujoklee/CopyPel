from __future__ import unicode_literals
import json
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.forms.util import flatatt


class ChoiceFieldRenderer(widgets.ChoiceFieldRenderer):
    def render(self):
        """
        Outputs a <ul ng-form="name"> for this set of choice fields to nest an ngForm.
        """
        output = ['<ul>']
        for widget in self:
            output.append(format_html('<li>{0}</li>', force_text(widget)))
        output.append('</ul>')
        return mark_safe('\n'.join(output))


class CheckboxChoiceInput(widgets.CheckboxChoiceInput):
    def tag(self):
        name = self.name
        tag_attrs = dict(self.attrs, type=self.input_type, name=name, value=self.choice_value)
        if 'id' in self.attrs:
            tag_attrs['id'] = '{0}_{1}'.format(self.attrs['id'], self.index)
        if 'checklist-model' in self.attrs:
            tag_attrs['checklist-value'] = '{0}'.format(self.choice_value)
        if self.is_checked():
            tag_attrs['checked'] = 'checked'
        return format_html('<input{0} />', flatatt(tag_attrs))


class CheckboxFieldRenderer(ChoiceFieldRenderer):
    choice_input_class = CheckboxChoiceInput


class CheckboxSelectMultiple(widgets.CheckboxSelectMultiple):
    """
    Form fields of type 'MultipleChoiceField' using the widget 'CheckboxSelectMultiple' must behave
    slightly different from the original. This widget overrides the default functionality.
    """
    renderer = CheckboxFieldRenderer
