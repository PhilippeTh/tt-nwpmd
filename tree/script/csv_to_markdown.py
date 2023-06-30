###############################################################################
#
# Copyright (C) 2023 Philippe Théroux
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from copy import deepcopy
import csv
import os
import shutil

from tomark import Tomark


class BuildMarkdown:
    def __init__(self) -> None:
        self.input_dir = root = "weather"
        self.markdown_basedir = "tree/weather"
        self.current = current = 0
        self.levels = [
            {
                "Level": current + 8,
                "Name": "Earth System Discipline Category",
                "Value": root.split("/")[-1].capitalize(),
            }
        ]
        with open("topic-hierarchy.csv", "r") as topic_file:
            self.topic_reader = list(csv.DictReader(topic_file))

    def __delete_markdown_tree(self):
        if os.path.exists(self.markdown_basedir):
            shutil.rmtree(self.markdown_basedir)

    def children_markdown(self, markdown_dir, table):
        with open(os.path.join(markdown_dir, "README.md"), 'w') as f:
            navigation = self.navigation_markdown(markdown_dir)
            f.write(f"# {' > '.join(navigation)}\n\n")
            f.write("## Levels\n\n")
            self.levels_markdown(markdown_dir)
            f.write(Tomark.table(self.levels))
            f.write(
                f"\n## {markdown_dir.split('/')[-1].capitalize()} children"
            )
            for row in table:
                row["Name"] = f"[{row['Name'].capitalize()}]({row['Name']}/)"
            f.write("\n\n")
            f.write(Tomark.table(table))

    def levels_markdown(self, markdown_dir):
        if self.current != 0:
            for level in range(1, self.current + 1):
                level_name = (
                    self.topic_reader[level - 1]["Name"]
                    .replace("-", " ")
                    .title()
                )
                new_level = {
                    "Level": level + 8,
                    "Name": level_name,
                    "Value": markdown_dir.split('/')[
                        level - (self.current + 1)
                    ].capitalize(),
                }
                if len(self.levels) > level:
                    self.levels[level] = new_level
                else:
                    self.levels.append(new_level)

    def navigation_markdown(self, markdown_dir):
        navigation = []
        path_elems = markdown_dir.split('/')[1:]
        for index, levels_down in enumerate(reversed(range(len(path_elems)))):
            if (levels_down) != 0:
                double_dots = [".."] * levels_down
                navigation.append(
                    f"[{path_elems[index].capitalize()}]({'/'.join(double_dots)})"  # noqa
                )
            else:
                navigation.append(path_elems[index].capitalize())
        return navigation

    def leafs_markdown(self, markdown_dir):
        with open(os.path.join(markdown_dir, "README.md"), 'w') as f:
            navigation = self.navigation_markdown(markdown_dir)
            f.write(f"# {' > '.join(navigation)}\n\n")
            f.write("## Levels\n\n")
            self.levels_markdown(markdown_dir)
            f.write(Tomark.table(self.levels))

    def build_tree(self):
        self.__delete_markdown_tree()
        markdown_dirs = [self.markdown_basedir]
        for root, _, files in os.walk(self.input_dir):
            names = []
            csv_filename = self.check_files(files)
            if csv_filename:
                with open(os.path.join(root, csv_filename), 'r') as csvfile:
                    dict_reader = csv.DictReader(csvfile)
                    table = list(dict_reader)
                    for dir in markdown_dirs:
                        for row in table:
                            new_dir = os.path.join(dir, row["Name"])
                            os.makedirs(new_dir)
                            names.append(os.path.join(dir, row["Name"]))
                        self.children_markdown(dir, deepcopy(table))
                    markdown_dirs = [name for name in names]
                    self.current += 1
        for dir in markdown_dirs:
            self.leafs_markdown(dir)

    def check_files(self, files):
        if files:
            csv_files = [file for file in files if file.endswith('.csv')]
            if csv_files:
                topics_list = [topic["Name"] for topic in self.topic_reader]
            for csv_file in csv_files:
                if csv_file.split(".csv")[0] in topics_list:
                    return csv_file
        return False


if __name__ == "__main__":
    r = BuildMarkdown()
    r.build_tree()
