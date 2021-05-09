import argparse
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import src.run
from src.bounce import BounceSystem
from src.default import DefaultSystem
from src.fire import FireSystem
from src.fireballs import FireballSystem
from src.portal import PortalSystem


SYSTEMS = {
    "bounce": BounceSystem,
    "default": DefaultSystem,
    "fire": FireSystem,
    "fireballs": FireballSystem,
    "portal": PortalSystem
}

parser = argparse.ArgumentParser()
parser.add_argument(
    "name",
    nargs="?",
    default="default",
    choices=SYSTEMS.keys(),
    help="Name of the particle system."
)
parser.add_argument(
    "-w",
    "--window-size",
    metavar=("<width>", "<height>"),
    nargs=2,
    type=int,
    default=(1200, 800),
    help="Specify the window width and height in pixels."
)
args = parser.parse_args()

src.run.run(SYSTEMS, args.name, args.window_size)
