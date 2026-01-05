# Fix generation

class FixAgent:
    def propose(self, analysis):
        fixes = []
        for rc in analysis["root_causes"]:
            if "CPU" in rc["cause"]:
                fixes.append("Enable HPA or increase CPU limits")
            if "DB" in rc["cause"]:
                fixes.append("Increase DB connection pool")
        return fixes