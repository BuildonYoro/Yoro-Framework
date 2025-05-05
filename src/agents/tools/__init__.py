# coding=utf-8

from .tool import Tool
from .web_search import WebSearchTool
from .web_crawl import WebCrawlTool
from .mail import MailTool
from .weather import WeatherTool
from .translate import TranslateTool
from .code_interpreter import CodeInterpreterTool
from .math import (
    EvaluateExpressionTool,
    CalculatePolynomialRootsTool,
    SolveAlgebraicEquationTool,
)

# from .web_browse import WebBrowseTool

AVAILABLE_TOOLS = {
    "code_interpreter": CodeInterpreterTool,
    "evaluate_expression": EvaluateExpressionTool,
    "calculate_polynomial_roots": CalculatePolynomialRootsTool,
    "solve_algebraic_equation": SolveAlgebraicEquationTool,
}
