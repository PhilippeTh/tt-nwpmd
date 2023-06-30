# Script overview

This script is used to automatically generate a tree of markdown files when run by the github workflow. If you wish to run this script manually, you will need Python 3 installed as well as the Tomark library. For the script to work, it needs to be run from the root folder (meaning from inside /tt-nwpmd).

Please take note that, when merging into [tt-nwpmd](https://github.com/wmo-im/tt-nwpmd), the layer tree will be fully rebuilt. As such, modifying or adding anything inside tree/weather serves no purpose as it will just get overwritten by the workflow.

# Installation and execution

## Requirements
- Python 3
- [virtualenv](https://virtualenv.pypa.io/)

## Dependencies
Dependencies are listed in [requirements.txt](tree/script/requirements.txt). Dependencies are automatically installed during installation.

## Installing tt-nwpmd
```bash

# setup virtualenv
python -m venv myvenv
cd myvenv
. bin/activate

# clone codebase and install
git clone https://github.com/wmo-im/tt-nwpmd.git
cd tt-nwpmd
pip install -r tree/script/requirements.txt
```

## Running the script
```bash
python tree/script/csv_to_markdown.py
```

# Github workflow

For the workflow to work properly, you will to follow these steps:

* Inside [main.yml](.github/workflows/main.yml), on the very bottom, you will need to modify the branch name for your own;
* For the workflow to be able to change the main branch, it needs to have workflow write access. This can be done by going on your github fork -> Settings -> Actions -> General -> In Workflow permissions, select Read and write permissions;
* Finally, you mustn't modify the branch on which the workflow is directly and instead you'll need to merge something into the branch. Modifying the branch in which you want this workflow to work directly would bypass the generation of the markdown tree. The correct way would be to fork the main branch when you wish to make a change, make the changes, push those changes and then make a pull request to the main branch. Once the pull request is approved and merged, the workflow will kick in and regenerate the markdown tree.