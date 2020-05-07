from pathlib import Path
import subprocess
import sys
import re

from typing import List, Iterator

def clear(file: str) -> None:
	with open(file, "w+") as f:
		f.write("")

def should_ignore(path: str, ignore: List=[]) -> bool:
	for check in ignore:
		if re.match(check, path):
			return True

	return False

def files(path: str, ignore: List=[]) -> Iterator[str]:
	ignore.append(r".*\.swp")

	for file in Path(path).iterdir():
		if not should_ignore(file.name, ignore):
			yield file

def sass(src: str, dest: str="") -> bytes:
	return call([
		"sass",
		"--no-source-map",
		"-s", "compressed",
		f"{src}:{dest}" if dest else src
	])

def call(commands: List[str]) -> bytes:
	return subprocess.run(
		commands,
		stdout=subprocess.PIPE
	).stdout

STATIC_CSS=Path("SHIMON/static/css/")
STATIC_JS=Path("SHIMON/static/js/")
THEMES=Path("SHIMON/templates/themes/")

BUNDLE_CSS=STATIC_CSS / "bundle.css"
BUNDLE_JS=STATIC_JS / "bundle.js"

clear(BUNDLE_JS)
clear(BUNDLE_CSS)

skipping=len(sys.argv) > 1

if not skipping:
	print("minifying JS")

	for file in files(STATIC_JS, ignore=["bundle.js"]):
		print(f"  {file.name}")

	with open(BUNDLE_JS, "rb+") as f:
		f.write(
			call(["minify", *files(
				STATIC_JS,
				["bundle.js"]
			)])
		)

print("\ncopying CSS files")
for file in files("src/css/"):
	sass(
		f"src/css/{file.name}",
		STATIC_CSS / file.name.replace("scss", "css")
	)

if not skipping:
	print("\nminifying CSS")

	with open(BUNDLE_CSS, "rb+") as f:
		for file in files("src/css/", ignore=["bundle.css", "_screen.scss"]):
			print(f"  {file.name}")
			f.write(sass(file))

	print("\nminifying themes:")

	for file in files("src/themes", ignore=[r"^_.*\.scss"]):
		css_name=file.name.replace("scss", "css")

		print(f"  {file.name}")
		clear(THEMES / css_name)

		sass(
			"src/themes/" + file.name,
			THEMES / css_name
		)

	solarized_license= \
b"""/* Reference to the original colorscheme */
/* github.com/altercation/solarized      */\n
"""

	with open(THEMES / "solarized dark.css", "rb+") as f:
		css=f.read()
		f.seek(0)
		f.write(solarized_license + css)

print("")
