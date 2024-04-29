import os

from block_html import markdown_to_html_node

def extract_title(markdown):
  if not markdown.startswith("# "):
    raise ValueError("Markdown text must start with a header ('# ...')")
  else:
    return markdown.lstrip("# ").split("\n")[0]

def generate_page(from_path, template_path, dest_path):
  if not os.path.exists(from_path):
    raise FileNotFoundError(f"Source path {from_path} does not exist.")
  elif not os.path.exists(template_path):
    raise FileNotFoundError(f"Template path {template_path} does not exist.")
  else:
    title_placeholder = "{{ Title }}"
    content_placeholder = "{{ Content }}"

    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    source_markdown = ""
    template = ""

    with open(from_path, encoding = "utf-8") as f:
      source_markdown = f.read()

    with open(template_path, encoding = "utf-8") as f:
      template = f.read()

    title = extract_title(source_markdown)
    content = markdown_to_html_node(source_markdown).to_html()

    generated_html = template.replace(title_placeholder, title).replace(content_placeholder, content)

    # make any necessary directories in the destination path
    subdirs = dest_path.split("/")[:-1]

    for i in range(1, len(subdirs)):
      subpath = os.path.join(*subdirs[:i])

      if not os.path.exists(subpath):
        os.mkdir(subpath)
    
    with open(dest_path, "w") as f:
      f.write(generated_html)