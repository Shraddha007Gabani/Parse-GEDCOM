import unittest
from typing import Optional, Dict, List
from datetime import datetime, date


class Individual:
    """ holds an Individual record """

    def __init__(self, _id=None, name=None, sex=None, birt=None, alive=True, deat=False):
        """ store Individual info """
        self.id = _id
        self.name = name
        self.sex = sex
        self.birt: Optional[Dict[str, str]] = birt
        self.alive = alive
        self.deat: Optional[bool, Dict[str, str]] = deat
        self.famc: List[str] = []
        self.fams: List[str] = []

    def age(self):
        """ calculate age using the birth date """
        today = date.today()
        birthday = datetime.strptime(self.birt['date'], "%d %b %Y")
        age = today.year - birthday.year - \
              ((today.month, today.day) < (birthday.month, birthday.day))
        return age

    def info(self):
        """ return Individual info """
        alive = True if self.deat is False else False
        death = 'NA' if self.deat is False else self.deat['date']
        child = 'NA' if len(self.famc) == 0 else self.famc
        spouse = 'NA' if len(self.fams) == 0 else self.fams
        return [self.id, self.name, self.sex, self.birt['date'],
                self.age(), alive, death, child, spouse]


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
        """ return Family info """
        div = 'NA' if self.div is False else self.div['date']
        chil = 'NA' if len(self.chil) == 0 else self.chil
        h_name = next(individual.name for individual in individuals if individual.id == self.husb)
        w_name = next(individual.name for individual in individuals if individual.id == self.wife)

        return [self.id, self.marr['date'], div, self.husb, h_name, self.wife, w_name, chil]


def male_last_names(family: Family, individulas: List[Individual]):
    ids = [family.husb, family.wife]
    ids.extend(family.chil)
    males = [individual for individual in individulas if individual.sex == 'M' and individual.id in ids]
    names = [male.name.split('/')[1] for male in males]
    print(names)
    return len(set(names)) == 1


class TestUserStory(unittest.TestCase):
    def test_male_last_names(self):
        husband: Individual = Individual(_id="I0", name="Pablo /Escobar/", sex='M')
        wife: Individual = Individual(_id="I1", name="Veronika /Esco/", sex='F')
        child1: Individual = Individual(_id="I2", name="Terry /Escobart/", sex='M')
        child2: Individual = Individual(_id="I3", name="Maria /Escobar/", sex='F')
        family = Family(husb=husband.id, wife=wife.id)
        family.chil = [child1.id, child2.id]
        individuals = [husband, wife, child1, child2]
        self.assertFalse(male_last_names(family, individuals))

        husband: Individual = Individual(_id="I112", name="Naal /Wagas/", sex='M')
        wife: Individual = Individual(_id="I22", name="Veron /Wagadi/", sex='F')
        child1: Individual = Individual(_id="I33", name="Ter /Wagada/", sex='M')
        child2: Individual = Individual(_id="I44", name="Mara /Wagadi/", sex='F')
        family = Family(husb=husband.id, wife=wife.id)
        family.chil = [child1.id, child2.id]
        individuals = [husband, wife, child1, child2]
        self.assertFalse(male_last_names(family, individuals))

        husband: Individual = Individual(_id="I9", name="Eden /Hazard/", sex='M')
        wife: Individual = Individual(_id="I99", name="Veva /Hazard/", sex='F')
        child1: Individual = Individual(_id="I999", name="JR /Hazard/", sex='M')
        child2: Individual = Individual(_id="I9999", name="SR /Hazard/", sex='M')
        family = Family(husb=husband.id, wife=wife.id)
        family.chil = [child1.id, child2.id]
        individuals = [husband, wife, child1, child2]
        self.assertTrue(male_last_names(family, individuals))

        husband: Individual = Individual(_id="I07", name="Reese /Walter/", sex='M')
        wife: Individual = Individual(_id="I177", name="Monica /Walter/", sex='F')
        child1: Individual = Individual(_id="I277", name="Malcom /Walter/", sex='M')
        child2: Individual = Individual(_id="I377", name="Hal /Walters/", sex='M')
        family = Family(husb=husband.id, wife=wife.id)
        family.chil = [child1.id, child2.id]
        individuals = [husband, wife, child1, child2]
        self.assertFalse(male_last_names(family, individuals))

        husband: Individual = Individual(_id="I007", name="Elon /Drogba/", sex='M')
        wife: Individual = Individual(_id="I1008", name="Emma /Drogba/", sex='F')
        child1: Individual = Individual(_id="I2009", name="Agua /Drogba/", sex='F')
        child2: Individual = Individual(_id="I3000", name="Win /Drogbaaa/", sex='F')
        family = Family(husb=husband.id, wife=wife.id)
        family.chil = [child1.id, child2.id]
        individuals = [husband, wife, child1, child2]
        self.assertTrue(male_last_names(family, individuals))


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
