import zipfile
from pathlib import Path

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
            z.extractall(extract_to)

            # Find the top-level directory inside the zip
            top_level_dirs = {Path(name).parts[0] for name in z.namelist() if len(Path(name).parts) > 1}
            if not top_level_dirs:
                raise ValueError("Could not determine top-level folder.")
            top_dir = extract_to / list(top_level_dirs)[0]

        # Should contain these directories inside top level directory
        ref_path = top_dir / "reference"
        synth_path = top_dir / "synthesis"

        if ref_path.is_dir() and synth_path.is_dir():
            print("Both required folders found")
        else:
            print("Missing folders after extraction.")
            if not ref_path.is_dir():
                print("Missing folder: reference")
            if not synth_path.is_dir():
                print("Missing folder: synthesis")

    except FileNotFoundError:
        print("File not found. Please check the path and try again.")
    except zipfile.BadZipFile:
        print("That’s not a valid ZIP file.")
    except Exception as e:
        print(f"Error: {e}")

