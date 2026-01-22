from request_parser import parse;
from context_policy import Policy,enforce_scope
from tools_registry import TOOLS;
from llm_planer import make_plan;
from plan_validator import validate;
from executor import run;
from report_generator import summarize
from pathlib import Path
import sys;

if "--undo" in sys.argv: __import__("undo"); raise SystemExit
apply="--apply" in sys.argv
req=parse(input("request> "), enforce_scope(Policy(base=Path.home()), input("path> ")))
req=type(req)(req.text, req.path, not apply)

plan = validate(make_plan(req, TOOLS), TOOLS); 
if req.dry_run is False or input("run this plan? (y/N) ").lower()=="y":
    print(summarize(run(plan, TOOLS)))


if input("apply changes? (y/N) ").lower()=="y":
    req = type(req)(req.text, req.path, False); 
    print(summarize(run(validate(make_plan(req, TOOLS), TOOLS), TOOLS)))





def show_plan(plan):
    for i,s in enumerate(plan.get("steps", []), 1):
        print(f"{i}. {s['tool']} — {s.get('why','')}  args={s['args']}")