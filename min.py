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
		if filename not in ignore and not filename.endswith(".swp"):
			yield (path + filename) if fullpath else filename

def sass(src: str, dest: str="") -> bytes:
	return call([
		"sass",
		"--no-source-map",
		"-s", "compressed",
		(f"{src}:{dest}") if dest else src
	])

def call(commands: List[str]) -> bytes:
	return subprocess.run(
		commands,
		stdout=subprocess.PIPE
	).stdout

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
		print(f"  {filename}")

	with open(BUNDLE_JS, "rb+") as f:
		f.write(
			call(["minify"] + list(
				files(
					STATIC_JS,
					["bundle.js"],
					fullpath=True
				)
			))
		)

print("\ncopying CSS files")
for filename in files("src/css/"):
	sass(
		f"src/css/{filename}",
		STATIC_CSS + filename[:-4] + "css"
	)

if not skipping:
	print("\nminifying CSS")

	with open(BUNDLE_CSS, "rb+") as f:
		for filename in files("src/css/", ignore=["bundle.css", "login.scss"], fullpath=True):
			print("  " + filename.split("/")[-1])
			f.write(sass(filename))

	print("\nminifying")
	print("  font.css")
	print("  login.css")

	# minify and combine these 2 css files together
	# they are not needed in the bundle, only the login

	with open(STATIC_CSS + "login.css", "wb+") as f:
		f.write(
			sass("src/css/font.scss") +
			sass("src/css/login.scss")
		)

	print("\nminifying themes:")

	for filename in files("src/themes", ignore=["_urls.scss", "_root.scss", "_theme.scss"]):
		css_name=filename[:-4] + "css"

		print(f"  {filename}")
		clear(THEMES + css_name)

		sass(
			"src/themes/" + filename,
			THEMES + css_name
		)

	# prepend license for solarized colorscheme

	solarized_license= \
"""/* Reference to the original colorscheme */
/* github.com/altercation/solarized      */

"""

	css=b""
	with open(THEMES + "solarized dark.css", "rb") as f:
		css=f.read()

	with open(THEMES + "solarized dark.css", "wb") as f:
		f.write(solarized_license.encode() + css)

print("")
