name = "blender"

version = "3.6.4.1"

authors = ["Blender Foundation"]

variants = [["platform-**", "arch-**"]]

description = "Free and Open 3D Creation Software."

uuid = "8af3cb94b05a4ee797c9222ae4678fcd"

requires = []

build_command = "python {root}/../build.py"

private_build_requires = [
    "python-3+",
    "rez",
    "rezbuild_utils-2+",
]

tools = [
    "blender",
    "blender-launcher",
]


def commands():
    env.PATH.append("{root}")
