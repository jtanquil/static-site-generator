import os, shutil

from copy_static import copy_recursive
from generate_static import generate_page

if __name__ == "__main__":
  source_path = "./static"
  destination_path = "./public"

  # remove files from destination_path to keep test runs idempotent
  if os.path.exists(destination_path):
    shutil.rmtree(destination_path)

  if not os.path.exists(destination_path):
    os.mkdir(destination_path)
  
  print(f"Copying contents of {source_path} into {destination_path}")
  copy_recursive(source_path, destination_path)

  generate_page("./content/index.md", "./template.html", f"{destination_path}/index.html")