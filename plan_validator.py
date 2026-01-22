def validate(plan, tools):
   for s in plan.get("steps", []):
        t=tools[s["tool"]]; 
        assert s["tool"] in tools
        req=[k for k,v in t.args_schema.items() if v is not None]
        for k in req: assert k in s["args"]
   return plan