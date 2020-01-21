from mediafile import MediaFile
from tracks_api.entities import TrackEntity


def update_id3(instance: TrackEntity):
    """Update ID3 tags from Track instance if changed"""
    modified = False
    from ipdb import set_trace; set_trace()
    mf = MediaFile(instance.file.path)

    for attrib in ["artist", "title", "bpm", "key", "album"]:
        mf_value = getattr(mf, attrib)
        instance_value = getattr(instance, attrib)
        if mf_value != instance_value:
            setattr(mf, attrib, instance_value)
            modified = True

    if modified:
        mf.save()
