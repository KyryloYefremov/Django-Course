from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, Women


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ1234567890- '
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Только русские буквы, цифры, символ "-" и пробел'

    def __call__(self, value, *args, **kwargs):
        if not (set(value)) <= set(self.ALLOWED_CHARS):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Category', empty_label='Not selected')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), label='Husband', required=False,
                                     empty_label='Not selected')

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'is_published', 'cat', 'tags', 'husband', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {
            'slug': 'URL',
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Максимум 50 символов')
        return title


class UploadFileForm(forms.Form):
    file = forms.ImageField(label='File')
