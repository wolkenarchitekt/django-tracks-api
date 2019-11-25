# ID3 tags for humans
import logging
from dataclasses import dataclass, field
from enum import Enum
from io import BytesIO

from mutagen.id3 import APIC, COMM, GEOB, ID3, POPM, TBPM, TKEY, PictureType
from mutagen.id3._frames import TIT2, TLEN, TOFN, TPE1
from mutagen.mp3 import MP3
from PIL import Image

logger = logging.getLogger(__name__)

ID3_TPE1 = 'TPE1'  # Lead Artist/Performer/Soloist/Group
ID3_TIT2 = 'TIT2'  # Title
ID3_TLEN = 'TLEN'  # Audio Length (ms)
ID3_APIC = 'APIC'  # Attached (or linked) Picture.
ID3_POPM = 'POPM'  # Popularimeter
ID3_TBPM = 'TBPM'  # Beats per minute
ID3_TKEY = 'TKEY'  # Starting Key
ID3_TOFN = 'TOFN'  # Original Filename
ID3_COMM = 'COMM'  # Comment
ID3_GEOB = 'GEOB'  # General encapsulated object (binary data)


class MimeType(Enum):
    JPG = 'image/jpeg'
    PNG = 'image/png'


GEOB_FINGERPRINT = 'fingerprint'
GEOB_TRAKTOR_AUDIO_ID = 'traktor_audio_id'


@dataclass
class Id3Image:
    """ ID3 APIC Image wrapper """
    desc: str
    data: bytes
    extension: str = field(init=False, repr=False)
    mime: str = field(init=False, repr=False)
    enc: int = 3
    type: PictureType = PictureType.BAND

    def __post_init__(self):
        pil_image = Image.open(BytesIO(self.data))
        self.extension = pil_image.format.lower()
        self.mime = f'image/{self.extension}'

    def to_apic(self):
        return APIC(
            desc=self.desc,
            encoding=self.enc,
            mime=self.mime,
            type=self.type,
            data=self.data
        )


class SimpleID3(ID3):
    """ Get and set common ID3 attributes """

    def __init__(self, filename):
        super().__init__(filename)
        mp3info = MP3(filename).info
        self[ID3_TLEN] = TLEN(text=str(mp3info.length))
        self.bitrate = int(mp3info.bitrate / 1000)
        self.bitrate_mode = mp3info.bitrate_mode

    @property
    def artist(self) -> str:
        artist = self.get(ID3_TPE1)
        return artist[0] if artist else None

    @artist.setter
    def artist(self, artist: str):
        self[ID3_TPE1] = TPE1(text=artist)

    @property
    def title(self) -> str:
        title = self.get(ID3_TIT2)
        return title[0] if title else None

    @title.setter
    def title(self, title: str):
        self[ID3_TIT2] = TIT2(text=title)

    @property
    def comment(self) -> str:
        comment = self.getall(ID3_COMM)
        return comment[0].text[0] if comment else ''

    @comment.setter
    def comment(self, comment: str):
        self.setall(ID3_COMM, [COMM(text=comment, lang='eng')])

    @property
    def images(self) -> [Id3Image]:
        images = []
        for apic in ID3(self.filename).getall(ID3_APIC):
            try:
                id3image = Id3Image(
                    desc=apic.desc,
                    data=apic.data,
                    type=apic.type,
                )
                images.append(id3image)
            except OSError as error:
                logger.warning(f"Invalid image data: {error}")
                continue
        return images

    @images.setter
    def images(self, id3_images: [Id3Image]):
        self.setall(ID3_APIC, [image.to_apic() for image in id3_images])

    @property
    def rating(self):
        rating = self.getall(ID3_POPM)
        if rating:
            rating = rating[0].rating
            return int(rating / 51)
        return None

    @rating.setter
    def rating(self, rating: int):
        popm = POPM(email='traktor@native-instruments.de', rating=rating * 51, count=0)
        self[ID3_POPM] = popm

    @property
    def bpm(self) -> int:
        bpm = self.get(ID3_TBPM)
        if bpm:
            try:
                return int(bpm.text[0])
            except ValueError:
                pass

    @bpm.setter
    def bpm(self, bpm: int):
        self[ID3_TBPM] = TBPM(text=str(bpm))

    @property
    def key(self) -> int:
        key = self.get(ID3_TKEY)
        return key.text[0] if key else None

    @key.setter
    def key(self, key: str):
        self[ID3_TKEY] = TKEY(text=key)

    @property
    def duration(self) -> float:
        # Duration in milliseconds
        return float(self[ID3_TLEN].text[0])

    @property
    def original_filename(self):
        tofn = self.get(ID3_TOFN)
        if tofn:
            return tofn[0].text

    @original_filename.setter
    def original_filename(self, filename):
        self[ID3_TOFN] = TOFN(text=filename)

    def _set_geob(self, key, data):
        geob = GEOB(desc=key, data=data)
        self.add(geob)

    def _get_geob(self, key):
        data = [geob_obj.data.decode() for geob_obj in self.getall(ID3_GEOB)
                if geob_obj.desc == key]
        return data[0] if data else None

    @property
    def fingerprint(self):
        return self._get_geob(GEOB_FINGERPRINT)

    @fingerprint.setter
    def fingerprint(self, fingerprint: str):
        self._set_geob(GEOB_FINGERPRINT, fingerprint.encode())

    @property
    def traktor_audio_id(self):
        return self._get_geob(GEOB_TRAKTOR_AUDIO_ID)

    @traktor_audio_id.setter
    def traktor_audio_id(self, traktor_audio_id: str):
        self._set_geob(GEOB_TRAKTOR_AUDIO_ID, traktor_audio_id.encode())
