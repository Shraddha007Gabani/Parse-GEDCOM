""" Implement user stories for GEDCOM parser

    date: 30-Sep-2020
    python: v3.8.4
"""

from typing import List
from datetime import datetime, timedelta
from models import Individual, Family


def birth_before_death_of_parents(family: Family, individuals: List[Individual]) -> bool:
    """ US09: verify that children are born before death of mother
        and before 9 months after death of father """

    husb = next(ind for ind in individuals if ind.id == family.husb)
    wife = next(ind for ind in individuals if ind.id == family.wife)

    if not husb.deat and not wife.alive:
        return True

    for child_id in family.chil:
        child_birth_date = next(ind.birt['date'] for ind in individuals if ind.id == child_id)
        child_birth_date = datetime.strptime(child_birth_date, "%d %b %Y")

        if husb.deat:
            husb_death_date = husb.deat['date']
            husb_death_date = datetime.strptime(husb_death_date, "%d %b %Y")

            if child_birth_date > husb_death_date + timedelta(days=270):
                print(f"✘ Family ({family.id}): Child ({child_id}) should be born "
                      f"before 9 months after death of father")
                return False

        if wife.deat:
            wife_death_date = wife.deat['date']
            wife_death_date = datetime.strptime(wife_death_date, "%d %b %Y")

            if child_birth_date > wife_death_date:
                print(f"✘ Family ({family.id}): Child ({child_id}) should be born before death of mother")
                return False
    else:
        print(f"✔ Family ({family.id}): Children are born before death of mother "
              f"and before 9 months after death of father")
        return True


def were_parents_over_14(family: Family, individuals: List[Individual]) -> bool:
    """ US10: verify that parents were at least 14 years old at the marriage date """
    marr_date: datetime = datetime.strptime(family.marr['date'], "%d %b %Y")

    husb_birthday = next(ind.birt['date'] for ind in individuals if ind.id == family.husb)
    husb_birthday = datetime.strptime(husb_birthday, "%d %b %Y")
    husb_marr_age = marr_date.year - husb_birthday.year - \
                    ((marr_date.month, marr_date.day) < (husb_birthday.month, husb_birthday.day))

    wife_birthday = next(ind.birt['date'] for ind in individuals if ind.id == family.wife)
    wife_birthday = datetime.strptime(wife_birthday, "%d %b %Y")
    wife_marr_age = marr_date.year - wife_birthday.year - \
                    ((marr_date.month, marr_date.day) < (wife_birthday.month, wife_birthday.day))

    if husb_marr_age >= 14 and wife_marr_age >= 14:
        print(f"✔ Family ({family.id}): Both parents were at least 14 at the marriage date")
        return True

    if husb_marr_age < 14 and wife_marr_age < 14:
        print(f"✘ Family ({family.id}): Husband ({husb_marr_age}) "
              f"and Wife ({wife_marr_age}) can not be less than 14")
    elif husb_marr_age < 14:
        print(f"✘ Family ({family.id}): Husband ({husb_marr_age}) can not be less than 14")
    elif wife_marr_age < 14:
        print(f"✘ Family ({family.id}): Wife ({wife_marr_age}) can not be less than 14")

    return False


def fewer_than_15_siblings(family: Family) -> bool:
    if len(family.chil) < 15:
        print(f"✔ Family ({family.id}): Siblings are less than 15")
        return True
    else:
        print(f"✘ Family ({family.id}): Siblings are greater than 15")
        return False


def male_last_names(family: Family, individuals: List[Individual]):
    ids = [family.husb, family.wife]
    ids.extend(family.chil)
    males = [individual for individual in individuals if individual.sex == 'M' and individual.id in ids]
    names = [male.name.split('/')[1] for male in males]
    return len(set(names)) == 1

def marriage_before_death(family: Family, individuals: List[Individual]) -> bool:
    """ user story: verify that marrriage before death of either spouse """
    mrgDate = datetime.strptime(family.marr.get('date'), "%d %b %Y")

    husb = list(filter(lambda x: x.id==family.husb,individuals))[0]
    wife = list(filter(lambda x: x.id == family.wife,individuals))[0]

    husbandDeathDate = datetime.strptime(husb.deat.get('date'), "%d %b %Y") if husb.deat else None
    wifeDeathDate = datetime.strptime(wife.deat.get('date'), "%d %b %Y") if wife.deat else None

   
    if (husbandDeathDate and husbandDeathDate - mrgDate > timedelta(minutes=0)) or (wifeDeathDate and wifeDeathDate - mrgDate > timedelta(minutes=0)):
        print(f"✔ Family ({family.husb}) and ({family.wife}):Their marriage took place, before either of their death.")
        return True
    else: 
        print(f"✘ Husband ({family.husb}): Wife ({family.wife}) Marriage did not take place before either of their death.")
        return False

def divorce_before_death(family: Family, individuals: List[Individual]) -> bool:
    """ user story: verify that divorce before death of either spouse """
    divdate = datetime.strptime(family.div.get('date'), "%d %b %Y")

    husb = list(filter(lambda x: x.id==family.husb,individuals))[0]
    wife = list(filter(lambda x: x.id == family.wife,individuals))[0]

    husbandDeathDate = datetime.strptime(husb.deat.get('date'), "%d %b %Y") if husb.deat else None
    wifeDeathDate = datetime.strptime(wife.deat.get('date'), "%d %b %Y") if wife.deat else None

    
    if (husbandDeathDate and husbandDeathDate - divdate > timedelta(minutes=0)) or (wifeDeathDate and wifeDeathDate - divdate > timedelta(minutes=0)):
        print(f"✔ Family ({family.husb}) and ({family.wife}):Their divorce took place, before either of their death.")
        return True
    else: 
        print(f"✘ Husband ({family.husb}) and Wife ({family.wife}): Divorce did not take place before either of their death.")
        return False