"""Build a portable Skill archive, excluding local runtime files."""
import hashlib
import os
from pathlib import Path
import zipfile

repo = Path(__file__).resolve().parents[1]
skill = repo / "skills/ai-thinker-fae-blade"
target = repo / "dist/ai-thinker-fae-blade.skill.zip"
target.parent.mkdir(exist_ok=True)
excluded = {".runtime", ".sync-lock", "__pycache__"}
def fail_walk(error):
    raise error

with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
    for directory, folders, files in os.walk(skill, onerror=fail_walk):
        folders[:] = sorted(folder for folder in folders if folder not in excluded)
        for name in sorted(files):
            path = Path(directory) / name
            relative = path.relative_to(skill)
            if not name.endswith(".pyc"):
                archive.write(path, "ai-thinker-fae-blade/" + relative.as_posix())
with zipfile.ZipFile(target) as archive:
    assert archive.testzip() is None
    assert "ai-thinker-fae-blade/SKILL.md" in archive.namelist()
print(str(target))
print("SHA256 " + hashlib.sha256(target.read_bytes()).hexdigest())
