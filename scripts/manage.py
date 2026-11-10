#!/usr/bin/env python3
"""Import an IPA into GitHub Releases and update an AltStore Classic-style JSON feed."""
import argparse
import datetime
import json
import os
import plistlib
import re
import subprocess
import urllib.parse
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/source.json"
MAX_BYTES = 2 * 1024**3

def gh(*args):
    return subprocess.run(["gh", *args], check=True, text=True, capture_output=True).stdout.strip()

def ipa_info(path):
    with zipfile.ZipFile(path) as archive:
        candidates = [n for n in archive.namelist() if re.fullmatch(r"Payload/[^/]+\.app/Info\.plist", n)]
        if not candidates:
            raise ValueError("IPA missing Payload/*.app/Info.plist")
        data = plistlib.loads(archive.read(candidates[0]))
        if not data.get("CFBundleIdentifier"):
            raise ValueError("IPA missing bundle identifier")
        return (str(data.get("CFBundleDisplayName") or data.get("CFBundleName") or path.stem),
                str(data.get("CFBundleShortVersionString") or data.get("CFBundleVersion") or "1.0"),
                str(data.get("CFBundleVersion") or "1"),
                str(data["CFBundleIdentifier"]))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["add"])
    p.add_argument("--file", type=Path, required=True)
    p.add_argument("--repo", default=os.getenv("GITHUB_REPOSITORY", ""))
    for arg in ("name", "version", "description", "icon", "developer"):
        p.add_argument("--" + arg, default="")
    a = p.parse_args()
    f = a.file.resolve()
    if not f.is_file() or f.suffix.lower() != ".ipa": p.error("Provide a valid IPA file")
    if f.stat().st_size >= MAX_BYTES: p.error("Release assets must be smaller than 2 GiB")
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", a.repo): p.error("Invalid OWNER/REPO")
    try:
        detected_name, detected_version, build, bundle = ipa_info(f)
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        p.error(str(error))
    name, version = a.name or detected_name, a.version or detected_version
    safe = lambda s: re.sub(r"[^a-zA-Z0-9_.-]", "-", s)[:65]
    tag = "ipa-" + safe(bundle) + "-" + safe(version) + "-" + safe(build)
    feed = json.loads(SOURCE.read_text(encoding="utf8"))
    try:
        gh("release", "view", tag, "--repo", a.repo)
    except subprocess.CalledProcessError:
        gh("release", "create", tag, "--repo", a.repo, "--title", name + " " + version,
           "--notes", a.description or ("Bundle ID: " + bundle))
    gh("release", "upload", tag, str(f), "--repo", a.repo, "--clobber")
    url = "https://github.com/" + a.repo + "/releases/download/" + tag + "/" + urllib.parse.quote(f.name)
    entry = {"version": version, "buildVersion": build, "date": datetime.datetime.now(datetime.timezone.utc).date().isoformat(),
             "localizedDescription": a.description or name, "downloadURL": url, "size": f.stat().st_size}
    apps = feed["apps"]
    app = next((x for x in apps if x["bundleIdentifier"] == bundle), None)
    if not app:
        app = {"name": name, "bundleIdentifier": bundle, "developerName": a.developer or "Personal Collection",
               "subtitle": "IPA", "localizedDescription": a.description or name,
               "iconURL": a.icon or "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
               "tintColor": "#5075E8", "versions": []}
        apps.insert(0, app)
    app["name"] = name
    if a.description: app["localizedDescription"] = a.description
    if a.icon: app["iconURL"] = a.icon
    if a.developer: app["developerName"] = a.developer
    app["versions"] = [v for v in app["versions"] if (v["version"], v.get("buildVersion")) != (version, build)]
    app["versions"].insert(0, entry)
    SOURCE.write_text(json.dumps(feed, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print("Imported:", name, version, url)

if __name__ == "__main__":
    main()
