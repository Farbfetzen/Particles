import argparse
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import src.run
import src.shared_constants


parser = argparse.ArgumentParser()
parser.add_argument(
    "name",
    nargs="?",
    default="default",
    help="Name of the particle simulation."
)
parser.add_argument(
    "-w",
    "--window-size",
    metavar=("<width>", "<height>"),
    nargs=2,
    type=int,
    default=src.shared_constants.WINDOW_SIZE,
    help="Specify the window width and height in pixels."
)
args = parser.parse_args()

valid_names = {"default", "bounce", "fire", "fireballs"}
if args.name not in valid_names:
    parser.error(f"name must be one of {list(valid_names)}")

src.shared_constants.WINDOW_SIZE = args.window_size

src.run.run(args.name)
