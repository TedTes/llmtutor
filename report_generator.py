def summarize(results):
    lines=[]
    for r in (results or []):
       if isinstance(r, dict) and r.get("tool")=="organize": 
        lines.append(f"organize(dry_run={r['dry_run']}): moved={r['moved']} errors={r['errors']}")
       elif isinstance(r, dict) and r.get("tool")=="dedupe":
         lines.append(f"dedupe(method={r['method']}): groups={r['group_count']}")
       else: lines.append(str(r)[:160])
   
    return "\n".join(lines) if lines else "No actions taken."
