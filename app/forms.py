import json
from django import forms
from app.models import Post
from app.widgets import EditorJSField


class PostAdminForm(forms.ModelForm):
    content_editor = EditorJSField(
        required=False,
        help_text='Не добавляйте изображения до сохранения записи'
        )
    post_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Post
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.initial['post_id'] = self.instance.pk

        # Преобразуем JSON в строку для начальных данных
        if self.instance.pk and self.instance.content:
            self.initial['content_editor'] = json.dumps(self.instance.content)

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Преобразуем строку обратно в JSON
        if self.cleaned_data.get('content_editor'):
            try:
                instance.content = json.loads(
                    self.cleaned_data['content_editor']
                )
            except json.JSONDecodeError:
                instance.content = {}

        if commit:
            instance.save()
        return instance
