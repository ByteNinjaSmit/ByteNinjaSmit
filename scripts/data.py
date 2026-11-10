"""Fetch live numbers for the profile. Token (optional) comes from env GH_TOKEN / GITHUB_TOKEN.
Without a token the public REST data still works; the contribution heatmap needs one."""
import json, os, sys, urllib.request

USER = os.environ.get("PROFILE_USER", "ByteNinjaSmit")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache.json")


def call(url, body=None):
    req = urllib.request.Request(url, data=body)
    req.add_header("User-Agent", "profile-builder")
    req.add_header("Accept", "application/vnd.github+json")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch():
    user = call(f"https://api.github.com/users/{USER}")
    repos, page = [], 1
    while True:
        chunk = call(f"https://api.github.com/users/{USER}/repos?per_page=100&page={page}&type=owner")
        repos += chunk
        if len(chunk) < 100:
            break
        page += 1
    own = [r for r in repos if not r["fork"]]
    langs = {}
    for r in own:
        try:
            for k, v in call(r["languages_url"]).items():
                langs[k] = langs.get(k, 0) + v
        except Exception as e:
            print("lang fail", r["name"], e, file=sys.stderr)
    stars = sum(r["stargazers_count"] for r in own)
    pushed = max(r["pushed_at"] for r in own)
    out = {
        "repos": user["public_repos"],
        "followers": user["followers"],
        "since": int(user["created_at"][:4]),
        "stars": stars,
        "langs": langs,
        "last_push": pushed[:10],
        "calendar": None,
    }
    if TOKEN:
        q = """query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{
        totalContributions weeks{contributionDays{contributionCount date weekday}}}}}}"""
        try:
            res = call("https://api.github.com/graphql", json.dumps({"query": q, "variables": {"u": USER}}).encode())
            out["calendar"] = res["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        except Exception as e:
            print("calendar fail", e, file=sys.stderr)
    prev = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    if out["calendar"] is None:
        out["calendar"] = prev.get("calendar")
    out["calendars"] = prev.get("calendars", {})
    if TOKEN:
        import datetime
        now = datetime.datetime.utcnow()
        parts = []
        for y in range(out["since"], now.year + 1):
            to = now.strftime("%Y-%m-%dT%H:%M:%SZ") if y == now.year else f"{y}-12-31T23:59:59Z"
            parts.append(f'y{y}: contributionsCollection(from:"{y}-01-01T00:00:00Z", to:"{to}")'
                         '{contributionCalendar{totalContributions weeks{contributionDays{contributionCount date weekday}}}}')
        q = "query($u:String!){user(login:$u){" + " ".join(parts) + "}}"
        try:
            res = call("https://api.github.com/graphql", json.dumps({"query": q, "variables": {"u": USER}}).encode())
            for k, v in res["data"]["user"].items():
                out["calendars"][k[1:]] = v["contributionCalendar"]
        except Exception as e:
            print("yearly calendars fail", e, file=sys.stderr)
    json.dump(out, open(CACHE, "w"))
    return out


def load(refresh=True):
    if refresh:
        try:
            return fetch()
        except Exception as e:
            print("fetch failed, using cache:", e, file=sys.stderr)
    return json.load(open(CACHE))


if __name__ == "__main__":
    d = fetch()
    print({k: (v if k not in ("langs", "calendar", "calendars") else "…") for k, v in d.items()})
    print(sorted(d["langs"].items(), key=lambda x: -x[1])[:8])
    print("calendar:", d["calendar"] and d["calendar"]["totalContributions"])
