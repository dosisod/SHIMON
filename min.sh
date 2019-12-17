#clear old js file
>SHIMON/static/js/shimon.min.js
>SHIMON/static/css/bundle.css
>SHIMON/static/css/login.css

if [ -z "$@" ]; then
	#print files to minify
	echo "minifiying:"
	ls SHIMON/static/js/ | grep -F ".js" | grep -v "shimon.min.js" | grep -v "msg.js"

	#minify the files
	minify $(tree -fi SHIMON/static/js/ | head -n -2 | grep -F ".js" | grep -v "shimon.min.js" | grep -v "msg.js") > SHIMON/static/js/shimon.min.js
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
fi
