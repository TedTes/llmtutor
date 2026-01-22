def make_plan(req, tools):
    t = req.text.lower()
    steps = []
    if any(k in t for k in ("dup","duplicate","dedupe")):
      steps.append({"tool":"dedupe","args":{"path":req.path,"method":"hash","dry_run":req.dry_run},"why":"identify duplicate files"})
    steps.append({"tool":"organize","args":{"path":req.path,"dry_run":req.dry_run},"why":"group files into folders by type"})


    return {"steps": steps}
