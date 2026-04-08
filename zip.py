import os
import zipfile
import unicodedata

def normalize_turkish_name(name):
    translation_table = str.maketrans({
        'ç': 'c', 'Ç': 'C',
        'ğ': 'g', 'Ğ': 'G',
        'ı': 'i', 'İ': 'I',
        'ö': 'o', 'Ö': 'O',
        'ş': 's', 'Ş': 'S',
        'ü': 'u', 'Ü': 'U'
    })
    return name.translate(translation_table)

def rename_turkish_zips(root_folder):
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith('.zip'):
                new_name = normalize_turkish_name(filename)
                if new_name != filename:
                    old_path = os.path.join(dirpath, filename)
                    new_path = os.path.join(dirpath, new_name)
                    os.rename(old_path, new_path)
                    print(f"Renamed: {filename} → {new_name}")

def extract_all_zip_files(root_folder):
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith(".zip"):
                zip_path = os.path.join(dirpath, filename)
                extract_folder = os.path.join(dirpath, filename[:-4])
                os.makedirs(extract_folder, exist_ok=True)
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_folder)
                    print(f"✅ Extracted: {zip_path}")
                except zipfile.BadZipFile:
                    print(f"❌ Still bad zip file: {zip_path}")

# Example usage:
root_folder = "CS410 Midterm1 Student Papers"
rename_turkish_zips(root_folder)
extract_all_zip_files(root_folder)
