import datetime
from urllib.parse import urljoin

from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from tracks_api.models import Track


class TrackAdmin(admin.ModelAdmin):
    list_display = (
        "image_tag",
        "audio_tag",
        "artist",
        "title",
        "bpm",
        "key",
        "duration_formatted",
        "bitrate_formatted",
        "file",
    )

    list_display_links = ('artist',)
    search_fields = ("artist", "title")
    change_form_template = 'tracks/track/change_form.html'
    change_list_template = 'tracks/track/change_list.html'

    def get_ordering(self, request):
        return ['-file_mtime', ]

    def duration_formatted(self, obj):
        td = datetime.timedelta(seconds=int(obj.duration))
        return td
    duration_formatted.short_description = "Duration"

    def bitrate_formatted(self, obj):
        return f"{int(obj.bitrate / 1000)}K"
    bitrate_formatted.short_description = "Bitrate"

    def audio_tag(self, obj):
        url = urljoin('/media/', obj.file.url)
        return format_html(f"""<button onclick="play(`{url}`, event)">Play</button>""")
    audio_tag.short_description = 'Audio'

    def image_tag(self, obj: Track):
        image = obj.images.first()
        if image:
            url = urljoin(settings.MEDIA_ROOT, image.image.url)
            return format_html(f'<a href="{url}"><img src="{url}" width="64"/></a>')
    image_tag.short_description = 'Image'


admin.site.site_header = "Django Tracks API"
admin.site.register(Track, TrackAdmin)
