""" Implement test cases for user stories

    date: 30-Sep-2020
    python: v3.8.4
"""

import unittest
from typing import List
from models import Individual, Family
import user_stories as us


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
        self.assertTrue(us.were_parents_over_14(family, individuals))

        # husband 11, wife 20 -> Only wife is over 14 -> False
        husband: Individual = Individual(_id="I2", birt={'date': "2 MAR 2007"})
        wife: Individual = Individual(_id="I3", birt={'date': "11 FEB 2000"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id="F1", husb=husband.id, wife=wife.id,
                                marr={'date': "11 FEB 2019"})
        self.assertFalse(us.were_parents_over_14(family, individuals))

        # husband 17, wife 10 -> Only husband is over 14 -> False
        husband: Individual = Individual(_id="I4", birt={'date': "22 AUG 2000"})
        wife: Individual = Individual(_id="I5", birt={'date': "5 DEC 2007"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id="F2", husb=husband.id, wife=wife.id,
                                marr={'date': "11 FEB 2018"})
        self.assertFalse(us.were_parents_over_14(family, individuals))

        # husband 12, wife 12 -> Both are under 14 -> False
        husband: Individual = Individual(_id="I6", birt={'date': "19 SEP 2007"})
        wife: Individual = Individual(_id="I7", birt={'date': "3 JAN 2008"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id="F3", husb=husband.id, wife=wife.id,
                                marr={'date': "11 FEB 2020"})
        self.assertFalse(us.were_parents_over_14(family, individuals))

        # husband 18, wife 16 -> Both are over 14 -> True
        husband: Individual = Individual(_id="I8", birt={'date': "7 FEB 1980"})
        wife: Individual = Individual(_id="I9", birt={'date': "8 FEB 1982"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id="F4", husb=husband.id, wife=wife.id,
                                marr={'date': "11 FEB 1998"})
        self.assertTrue(us.were_parents_over_14(family, individuals))

    def test_birth_before_death_of_parents(self):
        """ test birth_before_death_of_parents method """
        # mother and father are alive (no death date)
        husband: Individual = Individual(_id="I0")
        wife: Individual = Individual(_id="I1")
        child: Individual = Individual(_id="I2", birt={'date': "4 OCT 2000"})
        individuals: List[Individual] = [husband, wife, child]
        family: Family = Family(_id="F0", husb=husband.id, wife=wife.id)
        family.chil.append(child.id)
        self.assertTrue(us.birth_before_death_of_parents(family, individuals))

        # child born on: mother death, 270 day after father death
        husband: Individual = Individual(_id="I0", deat={'date': "8 JAN 2000"})
        wife: Individual = Individual(_id="I1", deat={'date': "4 OCT 2000"})
        child: Individual = Individual(_id="I2", birt={'date': "4 OCT 2000"})
        individuals: List[Individual] = [husband, wife, child]
        family: Family = Family(_id="F1", husb=husband.id, wife=wife.id)
        family.chil.append(child.id)
        self.assertTrue(us.birth_before_death_of_parents(family, individuals))

        # child born on: 1 day before mother death, 1 day after father death
        husband: Individual = Individual(_id="I0", deat={'date': "3 OCT 2000"})
        wife: Individual = Individual(_id="I1", deat={'date': "5 OCT 2000"})
        child: Individual = Individual(_id="I2", birt={'date': "4 OCT 2000"})
        individuals: List[Individual] = [husband, wife, child]
        family: Family = Family(_id="F2", husb=husband.id, wife=wife.id)
        family.chil.append(child.id)
        self.assertTrue(us.birth_before_death_of_parents(family, individuals))

        # child born on: after mother death, 10 day after father death
        husband: Individual = Individual(_id="I0", deat={'date': "3 OCT 2000"})
        wife: Individual = Individual(_id="I1", deat={'date': "12 OCT 2000"})
        child: Individual = Individual(_id="I2", birt={'date': "13 OCT 2000"})
        individuals: List[Individual] = [husband, wife, child]
        family: Family = Family(_id="F3", husb=husband.id, wife=wife.id)
        family.chil.append(child.id)
        self.assertFalse(us.birth_before_death_of_parents(family, individuals))

        # child born on: before mother death, 1 year after father death
        husband: Individual = Individual(_id="I0", deat={'date': "11 OCT 1999"})
        wife: Individual = Individual(_id="I1", deat={'date': "12 OCT 2000"})
        child: Individual = Individual(_id="I2", birt={'date': "11 OCT 2000"})
        individuals: List[Individual] = [husband, wife, child]
        family: Family = Family(_id="F4", husb=husband.id, wife=wife.id)
        family.chil.append(child.id)
        self.assertFalse(us.birth_before_death_of_parents(family, individuals))

    def test_fewer_than_15_siblings(self):
        husband: Individual = Individual(_id="I0")
        wife: Individual = Individual(_id="I1")
        child1: Individual = Individual(_id="I2")
        child2: Individual = Individual(_id="I3")
        child3: Individual = Individual(_id="I4")
        child4: Individual = Individual(_id="I5")
        child5: Individual = Individual(_id="I6")
        child6: Individual = Individual(_id="I7")
        child7: Individual = Individual(_id="I8")
        child8: Individual = Individual(_id="I9")
        child9: Individual = Individual(_id="I10")
        child10: Individual = Individual(_id="I12")
        child11: Individual = Individual(_id="I13")
        child12: Individual = Individual(_id="I14")
        child13: Individual = Individual(_id="I15")
        child14: Individual = Individual(_id="I16")
        child15: Individual = Individual(_id="I17")
        family: Family = Family(husb=husband.id, wife=wife.id)
        family.chil.extend([child1.id, child2.id, child3.id, child4.id, child5.id, child6.id,
                            child7.id, child8.id, child9.id, child10.id, child11.id, child12.id,
                            child13.id, child14.id, child15.id])
        self.assertFalse(us.fewer_than_15_siblings(family))

        family: Family = Family(husb=husband.id, wife=wife.id)
        family.chil.extend([child1.id, child2.id, child3.id, child4.id, child5.id, child6.id])
        self.assertTrue(us.fewer_than_15_siblings(family))

    def test_male_last_names(self):
        husband: Individual = Individual(_id="I0", name="Pablo /Escobar/", sex='M')
        wife: Individual = Individual(_id="I1", name="Veronika /Esco/", sex='F')
        child1: Individual = Individual(_id="I2", name="Terry /Escobart/", sex='M')
        child2: Individual = Individual(_id="I3", name="Maria /Escobar/", sex='F')
        family = Family(husb=husband.id, wife=wife.id)
        family.chil = [child1.id, child2.id]
        individuals = [husband, wife, child1, child2]
        self.assertFalse(us.male_last_names(family, individuals))

        husband: Individual = Individual(_id="I112", name="Naal /Wagas/", sex='M')
        wife: Individual = Individual(_id="I22", name="Veron /Wagadi/", sex='F')
        child1: Individual = Individual(_id="I33", name="Ter /Wagada/", sex='M')
        child2: Individual = Individual(_id="I44", name="Mara /Wagadi/", sex='F')
        family = Family(husb=husband.id, wife=wife.id)
        family.chil = [child1.id, child2.id]
        individuals = [husband, wife, child1, child2]
        self.assertFalse(us.male_last_names(family, individuals))

        husband: Individual = Individual(_id="I9", name="Eden /Hazard/", sex='M')
        wife: Individual = Individual(_id="I99", name="Veva /Hazard/", sex='F')
        child1: Individual = Individual(_id="I999", name="JR /Hazard/", sex='M')
        child2: Individual = Individual(_id="I9999", name="SR /Hazard/", sex='M')
        family = Family(husb=husband.id, wife=wife.id)
        family.chil = [child1.id, child2.id]
        individuals = [husband, wife, child1, child2]
        self.assertTrue(us.male_last_names(family, individuals))

        husband: Individual = Individual(_id="I07", name="Reese /Walter/", sex='M')
        wife: Individual = Individual(_id="I177", name="Monica /Walter/", sex='F')
        child1: Individual = Individual(_id="I277", name="Malcom /Walter/", sex='M')
        child2: Individual = Individual(_id="I377", name="Hal /Walters/", sex='M')
        family = Family(husb=husband.id, wife=wife.id)
        family.chil = [child1.id, child2.id]
        individuals = [husband, wife, child1, child2]
        self.assertFalse(us.male_last_names(family, individuals))

        husband: Individual = Individual(_id="I007", name="Elon /Drogba/", sex='M')
        wife: Individual = Individual(_id="I1008", name="Emma /Drogba/", sex='F')
        child1: Individual = Individual(_id="I2009", name="Agua /Drogba/", sex='F')
        child2: Individual = Individual(_id="I3000", name="Win /Drogbaaa/", sex='F')
        family = Family(husb=husband.id, wife=wife.id)
        family.chil = [child1.id, child2.id]
        individuals = [husband, wife, child1, child2]
        self.assertTrue(us.male_last_names(family, individuals))
     # Test cases of user story 14
         def test_verifySiblingsDates(self):
        date1 = datetime.date(1990, 1, 1)
        date2 = datetime.date(1991, 1, 1)
        date3 = datetime.date(1992, 1, 1)
        date4 = datetime.date(1993, 1, 1)
        date5 = datetime.date(1994, 1, 1)
        date6 = datetime.date(1995, 1, 1)
        siblingsDates = (date1, date2, date3, date4, date5, date6)
        self.assertTrue(user_stories.verifySiblingsDates(siblingsDates))

    def test_verifySiblingsDates(self):
        date1 = datetime.date(1990, 1, 1)
        date2 = datetime.date(1990, 1, 1)
        date3 = datetime.date(1990, 1, 1)
        date4 = datetime.date(1993, 1, 1)
        date5 = datetime.date(1994, 1, 1)
        date6 = datetime.date(1995, 1, 1)
        siblingsDates = (date1, date2, date3, date4, date5, date6)
        self.assertTrue(user_stories.verifySiblingsDates(siblingsDates))

    def test_verifySiblingsDates(self):
        date1 = datetime.date(1990, 1, 1)
        date2 = datetime.date(1990, 1, 1)
        date3 = datetime.date(1990, 1, 1)
        date4 = datetime.date(1990, 1, 1)
        date5 = datetime.date(1990, 1, 1)
        date6 = datetime.date(1990, 1, 1)
        siblingsDates = (date1, date2, date3, date4, date5, date6)
        self.assertFalse(user_stories.verifySiblingsDates(siblingsDates))

    def test_verifySiblingsDates(self):
        date1 = datetime.date(1990, 1, 2)
        date2 = datetime.date(1990, 1, 1)
        date3 = datetime.date(1990, 1, 2)
        date4 = datetime.date(1990, 1, 1)
        date5 = datetime.date(1990, 1, 1)
        date6 = datetime.date(1990, 1, 1)
        siblingsDates = (date1, date2, date3, date4, date5, date6)
        self.assertFalse(user_stories.verifySiblingsDates(siblingsDates))
    # Test cases of user story 13
         def test_alldifferentDates(self):
        date1 = datetime.date(1990, 1, 1)
        date2 = datetime.date(1991, 1, 1)
        date3 = datetime.date(1992, 1, 1)
        siblingsDates = (date1, date2, date3)
        self.assertTrue(user_stories.verifySiblingsSpace(siblingsDates))

    def test_someDifferentDatesSameYear(self):
        date1 = datetime.date(1990, 1, 1)
        date2 = datetime.date(1990, 11, 1)
        date3 = datetime.date(1991, 12, 1)
        siblingsDates = (date1, date2, date3)
        self.assertTrue(user_stories.verifySiblingsSpace(siblingsDates))

    def test_allSameDates(self):
        date1 = datetime.date(1990, 1, 1)
        date2 = datetime.date(1990, 1, 1)
        date3 = datetime.date(1990, 1, 1)
        siblingsDates = (date1, date2, date3)
        self.assertFalse(user_stories.verifySiblingsSpace(siblingsDates))

    def test_someWithDayDifference(self):
        date1 = datetime.date(1990, 1, 2)
        date2 = datetime.date(1990, 1, 1)
        date3 = datetime.date(1990, 1, 2)
        siblingsDates = (date1, date2, date3)
        self.assertFalse(user_stories.verifySiblingsSpace(siblingsDates))

    def test_someWithMonthsDifference(self):
        date1 = datetime.date(1990, 1, 1)
        date2 = datetime.date(1990, 6, 1)
        date3 = datetime.date(1992, 1, 2)
        siblingsDates = (date1, date2, date3)
        self.assertFalse(user_stories.verifySiblingsSpace(siblingsDates))
if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
