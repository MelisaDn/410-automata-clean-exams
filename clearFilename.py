import os
import re
import zipfile
import tempfile
import shutil


def rename_tm_file(file_path):

    filename = os.path.basename(file_path)
    lower_name = filename.lower()

    # Only process .tm files
    if not lower_name.endswith(".tm"):
        return

    new_name = None

    # Detect files containing 1 / 2 / 3
    if re.search(r'1', lower_name):
        new_name = "1.tm"

    elif re.search(r'2', lower_name):
        new_name = "2.tm"

    elif re.search(r'3', lower_name):
        new_name = "3.tm"

    # Rename if needed
    if new_name and filename != new_name:

        new_path = os.path.join(
            os.path.dirname(file_path),
            new_name
        )

        # Avoid overwriting existing file
        if not os.path.exists(new_path):

            os.rename(file_path, new_path)

            print(f"Renamed: {filename} -> {new_name}")

        else:
            print(f"Skipped rename (already exists): {new_name}")


def delete_files(root_folder):

    unwanted_extensions = ('.jar', '.pdf')

    for root, dirs, files in os.walk(root_folder):

        for file in files:

            file_path = os.path.join(root, file)

            # -------------------------------
            # Rename .tm files
            # -------------------------------
            rename_tm_file(file_path)

            # Refresh path after rename
            possible_paths = [
                os.path.join(root, "1.tm"),
                os.path.join(root, "2.tm"),
                os.path.join(root, "3.tm")
            ]

            for p in possible_paths:
                if os.path.exists(p):
                    file_path = p

            # -------------------------------
            # Delete normal files
            # -------------------------------
            if file.lower().endswith(unwanted_extensions):

                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")

                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

            # -------------------------------
            # Clean zip files
            # -------------------------------
            elif file.lower().endswith('.zip'):

                try:

                    with zipfile.ZipFile(file_path, 'r') as zip_ref:

                        unwanted_files = [
                            f for f in zip_ref.namelist()
                            if f.lower().endswith(unwanted_extensions)
                        ]

                        if not unwanted_files:
                            continue

                        print(f"Found {len(unwanted_files)} unwanted files inside {file_path}, removing...")

                        tmp_fd, tmp_name = tempfile.mkstemp(suffix=".zip")
                        os.close(tmp_fd)

                        with zipfile.ZipFile(tmp_name, 'w') as new_zip:

                            for item in zip_ref.infolist():

                                if not item.filename.lower().endswith(unwanted_extensions):

                                    new_zip.writestr(
                                        item,
                                        zip_ref.read(item.filename)
                                    )

                    shutil.move(tmp_name, file_path)

                    print(f"Cleaned .zip: {file_path}")

                except Exception as e:
                    print(f"Error processing zip {file_path}: {e}")


# Example usage
folder_path = "410_quiz5"

delete_files(folder_path)