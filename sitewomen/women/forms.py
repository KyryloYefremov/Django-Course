from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ1234567890- '
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Только русские буквы, цифры, символ "-" и пробел'

    def __call__(self, value, *args, **kwargs):
        if not (set(value)) <= set(self.ALLOWED_CHARS):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.Form):
    title = forms.CharField(min_length=5, max_length=255,
                            label='Заголовок',
                            widget=forms.TextInput(attrs={'class': 'form-input'}),
                            error_messages={
                                'min_length': 'Минимум 5 символов',
                                'required': 'Обязательное поле',
                            },)
    slug = forms.SlugField(max_length=255, label='Slug',
                           validators=[
                               MinLengthValidator(5, message='Минимум 5 символов'),
                               MaxLengthValidator(100, message='Максимум 100 символов'),
                           ])
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), label='Контент', required=False)
    is_published = forms.BooleanField(label='Публикация', initial=True, required=False)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Категория не выбрана')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), label='Муж', required=False,
                                     empty_label='Не замужем')

    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ1234567890- '

        if not set(title) <= set(ALLOWED_CHARS):
            raise ValidationError('Только русские буквы, цифры, символ "-" и пробел')