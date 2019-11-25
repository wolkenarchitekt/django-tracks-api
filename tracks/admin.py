import datetime
import logging
import re
from urllib.parse import urljoin

from django import forms
from django.conf import settings
from django.contrib import admin, messages
from django.db import models
from django.db.models import Count
from django.forms import widgets
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from inline_actions.admin import (InlineActionsMixin,
                                  InlineActionsModelAdminMixin)

from tracks.models import Track, TrackImage

logger = logging.getLogger(__name__)


class TrackFileWidget(forms.FileInput):
    def __init__(self, *args, **kwargs):
        super(TrackFileWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        return format_html(f"""<button onclick="play(`{value.url}`, event)">Play</button>""")


class TrackImageInline(InlineActionsMixin, admin.StackedInline):
    fields = (
        'image',
        'image_tag',
        'desc',
        'width',
        'height',
    )
    model = TrackImage
    readonly_fields = ('image_tag', 'desc', 'width', 'height')
    inline_actions = ['set_primary']
    ordering = ('-width', '-height')

    formfield_overrides = {
        models.TextField: {'widget': widgets.Textarea(attrs={'rows': 1})}
    }

    def image_tag(self, obj: TrackImage):
        return format_html(f'<div><img style="width: 50%" src="{obj.image.url}"/>')
    image_tag.short_description = 'Image'

    def set_primary(self, request, obj, parent_obj):
        obj.track.images.exclude(pk=obj.pk).delete()
        messages.info(request, "Image set as primary image")
        obj.track.db_to_id3()
        url = reverse('admin:tracks_track_changelist')
        return redirect(url)

    set_primary.short_description = "Set as primary image"


class TrackImageListFilter(admin.SimpleListFilter):
    title = 'Has track image'
    parameter_name = 'has_image'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no',  'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(images__count__gt=0)

        if self.value() == 'no':
            return queryset.filter(images__count=0)


class TrackAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    list_display = (
        'image_tag',
        'audio_tag',
        'track_id',
        'artist',
        'title',
        'rating',
        'bpm',
        'key',
        'formatted_duration',
        'bitrate',
        'bitrate_mode',
        'file_mtime',
        'file',
    )

    list_filter = [TrackImageListFilter, ]
    exclude = ['duration']
    inlines = [TrackImageInline]
    list_display_links = ('track_id', )

    change_form_template = 'tracks/track/change_form.html'
    change_list_template = 'tracks/track/change_list.html'

    search_fields = ('artist', 'title', 'comment')
    readonly_fields = ('file_mtime', 'formatted_duration', 'bpm', 'key', 'bitrate',
                       'bitrate_mode', 'finger_print')

    formfield_overrides = {
        models.FileField: {'widget': TrackFileWidget},
        models.TextField: {'widget': widgets.Textarea(attrs={'rows': 10})},
    }

    def formatted_duration(self, obj):
        td = datetime.timedelta(seconds=int(obj.duration))
        return td
    formatted_duration.short_description = 'Duration'

    def get_queryset(self, request):
        qs = super(TrackAdmin, self).get_queryset(request)
        qs = qs.prefetch_related('images').annotate(Count('images'))
        return qs

    def save_model(self, request, obj: Track, form, change):
        if change:
            obj.db_to_id3()
        obj.save()

    def image_tag(self, obj: Track):
        if obj.images.count():
            url = obj.images.all()[0].image.url
            return format_html(f'<a href="{url}"><img src="{url}" width="256"/></a>')
    image_tag.short_description = 'Image'

    def audio_tag(self, obj):
        return format_html(f"""<button onclick="play(`{obj.file.url}`, event)">Play</button>""")
    audio_tag.short_description = 'Audio'


admin.site.site_header = 'Django Tracks'
admin.site.register(Track, TrackAdmin)
