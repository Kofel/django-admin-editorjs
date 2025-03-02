from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class EditorJSWidget(forms.TextInput):

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = '{}'

        if attrs is None:
            attrs = {}

        context = {
            'widget': {
                'name': name,
                'value': value,
                'attrs': attrs,
            }
        }

        html = render_to_string('widgets/editorjs.tmpl', context)
        return mark_safe(html)

    class Media:
        css = {
            'all': ('admin/css/editorjs.css',)
        }
        js = (
            'https://cdn.jsdelivr.net/npm/@editorjs/editorjs@2.30.8',
            'https://cdn.jsdelivr.net/npm/@editorjs/header@2.8.8',
            'https://cdn.jsdelivr.net/npm/@editorjs/list@2.0.4',
            'https://cdn.jsdelivr.net/npm/@editorjs/paragraph@2.11.7',
            'https://cdn.jsdelivr.net/npm/@editorjs/image@2.10.2',
            'https://cdn.jsdelivr.net/npm/@editorjs/code@2.9.3',
            'https://cdn.jsdelivr.net/npm/@editorjs/inline-code@1.5.1',
            'https://cdn.jsdelivr.net/npm/@editorjs/table@2.4.3',
            'https://cdn.jsdelivr.net/npm/@editorjs/underline@1.2.1',
            'https://cdn.jsdelivr.net/npm/@editorjs/raw@2.5.1',
            'admin/js/editorjs_init.js',
        )

    def get_template_name(self):
        return self.template_name


class EditorJSField(forms.CharField):
    widget = EditorJSWidget()
