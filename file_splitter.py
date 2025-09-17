import subprocess
import os

# SMPTE25 frame > ms
# ms = (FF / 25) * 1000
# ffmpeg
# -ss absolute start timecode
# -to absolute end timecode
# -c copy without rencoding


def timecode_split(
    input_file: str, timecode_in: str, timecode_out: str, output_file: str
):
    try:
        subprocess.call(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "panic",
                "-y",
                "-i",
                input_file,
                "-ss",
                timecode_in,
                "-to",
                timecode_out,
                "-c",
                "copy",
                os.path.join("./soundcloud_files/", output_file),
            ]
        )
    except OSError as ose:
        raise "Error calling ffmpeg to split %s - %s" % (input_file, ose)


def convert_frames_to_ms(smpte_timecode: str) -> int:
    separator = ":"
    timecode_array = smpte_timecode.split(separator)
    frames = int(timecode_array.pop())
    ms = int((frames / 25) * 1000)

    hh_mm_ss_ms = f"{separator.join(timecode_array)}.{ms}"  # required time format for ffmpeg is hh:mm:ss.ms

    return hh_mm_ss_ms
