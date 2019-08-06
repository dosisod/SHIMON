from flask import render_template

#when a template is rendered with developer mode on, the .js files will be used
#when developer mode is off, the shimon.min.js file is used to improve proformance

def render(self, name, **kwargs): #automatically add devmode state to all render_templates
	kwargs["developer"]=self.developer
	return render_template(name, **kwargs)
