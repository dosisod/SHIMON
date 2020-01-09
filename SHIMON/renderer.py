from flask import render_template

from .__init__ import Page

def render(self, filepath: str, **kwargs) -> Page:
	kwargs["developer"]=self.developer
	kwargs["theme"]=self.theme
	kwargs["fresh_js"]=self.fresh_js
	kwargs["fresh_css"]=self.fresh_css

	return render_template(filepath, **kwargs)
