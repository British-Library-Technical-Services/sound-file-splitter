from dataclasses import dataclass


@dataclass
class SoundFileObject:
    filename: str
    file_id: str
    physical_id: str
    timecode_in: str
    timecode_out: str
    record_title: str


@dataclass
class RecordedAreaData:
    physical_id: str
    file_id: str
    timecode_in: str
    timecode_out: str


@dataclass
class RecordTitleData:
    title: str
    physical_id: str
