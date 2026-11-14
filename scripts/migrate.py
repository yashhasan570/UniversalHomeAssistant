#!/usr/bin/env python3
"""Reapply the Universal Home Assistant rebrand after an upstream sync."""
from pathlib import Path
import os, shutil

SKIP_DIRS = {'.git', '.github', 'scripts'}

def newpath(s):
    s = s.replace('HomeAssistant', 'UniversalAssistant').replace('homeassistant', 'universalassistant').replace('home-assistant', 'universal-assistant')
    return s

def sweep():
    protects = [('Universal Home Assistant', '__HA_KEEP__'), ('UniversalAssistant', '__HAC_KEEP__')]
    restores = [('__HA_KEEP__', 'Universal Home Assistant'), ('__HAC_KEEP__', 'UniversalAssistant')]
    pairs = [
        ('https://github.com/home-assistant/core', 'https://github.com/yashhasan570/UniversalHomeAssistant'),
        ('home-assistant.io', 'universalassistant.io'),
        ('home-assistant', 'universal-assistant'),
        ('HomeAssistant', 'UniversalAssistant'),
        ('Home Assistant', 'Universal Home Assistant'),
        ('homeassistant', 'universalassistant'),
        ('home_assistant', 'universal_assistant'),
        ('HOME_ASSISTANT', 'UNIVERSAL_ASSISTANT'),
        ('Home-Assistant', 'Universal-Assistant'),
        ('Home assistant', 'Universal assistant'),
        ('home assistant', 'universal assistant'),
    ]
    binary_ext = {'.png','.jpg','.jpeg','.gif','.ico','.webp','.pdf','.zip','.bin','.so','.a','.dll','.dylib','.mp3','.ogg','.wav','.woff','.woff2','.ttf','.otf'}
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            p = Path(root) / f
            if p.suffix.lower() in binary_ext or p.name in ('migrate.py',): continue
            try: t = p.read_text(encoding='utf-8')
            except Exception: continue
            orig = t
            for old, new in protects: t = t.replace(old, new)
            for old, new in pairs:
                t = t.replace(old, new)
            if t != orig: p.write_text(t)

def merge(src, dst):
    for child in list(src.iterdir()):
        ct = Path(newpath(str(child)))
        ct.parent.mkdir(parents=True, exist_ok=True)
        if ct.exists():
            if child.is_dir() and ct.is_dir():
                merge(child, ct)
                try: child.rmdir()
                except OSError: pass
            elif child.is_dir():
                shutil.rmtree(ct, ignore_errors=True)
                shutil.move(str(child), str(ct))
            else:
                if ct.is_dir(): shutil.rmtree(ct, ignore_errors=True)
                else: ct.unlink()
                shutil.move(str(child), str(ct))
        else:
            shutil.move(str(child), str(ct))
    try: src.rmdir()
    except OSError: pass

def renames():
    targets = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in dirs + files:
            if 'homeassistant' in name.lower() or 'home-assistant' in name or 'HomeAssistant' in name:
                targets.append(Path(root) / name)
    targets.sort(key=lambda p: len(p.parts), reverse=True)
    for p in targets:
        if not p.exists(): continue
        tgt = Path(newpath(str(p)))
        if p == tgt: continue
        tgt.parent.mkdir(parents=True, exist_ok=True)
        if p.is_dir() and tgt.exists() and tgt.is_dir():
            merge(p, tgt)
        elif tgt.exists():
            if p.is_dir(): shutil.rmtree(p, ignore_errors=True)
            else:
                if tgt.is_dir(): shutil.rmtree(tgt, ignore_errors=True)
                else: tgt.unlink()
                shutil.move(str(p), str(tgt))
        else:
            shutil.move(str(p), str(tgt))

def cleanup():
    for item in ['.github/FUNDING.yml','.agents','.claude','.gemini','.vscode','.devcontainer',
                 '.git-blame-ignore-revs','.pre-commit-config.yaml','.strict-typing','.hadolint.yaml',
                 '.yamllint','AGENTS.md','AI_POLICY.md','CLA.md','CODEOWNERS','CODE_OF_CONDUCT.md',
                 'CONTRIBUTING.md','README.rst','codecov.yml']:
        p = Path(item)
        if p.is_dir(): shutil.rmtree(p, ignore_errors=True)
        elif p.exists(): p.unlink()

def readme():
    Path('README.md').write_text("""# Universal Home Assistant

Self-hosted smart home automation platform. Control and automate your lights, climate, devices, and appliances from a single dashboard, with support for thousands of device integrations.

## Getting started

Docker is the recommended way to run it:

```
docker run -d --name universal-home-assistant --restart=unless-stopped \\
  -v /path/to/config:/config -p 8123:8123 ghcr.io/yashhasan570/universal-home-assistant:latest
```

The dashboard is then available at http://localhost:8123.

## Contact

Telegram: [@johnconstantine570](https://t.me/johnconstantine570)
""")

if __name__ == '__main__':
    sweep(); renames(); cleanup(); readme()
    print('rebrand reapplied')
