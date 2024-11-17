import ffmpeg

SUPPORTED_FORMATS = {
    "input": [".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a"],
    "output": [".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a"]
}

def convert(input_file, output_file):
    ffmpeg.input(input_file).output(output_file).run()