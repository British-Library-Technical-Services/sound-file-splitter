from rich import print


def welcome_message() -> str:
    message: str = """
    __________________________________________________________________________________

    [bold]WELCOME TO THE[/bold]

    ███████  ██████  ██   ██ ███    ██ ██████   ██████ ██       ██████  ██   ██ ██████     
    ██      ██    ██ ██   ██ ████   ██ ██   ██ ██      ██      ██    ██ ██   ██ ██   ██  
    ███████ ██    ██ ██   ██ ██ ██  ██ ██   ██ ██      ██      ██    ██ ██   ██ ██   ██  
         ██ ██    ██ ██   ██ ██  ██ ██ ██   ██ ██      ██      ██    ██ ██   ██ ██   ██  
    ███████  ██████   █████  ██   ████ ██████   ██████ ███████  ██████   █████  ██████   
                                                                                         
                                                                [bold]FILE SPLITTING SERVICE[/bold]
    __________________________________________________________________________________

The service will split mp4 audio files using the timecode ranges defined in their 
associated METS XML files.

[bold]Requirements:[/bold]
* mp4 and METS xml files stored in the same directory
* [bold]FFMPEG[/bold] installed to the PATH to run

[bold]Outputs:[/bold]
The service will generate a [bold]csv file listing the SMPTE25 timecodes[/bold] extracted from the 
METS and used for each timerange edit. These are generated for ease of reference only 
and are not used for any processing so they can be deleted afterwards if not needed.

The edited files output by the service will be renamed - [bold]"Shelfmark, Title.mp4"[/bold] - and saved to a 
"./split_file_ranges/" sub-directory.

[bold]Service Limits:[/bold]
Any recordings whose Logical Structure do not map Parent/Child time ranges to a single file
cannot currently be processed by the service. These files will be skipped over and a 
list generated at the end for inspection and manual intervention.

[bold][green]Press Enter to start the service[/green][/bold]

A dialog window will open to select the source directory containing the METS XML 
and audio files for processing 

"""

    return message


def source_directory_list(
    directory: str, number_of_xml_files: int, number_of_audio_files: int
) -> str:
    message: str = f"""

Source directory [green]{directory}[/green] selected containing: 
* [bold]{number_of_xml_files}[/bold] XML files
* [bold]{number_of_audio_files}[/bold] mp4 audio files

[green][bold]Press any key[/green][/bold] to continue"""

    return message


def service_information() -> str:
    message: str = """
===| FILES PROCESSING |==="""

    return message


def error_list(file: str) -> str:
    message: str = f"* [red]{file}[/red]"

    return message
