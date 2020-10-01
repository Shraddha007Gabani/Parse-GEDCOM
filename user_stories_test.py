""" Implement test cases for user stories

    date: 30-Sep-2020
    python: v3.8.4
"""

import unittest
from typing import List
from models import Individual, Family
from user_stories import were_parents_over_14, birth_before_death_of_parents


class TestApp(unittest.TestCase):
    """ test class of the methods """
    def test_were_parents_over_14(self):
        """ test were_parents_over_14 method """
        # husband is 20 and wife is 14 at the marriage date -> Both are over 14 -> True
        husband: Individual = Individual(_id="I0", birt={'date': "19 SEP 1995"})
        wife: Individual = Individual(_id="I1", birt={'date': "3 JAN 2000"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id="F0", husb=husband.id, wife=wife.id,
                                marr={'date': "11 FEB 2015"})
        self.assertTrue(were_parents_over_14(family, individuals))

        # husband 11, wife 20 -> Only wife is over 14 -> False
        husband: Individual = Individual(_id="I2", birt={'date': "2 MAR 2007"})
        wife: Individual = Individual(_id="I3", birt={'date': "11 FEB 2000"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id="F1", husb=husband.id, wife=wife.id,
                                marr={'date': "11 FEB 2019"})
        self.assertFalse(were_parents_over_14(family, individuals))

        # husband 17, wife 10 -> Only husband is over 14 -> False
        husband: Individual = Individual(_id="I4", birt={'date': "22 AUG 2000"})
        wife: Individual = Individual(_id="I5", birt={'date': "5 DEC 2007"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id="F2", husb=husband.id, wife=wife.id,
                                marr={'date': "11 FEB 2018"})
        self.assertFalse(were_parents_over_14(family, individuals))

        # husband 12, wife 12 -> Both are under 14 -> False
        husband: Individual = Individual(_id="I6", birt={'date': "19 SEP 2007"})
        wife: Individual = Individual(_id="I7", birt={'date': "3 JAN 2008"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id="F3", husb=husband.id, wife=wife.id,
                                marr={'date': "11 FEB 2020"})
        self.assertFalse(were_parents_over_14(family, individuals))

        # husband 18, wife 16 -> Both are over 14 -> True
        husband: Individual = Individual(_id="I8", birt={'date': "7 FEB 1980"})
        wife: Individual = Individual(_id="I9", birt={'date': "8 FEB 1982"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id="F4", husb=husband.id, wife=wife.id,
                                marr={'date': "11 FEB 1998"})
        self.assertTrue(were_parents_over_14(family, individuals))

    def test_birth_before_death_of_parents(self):
        """ test birth_before_death_of_parents method """
        # mother and father are alive (no death date)
        husband: Individual = Individual(_id="I0")
        wife: Individual = Individual(_id="I1")
        child: Individual = Individual(_id="I2", birt={'date': "4 OCT 2000"})
        individuals: List[Individual] = [husband, wife, child]
        family: Family = Family(_id="F0", husb=husband.id, wife=wife.id)
        family.chil.append(child.id)
        self.assertTrue(birth_before_death_of_parents(family, individuals))

        # child born on: mother death, 270 day after father death
        husband: Individual = Individual(_id="I0", deat={'date': "8 JAN 2000"})
        wife: Individual = Individual(_id="I1", deat={'date': "4 OCT 2000"})
        child: Individual = Individual(_id="I2", birt={'date': "4 OCT 2000"})
        individuals: List[Individual] = [husband, wife, child]
        family: Family = Family(_id="F1", husb=husband.id, wife=wife.id)
        family.chil.append(child.id)
        self.assertTrue(birth_before_death_of_parents(family, individuals))

        # child born on: 1 day before mother death, 1 day after father death
        husband: Individual = Individual(_id="I0", deat={'date': "3 OCT 2000"})
        wife: Individual = Individual(_id="I1", deat={'date': "5 OCT 2000"})
        child: Individual = Individual(_id="I2", birt={'date': "4 OCT 2000"})
        individuals: List[Individual] = [husband, wife, child]
        family: Family = Family(_id="F2", husb=husband.id, wife=wife.id)
        family.chil.append(child.id)
        self.assertTrue(birth_before_death_of_parents(family, individuals))

        # child born on: after mother death, 10 day after father death
        husband: Individual = Individual(_id="I0", deat={'date': "3 OCT 2000"})
        wife: Individual = Individual(_id="I1", deat={'date': "12 OCT 2000"})
        child: Individual = Individual(_id="I2", birt={'date': "13 OCT 2000"})
        individuals: List[Individual] = [husband, wife, child]
        family: Family = Family(_id="F3", husb=husband.id, wife=wife.id)
        family.chil.append(child.id)
        self.assertFalse(birth_before_death_of_parents(family, individuals))

        # child born on: before mother death, 1 year after father death
        husband: Individual = Individual(_id="I0", deat={'date': "11 OCT 1999"})
        wife: Individual = Individual(_id="I1", deat={'date': "12 OCT 2000"})
        child: Individual = Individual(_id="I2", birt={'date': "11 OCT 2000"})
        individuals: List[Individual] = [husband, wife, child]
        family: Family = Family(_id="F4", husb=husband.id, wife=wife.id)
        family.chil.append(child.id)
        self.assertFalse(birth_before_death_of_parents(family, individuals))


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
