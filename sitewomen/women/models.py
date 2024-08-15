from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


def translit_to_eng(s: str) -> str:
    """
    Transliteration of Russian text into English letters for making slugs
    :param s: Russian text
    :return: Transliterated text
    """
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
         'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
         'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
         'ю': 'yu', 'я': 'ya'}
    return ''.join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, validators=[
                               MinLengthValidator(5, message='Минимум 5 символов'),
                               MaxLengthValidator(100, message='Максимум 100 символов'),
                           ])
    content = models.TextField(blank=True)  # blank=True - поле может быть пустым
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT)
    cat = models.ForeignKey(to='Category', on_delete=models.PROTECT, related_name='posts')
    tags = models.ManyToManyField(to='TagPost', related_name='tags')
    husband = models.OneToOneField(to='Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='women',
                                   verbose_name='Husband')
    published = PublishedManager()
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Famous Woman'
        verbose_name_plural = 'Famous Women'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit_to_eng(str(self.title)))
    #     super().save(*args, **kwargs)


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)
    objects = models.Manager()

    def __str__(self):
        return self.name


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True)
    objects = models.Manager()

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})
