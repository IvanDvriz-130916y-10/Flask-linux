import sys
import argparse
from utils.port_tools import run_server_on_port


def start():
    parser = argparse.ArgumentParser(description="Free port and run Flask server.")
    parser.add_argument("p", type=int, help="Port number")
    args = parser.parse_args()

    cmd = [sys.executable, "web/app.py", "--port", str(args.p)]
    run_server_on_port(args.p, cmd)

    print(f"Server started on port {args.p}")
    print("Stop it with Ctrl+C in this terminal.")


if __name__ == "__main__":
    start()