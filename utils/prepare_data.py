import zipfile
from pathlib import Path
import sys

def input_zip():
    zip_file_path = input("Enter full path to zip file: ").strip()
    extract_path = input("Enter full path to unzip file: ").strip()
    unzip_and_prepare(zip_file_path, extract_path)

def unzip_and_prepare(zip_file_path, extract_path):
    extract_to = Path(extract_path)
    try:
        if not zipfile.is_zipfile(zip_file_path):
            raise ValueError("Provided file is not a valid ZIP file.")

        with zipfile.ZipFile(zip_file_path, 'r') as z:
            print("Contents of the ZIP file:")
            print(z.namelist())

            # Find the top-level directory inside the zip
            # Only consider names that have at least one "/" indicating a subfolder
            top_level_dirs = {Path(name).parts[0] for name in z.namelist() if len(Path(name).parts) > 1}
            if not top_level_dirs:
                raise ValueError("Could not determine top-level folder.")
            top_dir = list(top_level_dirs)[0]

            # Check for 'reference' and 'synthesis' folders inside the top-level directory
            ref_prefix = f"{top_dir}/reference/"
            synth_prefix = f"{top_dir}/synthesis/"

            # Collect files in reference and synthesis folders inside the zip
            ref_files = [name for name in z.namelist() if name.startswith(ref_prefix) and not name.endswith('/')]
            synth_files = [name for name in z.namelist() if name.startswith(synth_prefix) and not name.endswith('/')]

            if not ref_files:
                print("Missing 'reference' folder or it's empty inside the ZIP.")
                return
            if not synth_files:
                print("Missing 'synthesis' folder or it's empty inside the ZIP.")
                return

            # Check number of files
            if len(ref_files) != len(synth_files):
                print("Both 'reference' and 'synthesis' folders should have the same number of files.")
                return

            # Check that all files end with .wav (case insensitive)
            if not all(name.lower().endswith('.wav') for name in ref_files):
                print("Warning - All files in 'reference' folder should end with .wav extension.")
                return
            if not all(name.lower().endswith('.wav') for name in synth_files):
                print("Warning - All files in 'synthesis' folder should end with .wav extension.")
                return

            # If all checks passed, extract the zip
            z.extractall(extract_to)
            print("Extraction completed successfully.")

    except FileNotFoundError:
        print("File not found. Please check the path and try again.")
    except zipfile.BadZipFile:
        print("That’s not a valid ZIP file.")
    except Exception as e:
        print(f"Error: {e}")


def list_files(directory):
    isdir = Path(directory)
    if not isdir.is_dir():
        return []
    else:
        return [f for f in isdir.rglob('*') if f.is_file()]