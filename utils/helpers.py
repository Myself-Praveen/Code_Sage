import sys


def print_banner():
    print("\n╔══════════════════════════════╗")
    print("║        CodeSage v1.0         ║")
    print("╚══════════════════════════════╝\n")


def print_section(title):
    print(f"\n{'─' * 40}")
    print(f"  {title}")
    print(f"{'─' * 40}")


def fail(msg):
    print(f"\n[error] {msg}", file=sys.stderr)
    sys.exit(1)


def status(msg):
    print(f"  → {msg}")
