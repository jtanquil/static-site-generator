import unittest, os, shutil, filecmp

from main import copy

def test_path_equality(left_path, right_path):
  comparison = filecmp.dircmp(left_path, right_path)

  # if either the left_only or right_only have elements, return false
  # otherwise, for each new item in common, check left_path/item and right_path item:
  # if it's a directory, make a recursive call
  # if it's a file, check that the files are equal
  # return the and of all comparisons made for all paths
  if len(comparison.left_only) > 0 or len(comparison.right_only) > 0:
    return False
  else:
    subpath_comparisons = []

    for item in comparison.common:
      left_subpath = os.path.join(left_path, item)
      right_subpath = os.path.join(right_path, item)

      if os.path.isfile(left_subpath):
        subpath_comparisons.append(filecmp.cmp(left_subpath, right_subpath))
      else:
        subpath_comparisons.append(test_path_equality(left_subpath, right_subpath))

    return all(subpath_comparisons)


class TestCopy(unittest.TestCase):
  def setUp(self):
    self.source_path = os.path.join(".", "static")
    self.destination_path = os.path.join(".", "public")

  def test_copy(self):
    copy(self.source_path, self.destination_path)

    self.assertTrue(test_path_equality(self.source_path, self.destination_path))

  def tearDown(self):
    destination_subpaths = os.listdir(self.destination_path)

    for subpath in destination_subpaths:
      new_path = os.path.join(self.destination_path, subpath)

      if os.path.isfile(new_path):
        os.remove(new_path)
      else:
        shutil.rmtree(new_path)

if __name__ == "__main__":
  unittest.main()