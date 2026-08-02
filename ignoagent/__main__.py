"""IgnoAgent main entrypoint for module execution (python -m ignoagent)."""

from ignoagent.agent import generate_report

def main() -> None:
    """Main CLI execution entrypoint."""
    generate_report()

if __name__ == "__main__":
    main()
