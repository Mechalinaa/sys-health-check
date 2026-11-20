import argparse


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Check system health: CPU, memory, disk, services and URLs"
    )
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="path to the configuration file (default: %(default)s)",
    )
    parser.add_argument(
        "--format",
        choices=["json", "txt"],
        default="txt",
        help="output format of the report (default: %(default)s)",
    )
    parser.add_argument(
        "--log-file",
        help="append results to this log file; if omitted, no log is written",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="show debug information"
    )
    parser.parse_args(argv)
    return 0
