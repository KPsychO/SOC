import subprocess
import os

def convert_markdown_to_pdf(index_file, content_file, output_file):
    # Ensure the files exist
    if not os.path.exists(index_file) or not os.path.exists(content_file):
        print("One or both of the specified Markdown files do not exist.")
        return

    # Construct the command to call Pandoc
    command = [
        'pandoc',
        index_file,
        content_file,
        '-o',
        output_file
    ]

    try:
        # Run the command
        subprocess.run(command, check=True)
        print(f"Successfully converted {index_file} and {content_file} to {output_file}.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while converting to PDF: {e}")

# Specify your markdown files and output PDF
index_md = 'index.md'
content_md = 'content.md'
output_pdf = 'output.pdf'

# Convert the files
convert_markdown_to_pdf(index_md, content_md, output_pdf)
