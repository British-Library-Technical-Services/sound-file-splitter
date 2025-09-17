from typing import List
import os
import csv

from datamodels import SoundFileObject


def write_csv_file(file_to_write: str, data_to_write: List[SoundFileObject]) -> bool:
    with open(f"{file_to_write}.csv", "w", newline="") as csv_file:
        data_writer = csv.writer(csv_file, delimiter=",")
        data_writer.writerow(
            [
                "filename",
                "file_id",
                "physical_id",
                "timecode_in",
                "timecode_out",
                "record_title",
            ]
        )
        for data in data_to_write:
            data_writer.writerow(
                [
                    data.filename,
                    data.file_id,
                    data.physical_id,
                    data.timecode_in,
                    data.timecode_out,
                    data.record_title,
                ]
            )
