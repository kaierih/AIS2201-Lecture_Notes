src = "../demos"
dst = "demos"

import os
os.symlink(src, dst, target_is_directory=True)