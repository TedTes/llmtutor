from request_parser import parse;
from context_policy import Policy,enforce_scope
from tools_registry import TOOLS;
from llm_planer import make_plan;
from plan_validator import validate;
from executor import run;
from report_generator import summarize
from pathlib import Path

req=parse(input("request> "), enforce_scope(Policy(base=Path.home()), input("path> ")))

print(summarize(run(validate(make_plan(req, TOOLS), TOOLS), TOOLS)))