from flask import render_template

#when a template is rendered with developer mode on, the .js files will be used
#when developer mode is off, the shimon.min.js file is used to improve proformance

#theme and version are passed automatically just in case they are needed

def render(self, name: str, **kwargs) -> str: #automatically add devmode and other variables to all render_templates
	kwargs["developer"]=self.developer
	kwargs["theme"]=self.theme
	kwargs["version"]=self.VERSION
	return render_template(name, **kwargs)
