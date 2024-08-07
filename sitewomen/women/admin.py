from django.contrib import admin, messages

from .models import Women, Category


class MarriedFilter(admin.SimpleListFilter):
    title = 'Married status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Married'),
            ('single', 'Not married'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'cat', 'tags']
    # readonly_fields = ['slug']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    # filter_vertical = ('tags',)

    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('title',)
    ordering = ('-time_create', 'title')
    list_editable = ('is_published',)
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'cat__name',]
    list_filter = [MarriedFilter, 'cat__name', 'is_published',]

    @admin.display(description='Info', ordering='content')
    def brief_info(self, women: Women):
        return f"Описание {len(women.content)} символов"

    @admin.action(description='Publish selected posts')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f'Edited posts: {count}')

    @admin.action(description='Draft selected posts')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f'Edited posts: {count}', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

# OR:
# admin.site.register(Women, WomenAdmin)
