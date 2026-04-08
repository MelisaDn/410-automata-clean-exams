import os
import zipfile
import tempfile
import shutil

def delete_jar_files(root_folder):
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)

            # Case 1: Delete normal .jar files
            if file.endswith(".jar"):
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

            # Case 2: Check inside .zip files
            elif file.endswith(".zip"):
                try:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        jar_files = [f for f in zip_ref.namelist() if f.endswith('.jar')]

                        if not jar_files:
                            continue  # skip if no .jar inside

                        print(f"Found {len(jar_files)} .jar files inside {file_path}, removing...")

                        # Create temp zip without .jar files
                        tmp_fd, tmp_name = tempfile.mkstemp(suffix=".zip")
                        os.close(tmp_fd)

                        with zipfile.ZipFile(tmp_name, 'w') as new_zip:
                            for item in zip_ref.infolist():
                                if not item.filename.endswith('.jar'):
                                    new_zip.writestr(item, zip_ref.read(item.filename))

                    # Replace original zip with cleaned one
                    shutil.move(tmp_name, file_path)
                    print(f"Cleaned .zip: {file_path}")

                except Exception as e:
                    print(f"Error processing zip {file_path}: {e}")

# Example usage:
folder_path = "CS410 Mock Exam"
delete_jar_files(folder_path)
