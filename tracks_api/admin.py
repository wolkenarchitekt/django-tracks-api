from django import forms
import datetime
from urllib.parse import urljoin

from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from tracks_api.models import Track


class TrackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['artist'].widget = admin.widgets.AdminTextareaWidget(attrs={'rows': 1})
        self.fields['title'].widget = admin.widgets.AdminTextareaWidget(attrs={'rows': 1})
        self.fields['key'].widget = admin.widgets.AdminTextareaWidget(attrs={'rows': 1})


class TrackAdmin(admin.ModelAdmin):
    list_display = (
        "image_tag",
        "audio_tag",
        "artist",
        "title",
        "bpm",
        "key",
        "rating_formatted",
        "duration_formatted",
        "bitrate_formatted",
        "file",
    )

    form = TrackForm

    list_display_links = ("artist",)
    search_fields = ("artist", "title")
    change_form_template = "tracks/track/change_form.html"
    change_list_template = "tracks/track/change_list.html"
    fields = (
        "artist",
        "title",
        "key",
    )

    def get_ordering(self, request):
        return ["-file_mtime"]

    def duration_formatted(self, obj):
        td = datetime.timedelta(seconds=int(obj.duration))
        return td
    duration_formatted.short_description = "Duration"

    def bitrate_formatted(self, obj):
        return f"{int(obj.bitrate / 1000)}K"

    bitrate_formatted.short_description = "Bitrate"

    def rating_formatted(self, obj):
        rating = obj.ratings.first()
        if rating:
            return int(rating.rating / 51)

    rating_formatted.short_description = "Rating"

    def audio_tag(self, obj):
        url = urljoin(settings.MEDIA_ROOT, obj.file.url)
        return format_html(f"""<button onclick="play(`{url}`, event)">Play</button>""")

    audio_tag.short_description = "Audio"

    def image_tag(self, obj: Track):
        image = obj.images.first()
        if image:
            url = urljoin(settings.MEDIA_ROOT, image.image.url)
            return format_html(f'<a href="{url}"><img src="{url}" width="64"/></a>')

    image_tag.short_description = "Image"


admin.site.site_header = "Django Tracks API"
admin.site.register(Track, TrackAdmin)
