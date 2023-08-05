from pyquilted.html_app import HtmlApp
from pyquilted.pdf_app import PdfApp
from pyquilted.sample_app import SampleApp
from pyquilted.quilted.style import Style


class AppFactory:
    """App factory object that creates app objects for major cli options"""
    def __init__(self, args):
        self.args = vars(args)
        self.options = Options(**self.args)
        self.style = vars(Style(**self.args))

    def create(self):
        """returns a different app object depending on the cli options

           Returns:
               app: app object with a run method
        """
        app = None
        if self.options.sample:
            app = SampleApp('/sample/resume.yml', self.options.sample)
        elif self.options.html:
            app = HtmlApp(self.options.html[0], self.options.html[1],
                          style=self.style)
        elif self.options.pdf:
            app = PdfApp(self.options.pdf[0], self.options.pdf[1],
                         style=self.style)
        return app


class Options:
    """pyquilted options settings"""
    def __init__(self, pdf=None, html=None, sample=None, **kwargs):
        self.pdf = pdf
        self.html = html
        self.sample = sample
