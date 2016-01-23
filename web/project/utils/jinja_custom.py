from flask import url_for
from werkzeug.routing import BuildError
from project import app

@app.context_processor
def utility_processor():
    def url_for_or_none(url):
        try:
            url = url_for(url)
        except BuildError:
            url = '404'
        return url

    return dict(url_for_or_none=url_for_or_none)

@app.template_filter('dateformat')
def _jinja_datetimefilter(value, format='%Y/%m/%d'):
    """convert a datetime to a different format."""
    return value.strftime(format)

@app.template_filter('format_decimal')
def format_decimal(value):
    return "{:,.2f}".format(float(value))

