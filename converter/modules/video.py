import ffmpeg

SUPPORTED_FORMATS = {
    "input": [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm", ".gif"],
    "output": [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm", ".gif"]
}


def convert(input_file, output_file):
    ffmpeg.input(input_file).output(output_file).run()
