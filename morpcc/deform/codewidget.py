from deform.widget import TextAreaWidget
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import find_lexer_class_by_name


class CodeWidget(TextAreaWidget):

    css_class = "code"
    template = "code"
    readonly_template = "readonly/code"
    syntax = "python"

    def highlight(self, code):
        Lexer = find_lexer_class_by_name(self.syntax)
        formatter = HtmlFormatter()
        highlighted = highlight(code, Lexer(), formatter)
        return highlighted
