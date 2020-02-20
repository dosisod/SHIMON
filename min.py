import subprocess
import shutil
import sys
import os

from typing import List, Iterator, Union, Optional

def clear(filename: Union[str, List[str]]) -> None:
	if isinstance(filename, list):
		for fn in filename:
			clear(fn)

		return None

	with open(filename, "w+") as f:
		f.write("")

def files(path: str, ignore: List=[], full: bool=False) -> Iterator[str]:
	for f in os.listdir(path):
		if f not in ignore:
			if full:
				yield path + f
			else:
				yield f

def minify_dir(path: str, ignore: List=[], write: str="") -> Optional[bytes]:
	return minify(
		list(files(path, ignore, full=True)),
		write
	)

def minify_single(path: str, write: str="") -> Optional[bytes]:
	return minify([path], write)

def minify(commands: List[str], write: str="") -> Optional[bytes]:
	command=["minify"]
	command+=commands

	out=subprocess.run(
		command,
		stdout=subprocess.PIPE
	).stdout

	if write:
		with open(write, "rb+") as f:
			f.write(out)
	else:
		return out

skipping=False
if len(sys.argv) > 1:
	skipping=True

STATIC_CSS="SHIMON/static/css/"
STATIC_JS="SHIMON/static/js/"

BUNDLE_JS=STATIC_JS + "bundle.js"
BUNDLE_CSS=STATIC_CSS + "bundle.css"

#force clear given files

clear([
	BUNDLE_JS,
	BUNDLE_CSS,
	STATIC_CSS + "login.css"
])

if not skipping:
	print("minifying JS")

	for f in files(STATIC_JS, ignore=["bundle.js"]):
		print("  " + f)

	minify_dir(
		STATIC_JS,
		ignore=["bundle.js"],
		write=STATIC_JS + "bundle.js"
	)

print("\ncopying CSS files")
for f in files("src/css/"):
	shutil.copy(
		"src/css/" + f,
		STATIC_CSS + f
	)

if not skipping:
	print("\nminifying CSS")

	for f in files(STATIC_CSS, ignore=["bundle.css", "login.css"]):
		print("  " + f)

	minify_dir(
		"src/css/",
		ignore=["bundle.css", "login.css"],
		write=STATIC_CSS + "bundle.css"
	)

	print("\nminifying")
	print("  font.css")
	print("  login.css")

	#minify src/css/font.css > "SHIMON/static/css/login.css"
	first=minify_single("src/css/font.css")

	#minify src/css/login.css >> "SHIMON/static/css/login.css"
	second=minify_single("src/css/login.css")

	with open(STATIC_CSS + "login.css", "wb+") as f:
		f.write(first + second)

	print("\nminifying themes:")

	for f in files("src/themes", ignore=["auto.css"]):
		print("  " + f)

		clear("SHIMON/templates/themes/" + f)
		#minify "src/themes/"+f > "SHIMON/templates/themes/"+f

		minify_single(
			"src/themes/" + f,
			write="SHIMON/templates/themes/" + f
		)


	solarized_license= \
"""/* Reference to the original colorscheme */
/* github.com/altercation/solarized      */

"""

	css=""
	with open("SHIMON/templates/themes/solarized dark.css", "r") as f:
		css=f.read()

	with open("SHIMON/templates/themes/solarized dark.css", "w") as f:
		f.write(solarized_license + css)

print("")
