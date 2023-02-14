"""Transform the README.md to support a specific deployment target.

By default, we assume that our README.md will be rendered on GitHub. However, different
targets have different strategies for rendering light- and dark-mode images. This script
adjusts the images in the README.md to support the given target.
"""
import argparse
from pathlib import Path

URL = "https://user-images.githubusercontent.com/88637659/{}.svg"
URL_LIGHT = URL.format("213171745-7acf07df-6578-4a50-a106-1a7b368f8d6c")
URL_DARK = URL.format("213173736-6e91724c-8de1-4568-9d52-297b4b5ff0d2")

# https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#specifying-the-theme-an-image-is-shown-to
GITHUB = f"""
<p align="center">
  <picture align="center">
    <source media="(prefers-color-scheme: dark)" srcset="{URL_DARK}">
    <source media="(prefers-color-scheme: light)" srcset="{URL_LIGHT}">
    <img alt="Shows a bar chart with benchmark results." src="{URL_LIGHT}">
  </picture>
</p>
"""

# https://github.com/pypi/warehouse/issues/11251
PYPI = f"""
<p align="center">
  <img alt="Shows a bar chart with benchmark results." src="{URL_LIGHT}">
</p>
"""

# https://squidfunk.github.io/mkdocs-material/reference/images/#light-and-dark-mode
MK_DOCS = f"""
<p align="center">
  <img alt="Shows a bar chart with benchmark results." src="{URL_LIGHT}#only-light">
</p>

<p align="center">
  <img alt="Shows a bar chart with benchmark results." src="{URL_DARK}#only-dark">
</p>
"""


def main(target: str) -> None:
    """Modify the README.md to support the given target."""
    with Path("README.md").open(encoding="utf8") as fp:
        content = fp.read()
        if GITHUB not in content:
            msg = "README.md is not in the expected format."
            raise ValueError(msg)

    if target == "pypi":
        with Path("README.md").open("w", encoding="utf8") as fp:
            fp.write(content.replace(GITHUB, PYPI))
    elif target == "mkdocs":
        with Path("README.md").open("w", encoding="utf8") as fp:
            fp.write(content.replace(GITHUB, MK_DOCS))
    else:
        msg = f"Unknown target: {target}"
        raise ValueError(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Modify the README.md to support a specific deployment target.",
    )
    parser.add_argument(
        "--target",
        type=str,
        required=True,
        choices=("pypi", "mkdocs"),
    )
    args = parser.parse_args()

    main(target=args.target)
