""" A script to parse the data from a .ged file.

    date: 20-Sep-2020
    python: v3.8.4
"""

import re
import operator
from typing import List, Optional

from prettytable import PrettyTable

TAGS: List[str] = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM',
                   'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']

ARGUMENT_PATTERN: str = '^(0|1|2) (NAME|SEX|FAMC|FAMS|MARR|HUSB|WIFE|CHIL|DATE) (.*)$'  # pattern 1
NO_ARGUMENT_PATTERN: str = '^(0|1) (BIRT|DEAT|MARR|DIV|HEAD|TRLR|NOTE)$'  # pattern 2
ZERO_PATTERN_1: str = '^0 (.*) (INDI|FAM)$'  # pattern 3
ZERO_PATTERN_2: str = '^0 (HEAD|TRLR|NOTE) ?(.*)$'  # pattern 4

regex_list: List[str] = [ARGUMENT_PATTERN, NO_ARGUMENT_PATTERN, ZERO_PATTERN_1, ZERO_PATTERN_2]


def pattern_finder(line: str) -> Optional[str]:
    """ find the pattern of a given line """
    for pattern, regex in zip(['ARGUMENT', 'NO_ARGUMENT', 'ZERO_1', 'ZERO_2'], regex_list):
        if re.search(regex, line):
            return pattern


def get_lines(path) -> List[str]:
    """ get lines read from a .ged file """
    with (file := open(path, "r")):  # close file after opening
        return [line for line in file]

class Family:
    """ holds a Family record """
    def __init__(self, _id=None, marr=None, husb=None, wife=None, div=False):
        """ store Family info """
        self.id = _id
        self.marr = marr
        self.husb = husb
        self.wife = wife
        self.chil: List[str] = []
        self.div: Optional[bool, Dict[str, str]] = div

    def info(self, individuals: List[Individual]):
        div = 'NA' if self.div is False else self.div['date']
        chil = 'NA' if len(self.chil) == 0 else self.chil
        h_name = next(individual.name for individual in individuals if individual.id == self.husb)
        w_name = next(individual.name for individual in individuals if individual.id == self.wife)

        return [self.id, self.marr['date'], div, self.husb, h_name, self.wife, w_name, chil]


def pretty_print(individuals: List[Individual], families: List[Family]) -> None:
    """ prettify the data """

    individual_table: PrettyTable = PrettyTable()
    family_table: PrettyTable = PrettyTable()
    individual_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age",
                                    "Alive", "Death", "Child", "Spouse"]
    family_table.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name",
                                "Wife ID", "Wife Name", "Child"]

    for individual in individuals:  # add individual info to the table
        individual_table.add_row(individual.info())

    for family in families:  # add individual info to the table
        family_table.add_row(family.info(individuals))

    print("Individuals\n", individual_table, sep="")
    print("Families\n", family_table, sep="")

def generate_classes(lines: List[str]) -> Tuple[List[Individual], List[Family]]:
    """ get lines read from a .ged file """
    individuals: List[Individual] = []
    families: List[Family] = []
    current_record: Optional[Individual, Family] = None
    current_tag: Optional[str] = None

    for line in lines:
        row_fields: List[str] = line.rstrip("\n").split(' ', 2)
        pattern_type = pattern_finder(line)



def main():
    """ the main function to check the data """
    path: str = 'SSW555-P1-fizgi.ged'
    lines = get_lines(path)  # process the file
    individuals, families = generate_classes(lines)
    individuals.sort(key=operator.attrgetter('id'))
    families.sort(key=operator.attrgetter('id'))
    pretty_print(individuals, families)


if __name__ == '__main__':
    main()
