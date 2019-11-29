#clear old js file
>SHIMON/static/js/shimon.min.js

#print files to minify
echo minifiying:
ls SHIMON/static/js/ | grep -F ".js" | grep -v "shimon.min.js" | grep -v "msg.js"

#minify the files
minify $(tree -fi SHIMON/static/js/ | head -n -2 | grep -F ".js" | grep -v "shimon.min.js" | grep -v "msg.js") > SHIMON/static/js/shimon.min.js
