import subprocess

# SMPTE25 frame > ms
# ms = (FF / 25) * 1000
# ffmpeg
# -ss absolute start timecode
# -to absolute end timecode
# -c copy without recoding

source_file = "022A-C0324X10X01X-0100M0.mp4"
split_file = "test_ouput_1.mp4"

smpte_tc_in = "00:01:01:24"
smpte_tc_out = "00:01:25:22"


def timecode_split(input_file, tc_in, tc_out, output_file):
    subprocess.call(
        [
            "ffmpeg",
            "-i",
            input_file,
            "-ss",
            tc_in,
            "-to",
            tc_out,
            "-c",
            "copy",
            output_file,
        ]
    )


def frames_to_ms(smpte_tc) -> int:
    separator = ":"
    tc_array = smpte_tc.split(separator)
    ff = int(tc_array.pop())
    ms = int((ff / 25) * 1000)
    tc_array.append(str(ms))
    hh_mm_ss_ms = separator.join(tc_array)
    print(hh_mm_ss_ms)

    return ms


ms_tc_in = frames_to_ms(smpte_tc_in)
ms_tc_out = frames_to_ms(smpte_tc_out)

# timecode_split(source_file, smpte_tc_in, smpte_tc_out, split_file)
