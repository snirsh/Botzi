import unittest

from Campaign import Campaign
from Skill import *
from Data import Data
from Volunteer import Volunteer


class SkillTest(unittest.TestCase):
    def test_is_in(self):
        """
        Test fot that we got the appropriate answer if the skill is in the data base or not
        """
        data = Data()
        skills_data = data.get_skills_data()

        skill1 = Skill('Python')
        skill2 = Skill('Python+')
        skill3 = Skill('python')
        skill4 = Skill('python+')
        skill5 = Skill('dance')

        result1 = skill1.is_in(skills_data)
        result2 = skill2.is_in(skills_data)
        result3 = skill3.is_in(skills_data)
        result4 = skill4.is_in(skills_data)
        result5 = skill5.is_in(skills_data)

        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertTrue(result3)
        self.assertTrue(result4)
        self.assertFalse(result5)

    def test__eq__(self):
        """
        Test if two skills object are equals: one could be with uppercase iand the other not
        """
        skill1 = Skill('Python')
        skill2 = Skill('Python+')
        skill3 = Skill('python')
        skill4 = Skill('dance')

        result1 = (skill1 == skill2)
        result2 = (skill1 == skill3)
        result3 = (skill1 == skill4)

        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertFalse(result3)

    def test_add_volunteer(self):
        skill = Skill('python')
        vol1 = Volunteer('osnat', '122', ['Python', 'C', 'C++'])
        vol2 = Volunteer('daniel', '133', ['Python', 'C', 'C++'])
        vol3 = Volunteer('someone', '155', [])

        volunteers = [vol1, vol2, vol3]

        skill.add_volunteer(vol1)
        skill.add_volunteer(vol2)
        skill.add_volunteer(vol3)

        flag = False
        i = 0
        for vol in skill.match_volunteer_to_campaign():
            flag = vol == volunteers[i]
            i += 1

        self.assertTrue(flag)

    def test_add_campaign(self):
        skill = Skill('python')
        camp1 = Campaign('ezer mitzion', 1234, [('python', 1), ('c', 1), ('c++', 1)])
        camp2 = Campaign('shalva', 3456, [('python', 5), ('c', 6), ('c++', 7)])
        camp3 = Campaign('jerusalem', 6789, [])

        campaigns = [camp1, camp2, camp3]

        skill.add_campaign(camp1)
        skill.add_campaign(camp2)
        skill.add_campaign(camp3)

        flag = False
        i = 0
        for camp in skill.match_campaign_to_volunteer():
            flag = camp == campaigns[i]
            i += 1
        self.assertTrue(flag)


if __name__ == '__main__':
    unittest.main()
