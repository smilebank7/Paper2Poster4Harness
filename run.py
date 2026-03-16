#!/usr/bin/env python3
import shutil
import site
import sys


def main():
    if not shutil.which("claude"):
        print("ERROR: 'claude' CLI not found.")
        print("Install Claude Code: npm install -g @anthropic-ai/claude-code")
        print("Or use OpenCode: https://github.com/opencode-ai/opencode")
        sys.exit(1)

    print("✅ Claude CLI found. Using subscription-based AI (no API key needed).")
    print("🎓 Paper2Poster4Harness — Generating poster...")
    print()

    for site_path in reversed(site.getsitepackages()):
        if site_path in sys.path:
            sys.path.remove(site_path)
        sys.path.insert(0, site_path)

    from PosterAgent.new_pipeline import main as pipeline_main

    pipeline_main()


if __name__ == "__main__":
    main()
