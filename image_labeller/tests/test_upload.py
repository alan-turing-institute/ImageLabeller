"""
Test the file uploading functions
"""

from ..admin.admin_utils import *

def test_allowed_filename():
    assert(allowed_file("myfile.json"))
    assert(allowed_file("myfile.png"))
    assert(allowed_file("myfile.zip"))
    assert(allowed_file("myfile.JSON"))
    assert(allowed_file("myfile.PNG"))
    assert(allowed_file("myfile.ZIP"))
    assert( not allowed_file("no_extension"))
    assert( not allowed_file("myfile.py"))
    assert( not allowed_file("myfile.php"))
