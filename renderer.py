from flask import render_template

#when a template is rendered with developer mode on, the .js files will be used
#when developer mode is off, the shimon.min.js file is used to improve proformance

#when darkmode is on, style sheets will use darker colors and patterns
#when off (default), normal white theme is used

def render(self, name, **kwargs): #automatically add devmode and darkmode state to all render_templates
	kwargs["developer"]=self.developer
	kwargs["darkmode"]=self.darkmode
	return render_template(name, **kwargs)
