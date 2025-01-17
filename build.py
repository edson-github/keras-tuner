import glob
import os
import shutil

import namex

package = "keras_tuner"
build_directory = "build"
if os.path.exists(build_directory):
    raise ValueError(f"Directory already exists: {build_directory}")

# Copy sources (`keras_tuner/` directory and setup files) to build directory
os.mkdir(build_directory)
shutil.copytree(package, os.path.join(build_directory, package))
shutil.copy("setup.py", os.path.join(f"{build_directory}", "setup.py"))
shutil.copy("setup.cfg", os.path.join(f"{build_directory}", "setup.cfg"))
os.chdir(build_directory)

# Restructure the codebase so that source files live in `keras_tuner/src`
namex.convert_codebase(package, code_directory="src")
# Generate API __init__.py files in `keras_tuner/`
namex.generate_api_files(package, code_directory="src", verbose=True)

# Make sure to export the __version__ string
from keras_tuner.src import __version__  # noqa: E402

with open(os.path.join(package, "__init__.py")) as f:
    init_contents = f.read()
with open(os.path.join(package, "__init__.py"), "w") as f:
    f.write(init_contents + "\n\n" + f'__version__ = "{__version__}"\n')

# Build the package
os.system("python3 -m build")

# Save the dist files generated by the build process
os.chdir("..")
if not os.path.exists("dist"):
    os.mkdir("dist")
for filename in glob.glob(os.path.join(build_directory, "dist", "*.*")):
    shutil.copy(filename, "dist")

# Clean up: remove the build directory (no longer needed)
shutil.rmtree(build_directory)
