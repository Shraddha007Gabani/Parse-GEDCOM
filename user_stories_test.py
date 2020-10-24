""" Implement test cases for user stories

    date: 30-Sep-2020
    python: v3.8.4
"""
import datetime
import unittest
from typing import List, Dict

import user_stories
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

    def test_marriage_before_death(self):
        
        husband: Individual = Individual(_id="I0", deat={'date': "1 JAN 2020"})
        wife: Individual = Individual(_id="I1", deat={'date': "2 JAN 2019"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, marr={'date': "11 FEB 1999"})
        self.assertTrue(us.marriage_before_death(family, individuals))

        """Husband and wife they both die before their marriage so False (not possible)"""
        husband: Individual = Individual(_id="I2", deat={'date': "1 JAN 2000"})
        wife: Individual = Individual(_id="I3", deat={'date': "2 JAN 2000"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, marr={'date': "11 FEB 2001"})
        self.assertFalse(us.marriage_before_death(family, individuals))

        """ Husband dies before marriage wife is alive so False (not possible)"""
        husband: Individual = Individual(_id="I4", deat={'date': "1 JAN 2000"})
        wife: Individual = Individual(_id="I5")
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, marr={'date': "11 FEB 2001"})
        self.assertFalse(us.marriage_before_death(family, individuals))

        """ Husband dies after marriage and  wife is alive so true"""
        husband: Individual = Individual(_id="I4", deat={'date': "1 JAN 2002"})
        wife: Individual = Individual(_id="I5")
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, marr={'date': "11 FEB 2001"})
        self.assertTrue(us.marriage_before_death(family, individuals))

        """Wife dies before marriage and Husband is alive so False (not possible)"""
        husband: Individual = Individual(_id="I6")
        wife: Individual = Individual(_id="I7", deat={'date': "1 JAN 2000"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, marr={'date': "11 FEB 2001"})
        self.assertFalse(us.marriage_before_death(family, individuals))

        """Wife dies after marriage and Husband is alive so true"""
        husband: Individual = Individual(_id="I8")
        wife: Individual = Individual(_id="I9",  deat={'date': "1 JAN 2002"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, marr={'date': "11 FEB 2001"})
        self.assertTrue(us.marriage_before_death(family, individuals))

        """ Husband and wife they both are alive no daeth date is found so false"""
        husband: Individual = Individual(_id="I10")
        wife: Individual = Individual(_id="I11")
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, marr={'date': "11 FEB 2002"})
        self.assertFalse(us.marriage_before_death(family, individuals))

    def test_divorce_before_death(self):
            
            husband: Individual = Individual(_id="I0", deat={'date': "1 JAN 2020"})
            wife: Individual = Individual(_id="I1", deat={'date': "2 JAN 2019"})
            individuals: List[Individual] = [husband, wife]
            family: Family = Family(husb=husband.id, wife=wife.id, div={'date': "11 FEB 1999"})
            self.assertTrue(us.divorce_before_death(family, individuals))

            """Husband and wife they both die before their divorce so False (not possible)"""
            husband: Individual = Individual(_id="I2", deat={'date': "1 JAN 2000"})
            wife: Individual = Individual(_id="I3", deat={'date': "2 JAN 2000"})
            individuals: List[Individual] = [husband, wife]
            family: Family = Family(husb=husband.id, wife=wife.id, div={'date': "11 FEB 2001"})
            self.assertFalse(us.divorce_before_death(family, individuals))

            """ Husband dies before divorce wife is alive so False (not possible)"""
            husband: Individual = Individual(_id="I4", deat={'date': "1 JAN 2000"})
            wife: Individual = Individual(_id="I5")
            individuals: List[Individual] = [husband, wife]
            family: Family = Family(husb=husband.id, wife=wife.id, div={'date': "11 FEB 2001"})
            self.assertFalse(us.divorce_before_death(family, individuals))

            """ Husband dies after divorce and  wife is alive so true"""
            husband: Individual = Individual(_id="I4", deat={'date': "1 JAN 2002"})
            wife: Individual = Individual(_id="I5")
            individuals: List[Individual] = [husband, wife]
            family: Family = Family(husb=husband.id, wife=wife.id, div={'date': "11 FEB 2001"})
            self.assertTrue(us.divorce_before_death(family, individuals))

            """Wife dies before divorce and Husband is alive so False (not possible)"""
            husband: Individual = Individual(_id="I6")
            wife: Individual = Individual(_id="I7", deat={'date': "1 JAN 2000"})
            individuals: List[Individual] = [husband, wife]
            family: Family = Family(husb=husband.id, wife=wife.id, div={'date': "11 FEB 2001"})
            self.assertFalse(us.divorce_before_death(family, individuals))

            """Wife dies after divorce and Husband is alive so true"""
            husband: Individual = Individual(_id="I8")
            wife: Individual = Individual(_id="I9",  deat={'date': "1 JAN 2002"})
            individuals: List[Individual] = [husband, wife]
            family: Family = Family(husb=husband.id, wife=wife.id, div={'date': "11 FEB 2001"})
            self.assertTrue(us.divorce_before_death(family, individuals))

            """ Husband and wife they both are alive no divorce date is found so false"""
            husband: Individual = Individual(_id="I10")
            wife: Individual = Individual(_id="I11")
            individuals: List[Individual] = [husband, wife]
            family: Family = Family(husb=husband.id, wife=wife.id, div={'date': "11 FEB 2002"})
            self.assertFalse(us.divorce_before_death(family, individuals))

    def test_checkForOldParents(self):
        """Test cases for checking parents are old or not US12"""
        f = open("Output.txt", "a+")
        fam: Dict = {'F23':
                         {'fam': 'F23', 'MARR': '14 FEB 1980', 'HUSB': 'I01', 'WIFE': 'I07',
                          'CHIL': ['I19', 'I26', 'I30']},
                     'F16': {'fam': 'F16', 'MARR': '12 DEC 2007'}}
        fam2: Dict = {'F23': {'fam': 'F23', 'MARR': '14 FEB 1980', 'HUSB': 'I01', 'WIFE': 'I07', 'CHIL': ['I19']}}

        ind1: Dict = {'I01': {'id': 'I01', 'name': 'Joe /Smith/', 'BIRT': '15 JUL 1900', 'sex': 'M', 'family': 'F23',
                              'DEAT': '31 DEC 2013'},
                      'I07': {'id': 'I07', 'name': 'Jennifer /Smith/', 'BIRT': '23 SEP 1902', 'sex': 'F',
                              'family': 'F23',
                              'DEAT': '31 DEC 2013'},
                      'I19': {'id': 'I19', 'name': 'Dick /Smith/', 'BIRT': '13 FEB 1999', 'sex': 'M', 'family': 'F23',
                              'DEAT': '31 DEC 2013'}}

        ind2: Dict = {'I01': {'id': 'I01', 'name': 'Joe /Smith/', 'BIRT': '15 JUL 1960', 'sex': 'M', 'family': 'F23',
                              'DEAT': '31 DEC 2013'},
                      'I07': {'id': 'I07', 'name': 'Jennifer /Smith/', 'BIRT': '23 SEP 1960', 'sex': 'F',
                              'family': 'F23'},
                      'I19': {'id': 'I19', 'name': 'Dick /Smith/', 'BIRT': '13 FEB 1981', 'sex': 'M', 'family': 'F23'},
                      'I26': {'id': 'I26', 'name': 'Jane /Smith/', 'BIRT': '13 FEB 1981', 'sex': 'F', 'family': 'F23'},
                      'I30': {'id': 'I30', 'name': 'Mary /Test/', 'BIRT': '13 FEB 1981', 'sex': 'F', 'family': 'F23'},
                      'I32': {'id': 'I32', 'name': 'Nick /Tary/', 'BIRT': '13 FEB 1981', 'sex': 'M', 'family': 'F23'},
                      'I44': {'id': 'I44', 'name': 'Cersi /Lanister/', 'BIRT': '13 FEB 1981', 'sex': 'F',
                              'family': 'F23'}}

        self.assertTrue(us.checkForOldParents(fam, ind2, f))
        self.assertFalse(us.checkForOldParents(fam2, ind1, f))

    def test_checkBigamy(self):
        """Test cases for bigamy"""

        # No Bigamy
        fam: Dict = {'F23':
                         {'fam': 'F23', 'MARR': '14 FEB 1980', 'HUSB': 'I01', 'WIFE': 'I07',
                          'CHIL': ['I19', 'I26', 'I30']},
                     'F16': {'fam': 'F16', 'MARR': '12 DEC 2007'}}

        indi: Dict = {
            'I01': {'id': 'I01', 'name': 'Joe /Smith/', 'BIRT': '15 JUL 1960', 'sex': 'M', 'family': 'F23',
                    'DEAT': '31 DEC 2013'},
            'I07': {'id': 'I07', 'name': 'Jennifer /Smith/', 'BIRT': '23 SEP 1960', 'sex': 'F',
                    'family': 'F23'},
            'I19': {'id': 'I19', 'name': 'Dick /Smith/', 'BIRT': '13 FEB 1981', 'sex': 'M', 'family': 'F23'},
            'I26': {'id': 'I26', 'name': 'Jane /Smith/', 'BIRT': '13 FEB 1981', 'sex': 'F', 'family': 'F23'},
            'I30': {'id': 'I30', 'name': 'Mary /Test/', 'BIRT': '13 FEB 1981', 'sex': 'F', 'family': 'F23'},
            'I32': {'id': 'I32', 'name': 'Nick /Tary/', 'BIRT': '13 FEB 1981', 'sex': 'M', 'family': 'F23'},
            'I44': {'id': 'I44', 'name': 'Cersi /Lanister/', 'BIRT': '13 FEB 1981', 'sex': 'F',
                    'family': 'F23'}}

        # bigamy (same husband)
        fam2: Dict = {'F23':
                          {'fam': 'F23', 'MARR': '14 FEB 1980', 'HUSB': 'I01', 'WIFE': 'I07',
                           'CHIL': ['I19', 'I26', 'I30']},
                      'F16': {'fam': 'F16', 'MARR': '12 DEC 2007', 'HUSB': 'I01'}}

        indi2: Dict = {
            'I01': {'id': 'I01', 'name': 'Joe /Smith/', 'BIRT': '15 JUL 1960', 'sex': 'M', 'family': 'F23',
                    'DEAT': '31 DEC 2013'},
            'I07': {'id': 'I07', 'name': 'Jennifer /Smith/', 'BIRT': '23 SEP 1960', 'sex': 'F',
                    'family': 'F23'},
            'I19': {'id': 'I19', 'name': 'Dick /Smith/', 'BIRT': '13 FEB 1981', 'sex': 'M', 'family': 'F23'},
            'I26': {'id': 'I26', 'name': 'Jane /Smith/', 'BIRT': '13 FEB 1981', 'sex': 'F', 'family': 'F23'},
            'I30': {'id': 'I30', 'name': 'Mary /Test/', 'BIRT': '13 FEB 1981', 'sex': 'F', 'family': 'F23'},
            'I32': {'id': 'I32', 'name': 'Nick /Tary/', 'BIRT': '13 FEB 1981', 'sex': 'M', 'family': 'F23'},
            'I44': {'id': 'I44', 'name': 'Cersi /Lanister/', 'BIRT': '13 FEB 1981', 'sex': 'F',
                    'family': 'F23'}}

        # bigamy (same wife)
        fam3: Dict = {'F23':
                          {'fam': 'F23', 'MARR': '14 FEB 1980', 'HUSB': 'I01', 'WIFE': 'I07',
                           'CHIL': ['I19', 'I26', 'I30']},
                      'F16': {'fam': 'F16', 'MARR': '12 DEC 2007', 'WIFE': 'I07'}}

        indi3: Dict = {
            'I01': {'id': 'I01', 'name': 'Joe /Smith/', 'BIRT': '15 JUL 1960', 'sex': 'M', 'family': 'F23',
                    'DEAT': '31 DEC 2013'},
            'I07': {'id': 'I07', 'name': 'Jennifer /Smith/', 'BIRT': '23 SEP 1960', 'sex': 'F',
                    'family': 'F23'},
            'I19': {'id': 'I19', 'name': 'Dick /Smith/', 'BIRT': '13 FEB 1981', 'sex': 'M', 'family': 'F23'},
            'I26': {'id': 'I26', 'name': 'Jane /Smith/', 'BIRT': '13 FEB 1981', 'sex': 'F', 'family': 'F23'},
            'I30': {'id': 'I30', 'name': 'Mary /Test/', 'BIRT': '13 FEB 1981', 'sex': 'F', 'family': 'F23'},
            'I32': {'id': 'I32', 'name': 'Nick /Tary/', 'BIRT': '13 FEB 1981', 'sex': 'M', 'family': 'F23'},
            'I44': {'id': 'I44', 'name': 'Cersi /Lanister/', 'BIRT': '13 FEB 1981', 'sex': 'F',
                    'family': 'F23'}}

        us.checkBigamy(fam)
        self.assertTrue(('I01' in indi))
        self.assertTrue(('I01' == fam['F23']['HUSB']))
        us.checkBigamy(fam2)
        self.assertTrue(('I01' in indi2))
        self.assertTrue(('I01' in fam2['F23']['HUSB']))
        us.checkBigamy(fam3)
        self.assertTrue(('I07' in indi3))
        self.assertTrue(('WIFE' in fam3['F23']))

    def test_birth_before_marriage_of_parents(self):
        individual = Individual(_id="I20", birt={'date': "11 nov 2008"})
        family = Family(_id="I21" , marr={'date': "10 jan 2008"}, div= {'date':"15 JAN 2009"})
        self.assertTrue(us.birth_before_marriage_of_parents(family, individual))

        individual = Individual(_id="I20", birt={'date': "11 nov 2009"})
        family = Family(_id="I21" , marr={'date': "10 may 2008"}, div= {'date':"15 jul 2008"})
        self.assertFalse(us.birth_before_marriage_of_parents(family, individual))

        individual = Individual(_id="I20", birt={'date': "12  dec 2009"})
        family = Family(_id="I21" , marr={'date': "11 may 2008"}, div= {'date':"15 sep 2008"})
        self.assertFalse(us.birth_before_marriage_of_parents(family, individual))

        individual = Individual(_id="I20", birt={'date': "12  dec 2009"})
        family = Family(_id="I21" , marr={'date': "11 may 2009"}, div= {'date':"15 sep 2009"})
        self.assertTrue(us.birth_before_marriage_of_parents(family, individual))

    def test_less_than_150(self):
        individual = Individual(birt={'date': "20 Mar 1985"})
        individual.deat = {'date': "15 Aug 2008"}
        self.assertTrue(us.less_than_150(individual))

        individual = Individual(birt={'date': "15 JAN 2000"})
        self.assertTrue(us.less_than_150(individual))

        individual = Individual(birt={'date': "15 Feb 2012"})
        individual.deat = {'date': "21 JAN 2000"}
        self.assertFalse(us.less_than_150(individual))

        individual = Individual(birt={'date': "15 JAN 1500"})
        self.assertFalse(us.less_than_150(individual))

        individual = Individual(birt={'date': "15 JAN 2006"})
        individual.deat = {'date': "15 JAN 1200"}
        self.assertFalse(us.less_than_150(individual))

    def test_dates_before_current(self):
        family = Family(_id="I21", marr={'date': "15 JAN 2019"}) ##marrige date is before
        # current date so result is true
        self.assertTrue(us.marriage(family))

        family = Family(_id="I22", div={'date': "15 JAN 2020"}) ##divorse date is before current date so result is true
        self.assertTrue(us.divo(family))

        Indi = Individual(_id="I23", birt={'date': "15 JAN 2021"}) ##Birth date is after current date so result is false
        self.assertFalse(us.birth(Indi))

        Indi = Individual(_id="I24", deat={'date': "15 JAN 2021"}) ##death date is after current date so result is false
        self.assertFalse(us.death(Indi))

        Indi = Individual(_id="I26", birt={'date': "15 JAN 2020"}) ##Birth date is before current date so result is true
        self.assertTrue(us.birth(Indi))

    def test_Birth_before_death(self):
        individual = Individual(_id='I20', birt={'date': "15 JAN 1995"})
        individual.deat = {'date': "15 JAN 1994"}
        self.assertFalse(us.birth_before_death(individual))

        individual = Individual(_id='I21', birt={'date': "15 JAN 1995"})
        individual.deat = {'date': "15 JAN 1996"}
        self.assertTrue(us.birth_before_death(individual))

        individual = Individual(_id='I22', birt={'date': "25 DEC 1996"})
        individual.deat = {'date': "26 DEC 1996"}
        self.assertTrue(us.birth_before_death(individual))

        individual = Individual(_id='I23', birt={'date': "26 dec 1995"})
        individual.deat = {'date': "25 dec 1995"}
        self.assertFalse(us.birth_before_death(individual))

        individual = Individual(_id='I24', birt={'date': "25 JAN 1996"})
        individual.deat = {'date': "25 dec 1997"}
        self.assertTrue(us.birth_before_death(individual))

        individual = Individual(_id='I25', birt={'date': "26 JAN 1997"})
        individual.deat = {'date': "25 dec 1996"}
        self.assertFalse(us.birth_before_death(individual))

        individual = Individual(_id='I26', birt={'date': "26 JAN 1997"})
        self.assertTrue(us.birth_before_death(individual))

    def test_marriage_before_divorce(self):
        family = Family(_id='I20', marr={'date': "15 JAN 1995"})
        family.div = {'date': "15 JAN 1994"}
        self.assertFalse(us.marriage_before_divorce(family))

        family = Family(_id='I21', marr={'date': "15 JAN 1995"})
        family.div = {'date': "15 JAN 1996"}
        self.assertTrue(us.marriage_before_divorce(family))

        family = Family(_id='I22', marr={'date': "25 DEC 1996"})
        family.div = {'date': "26 dec 1996"}
        self.assertTrue(us.marriage_before_divorce(family))

        family = Family(_id='I23', marr={'date': "26 DEC 1996"})
        family.div = {'date': "25 dec 1996"}
        self.assertFalse(us.marriage_before_divorce(family))

        family = Family(_id='I24', marr={'date': "25 jan 1996"})
        family.div = {'date': "25 dec 1997"}
        self.assertTrue(us.marriage_before_divorce(family))

        family = Family(_id='I25', marr={'date': "26 jan 1997"})
        family.div = {'date': "25 dec 1996"}
        self.assertFalse(us.marriage_before_divorce(family))

        family = Family(_id='I26', marr={'date': "26 jan 1997"})
        self.assertTrue(us.marriage_before_divorce(family))

    def test_Birth_before_mrg(self):
        indi = Individual(_id="I20", birt={'date': "15 JAN 2020"})
        family = Family(marr={'date': "15 JAN 2019"})  # marrige date is before birth date so result is fasle
        self.assertFalse(us.birth_before_mrg(family, indi))

        indi = Individual(_id="I21", birt={'date': "5 JUL 2000"})
        family = Family(marr={'date': "1 JAN 2010"}) # marrige date is after birth date so result is true
        self.assertTrue(us.birth_before_mrg(family, indi))

        indi = Individual(_id="I22", birt={'date': "7 JUN 2000"})
        family = Family(marr={'date': "9 JAN 1995"})  # marrige date is before birth date so result is false
        self.assertFalse(us.birth_before_mrg(family, indi))

        indi = Individual(_id="I23", birt={'date': "15 MAY 1989"})
        family = Family(marr={'date': "15 FEB 2000"})  # marrige date is after birth date so result is true
        self.assertTrue(us.birth_before_mrg(family, indi))

        indi = Individual(_id="I24", birt={'date': "15 JAN 2020"})
        family = Family(marr=None)  # marriage is not take place so result is by default true
        self.assertTrue(us.birth_before_mrg(family, indi))

    def test_verifySiblingsDates(self):
        date1 = datetime.date(1990, 1, 1)
        date2 = datetime.date(1991, 1, 1)
        date3 = datetime.date(1992, 1, 1)
        date4 = datetime.date(1993, 1, 1)
        date5 = datetime.date(1994, 1, 1)
        date6 = datetime.date(1995, 1, 1)
        siblingsDates = (date1, date2, date3, date4, date5, date6)
        self.assertTrue(user_stories.verifySiblingsDates(siblingsDates))

        date1 = datetime.date(1990, 1, 1)
        date2 = datetime.date(1990, 1, 1)
        date3 = datetime.date(1990, 1, 1)
        date4 = datetime.date(1993, 1, 1)
        date5 = datetime.date(1994, 1, 1)
        date6 = datetime.date(1995, 1, 1)
        siblingsDates = (date1, date2, date3, date4, date5, date6)
        self.assertTrue(user_stories.verifySiblingsDates(siblingsDates))

        date1 = datetime.date(1990, 1, 1)
        date2 = datetime.date(1990, 1, 1)
        date3 = datetime.date(1990, 1, 1)
        date4 = datetime.date(1990, 1, 1)
        date5 = datetime.date(1990, 1, 1)
        date6 = datetime.date(1990, 1, 1)
        siblingsDates = (date1, date2, date3, date4, date5, date6)
        self.assertFalse(user_stories.verifySiblingsDates(siblingsDates))

        date1 = datetime.date(1990, 1, 2)
        date2 = datetime.date(1990, 1, 1)
        date3 = datetime.date(1990, 1, 2)
        date4 = datetime.date(1990, 1, 1)
        date5 = datetime.date(1990, 1, 1)
        date6 = datetime.date(1990, 1, 1)
        siblingsDates = (date1, date2, date3, date4, date5, date6)
        self.assertFalse(user_stories.verifySiblingsDates(siblingsDates))

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

    def test_correct_gender_for_role(self):
        """ test correct_gender_for_role method """
        # husband is Male, wife is Female
        husband: Individual = Individual(_id="I0", sex='M')
        wife: Individual = Individual(_id="I1", sex='F')
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id='F0', husb=husband.id, wife=wife.id)
        self.assertTrue(us.correct_gender_for_role(family, individuals))

        # husband is Male, wife is Male
        husband: Individual = Individual(_id="I0", sex='M')
        wife: Individual = Individual(_id="I1", sex='M')
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id='F1', husb=husband.id, wife=wife.id)
        self.assertFalse(us.correct_gender_for_role(family, individuals))

        # husband is Female, wife is Female
        husband: Individual = Individual(_id="I0", sex='F')
        wife: Individual = Individual(_id="I1", sex='F')
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id='F2', husb=husband.id, wife=wife.id)
        self.assertFalse(us.correct_gender_for_role(family, individuals))

        # husband is Female, wife is Male
        husband: Individual = Individual(_id="I0", sex='F')
        wife: Individual = Individual(_id="I1", sex='M')
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id='F3', husb=husband.id, wife=wife.id)
        self.assertFalse(us.correct_gender_for_role(family, individuals))

    def test_unique_ids(self):
        """ test unique_ids method """
        husband1: Individual = Individual(_id="I0")
        wife1: Individual = Individual(_id="I1")
        child1: Individual = Individual(_id="I2")
        child2: Individual = Individual(_id="I3")
        family1: Family = Family(_id='F0', husb=husband1.id, wife=wife1.id)

        husband2: Individual = Individual(_id="I4")
        wife2: Individual = Individual(_id="I5")
        child3: Individual = Individual(_id="I6")
        child4: Individual = Individual(_id="I7")
        family2: Family = Family(_id='F1', husb=husband2.id, wife=wife2.id)

        individuals = [husband1, wife1, husband2, wife2, child1, child2, child3, child4]
        families = [family1, family2]

        self.assertTrue(us.unique_ids(families, individuals))

        husband1: Individual = Individual(_id="I0")
        wife1: Individual = Individual(_id="I1")
        child1: Individual = Individual(_id="I3")
        child2: Individual = Individual(_id="I3")
        family1: Family = Family(_id='F0', husb=husband1.id, wife=wife1.id)

        husband2: Individual = Individual(_id="I4")
        wife2: Individual = Individual(_id="I5")
        child3: Individual = Individual(_id="I6")
        child4: Individual = Individual(_id="I7")
        family2: Family = Family(_id='F0', husb=husband2.id, wife=wife2.id)

        individuals = [husband1, wife1, husband2, wife2, child1, child2, child3, child4]
        families = [family1, family2]

        self.assertFalse(us.unique_ids(families, individuals))

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
