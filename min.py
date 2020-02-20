import subprocess
import shutil
import sys
import os

from typing import List, Iterator, Union, Optional

def clear(filename: Union[str, List[str]]) -> None:
	if isinstance(filename, list):
		for fn in filename:
			clear(fn)

	else:
		with open(filename, "w+") as f:
			f.write("")

def files(path: str, ignore: List=[], fullpath: bool=False) -> Iterator[str]:
	for filename in os.listdir(path):
		if filename not in ignore:
			yield (path + filename) if fullpath else filename

def minify_dir(path: str, ignore: List=[], filename: str="") -> Optional[bytes]:
	return minify(
		list(files(path, ignore, fullpath=True)),
		filename
	)

def minify_single(path: str, filename: str="") -> Optional[bytes]:
	return minify([path], filename)

def minify(commands: List[str], filename: str="") -> Optional[bytes]:
	command=["minify"] + commands

	out=subprocess.run(
		command,
		stdout=subprocess.PIPE
	).stdout

	if filename:
		with open(filename, "rb+") as f:
			f.write(out)
	else:
		return out

STATIC_CSS="SHIMON/static/css/"
STATIC_JS="SHIMON/static/js/"
THEMES="SHIMON/templates/themes/"

BUNDLE_JS=STATIC_JS + "bundle.js"
BUNDLE_CSS=STATIC_CSS + "bundle.css"

#force clear given files
clear([
	BUNDLE_JS,
	BUNDLE_CSS,
	STATIC_CSS + "login.css"
])

skipping=len(sys.argv) > 1

if not skipping:
	print("minifying JS")

	for filename in files(STATIC_JS, ignore=["bundle.js"]):
		print("  " + filename)

	minify_dir(
		STATIC_JS,
		ignore=["bundle.js"],
		filename=BUNDLE_JS
	)

print("\ncopying CSS files")
for filename in files("src/css/"):
	shutil.copy(
		"src/css/" + filename,
		STATIC_CSS + filename
	)

if not skipping:
	print("\nminifying CSS")

	for filename in files(STATIC_CSS, ignore=["bundle.css", "login.css"]):
		print("  " + filename)

	minify_dir(
		"src/css/",
		ignore=["bundle.css", "login.css"],
		filename=BUNDLE_CSS
	)

	print("\nminifying")
	print("  font.css")
	print("  login.css")

	# minify and combine these 2 css files together
	# they are not needed in the bundle, only the login

	first=minify_single("src/css/font.css")
	second=minify_single("src/css/login.css")

	with open(STATIC_CSS + "login.css", "wb+") as f:
		f.write(first + second)

	print("\nminifying themes:")

	for f in files("src/themes", ignore=["auto.css"]):
		print("  " + f)
		clear(THEMES + f)

		minify_single(
			"src/themes/" + f,
			filename=THEMES + f
		)


	solarized_license= \
"""/* Reference to the original colorscheme */
/* github.com/altercation/solarized      */

"""

	css=""
	with open(THEMES + "solarized dark.css", "r") as f:
		css=f.read()

	with open(THEMES + "solarized dark.css", "w") as f:
		f.write(solarized_license + css)

print("")
