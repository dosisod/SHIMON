#clear old js file
>SHIMON/static/js/bundle.js
>SHIMON/static/css/bundle.css
>SHIMON/static/css/login.css

if [ -z "$@" ]; then
	#print files to minify
	echo "minifiying:"
	ls SHIMON/static/js/ | grep -F ".js" | grep -v "bundle.js"

	#minify the files
	minify $(tree -fi SHIMON/static/js/ | head -n -2 | grep -F ".js" | grep -v "bundle.js") > SHIMON/static/js/bundle.js
	echo ""
fi

#always move css files
echo "copying files"
cp src/css/* SHIMON/static/css/

if [ -z "$@" ]; then
	echo "minifiying:"
	ls src/css/ | grep -F ".css" | grep -v "bundle.css" | grep -v "login.css"

	#minify all css into a single bundle
	minify $(tree -fi src/css/ | head -n -2 | grep -F ".css" | grep -v "bundle.css" | grep -v "login.css") > "SHIMON/static/css/bundle.css"

	echo ""
	echo "minifying:"
	echo "font.css"
	echo "login.css"

	minify src/css/font.css > "SHIMON/static/css/login.css"
	minify src/css/login.css >> "SHIMON/static/css/login.css"

	files=$(find src/themes/ | grep -vF "auto.css" | tail -n +2 | cut -d "/" -f 3)
	echo ""
	echo "minifying:"
	echo "$files"

	while read -r file; do
		>"SHIMON/templates/themes/$file"
		minify "src/themes/$file" > "SHIMON/templates/themes/$file"
	done <<< "$files"

	#add license to solarized dark
	echo -e "/* Reference to the original colorscheme */\n/* github.com/altercation/solarized      */\n\n$(cat "SHIMON/templates/themes/solarized dark.css")" > "SHIMON/templates/themes/solarized dark.css"
fi
