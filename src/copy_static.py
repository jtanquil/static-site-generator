import os, shutil

# recursively copies everything from source_path into destination_path
def copy_recursive(source_path, destination_path):
  if not os.path.exists(source_path):
    raise ValueError("invalid source path")
  else:
    current_dir = os.listdir(source_path)

    # for each file/directory in the current directory,
    # if it's a file, copy the file into destination_path/file_name
    # if it's a directory, create destination_path/directory_name and
    # call copy(source_path/directory_name, destination_path/directory_name)
    for subpath in current_dir:
      current_dir_path = os.path.join(source_path, subpath)

      print(f"checking {current_dir_path}")

      if os.path.isfile(current_dir_path):
        print(f"{current_dir_path} is a file, copying into {os.path.join(destination_path, subpath)}")
        shutil.copy(current_dir_path, os.path.join(destination_path, subpath))
      else:
        print(f"{current_dir_path} is a directory, calling copy({current_dir_path}, {os.path.join(destination_path, subpath)})")
        os.mkdir(os.path.join(destination_path, subpath))
        copy_recursive(current_dir_path, os.path.join(destination_path, subpath))