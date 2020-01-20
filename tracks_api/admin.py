import datetime
from urllib.parse import urljoin

from django import forms
from django.conf import settings
from django.contrib import admin
from django.db import models
from django.forms import widgets
from django.utils.html import format_html
from tracks_api.models import Track, TrackImage


class ReadonlyTextWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        return format_html(f"""<div class="readonly">{value}</div>""")


class TrackImageInline(admin.StackedInline):
    fields = (
        "image_tag",
        "desc",
    )
    model = TrackImage
    readonly_fields = ("image_tag", "desc")
    extra = 0

    formfield_overrides = {
        models.TextField: {"widget": widgets.Textarea(attrs={"rows": 1})}
    }

    def image_tag(self, obj: TrackImage):
        url = urljoin(settings.MEDIA_ROOT, obj.image.url)
        return format_html(f'<div><img style="width: 50%" src="{url}"/>')

    image_tag.short_description = "Image"  # type: ignore


class TrackForm(forms.ModelForm):
    duration_formatted = forms.CharField(
        widget=ReadonlyTextWidget, required=False, label="Duration"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ["artist", "title", "album"]:
            self.fields[field].widget = admin.widgets.AdminTextareaWidget(
                attrs={"rows": 1}
            )
        instance: Track = kwargs["instance"]
        self.fields["duration_formatted"].initial = datetime.timedelta(
            seconds=int(instance.duration)
        )


class TrackAdmin(admin.ModelAdmin):
    list_display = (
        "image_tag",
        "audio_tag",
        "artist",
        "title",
        "album",
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
    readonly_fields = ("key", "duration")
    fields = (
        "artist",
        "title",
        "album",
        "duration_formatted",
        "key",
    )
    inlines = [
        TrackImageInline,
    ]

    def get_ordering(self, request):
        return ["-file_mtime"]

    def duration_formatted(self, obj):
        td = datetime.timedelta(seconds=int(obj.duration))
        return td

    duration_formatted.short_description = "Duration"  # type: ignore

    def bitrate_formatted(self, obj):
        return f"{int(obj.bitrate / 1000)}K"

    bitrate_formatted.short_description = "Bitrate"  # type: ignore

    def rating_formatted(self, obj):
        rating = obj.ratings.first()
        if rating:
            return int(rating.rating / 51)

    rating_formatted.short_description = "Rating"  # type: ignore

    def audio_tag(self, obj):
        url = urljoin(settings.MEDIA_ROOT, obj.file.url)
        return format_html(f"""<button onclick="play(`{url}`, event)">Play</button>""")

    audio_tag.short_description = "Audio"  # type: ignore

    def image_tag(self, obj: Track):
        image = obj.images.first()
        if image:
            url = urljoin(settings.MEDIA_ROOT, image.image.url)
            return format_html(f'<a href="{url}"><img src="{url}" width="64"/></a>')

    image_tag.short_description = "Image"  # type: ignore


admin.site.site_header = "Django Tracks API"
admin.site.register(Track, TrackAdmin)
