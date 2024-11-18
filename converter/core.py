import click
from converter.registry import Registry
import os
import sys


@click.command()
@click.argument('input_file')
@click.argument('output_file')
def convert(input_file, output_file):
    """Convert a file from one format to another."""
    try:
        if not os.path.exists(input_file):
            error(f"Input file {input_file} does not exist.")

        if os.path.exists(output_file):
            # Prompt the user to confirm overwriting
            confirm = input(
                f"Target file '{output_file}' already exists. "
                "Do you want to overwrite it? (y/n): "
            ).strip().lower()
            if confirm != 'y':
                print("Operation cancelled.")
                return

        registry = Registry()
        module = registry.find_module(input_file, output_file)
        if not module:
            error(f"No module found to handle {input_file} -> {output_file}")
        module.convert(input_file, output_file)
        success(f"Converted {input_file} to {output_file}")
    except Exception as e:
        error(f"An error occurred: {e}")


def success(msg):
    click.echo(click.style(msg, fg='green'), None, True, True, True)


def error(msg):
    click.echo(click.style(msg, fg='red'), None, True, True, True)
    sys.exit(1)


if __name__ == "__main__":
    convert()
