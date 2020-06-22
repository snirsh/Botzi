import re

from Skill import Skill
skill1 = Skill('python')
skill2 = Skill('c')
skill3 = Skill('c++')

skills = [skill1, skill2, skill3]


class Data:
    """
    A class that represents the data that we have in the data base
    """
    def get_skills_data(self):
        """
        :return: a list with the skills that in the data
        """
        return skills

    def get_skill_from_data(self, skill_name):
        """
        get Skill object from data
        :param skill_name: string -  name of skill, could be in uppercase ore even some letters in the string
        :return: the object of the skill with the name skill_name in the data - object from Skill type
        """
        skill_name = skill_name.lower()
        skill_name = re.match(r'[a-z]+', skill_name).group(0)
        for skill in self.get_skills_data():
            if skill.get_name() == skill_name:
                return skill
        return None

    def is_skill_in_data(self, skill_name):
        """
        search if we have skill_name un the skills that in the data
        :param skill_name: string -  name of skill, could be in uppercase ore even some letters in the string
        :return: True if the skill is in the data, False - else
        """
        other_skill = Skill(skill_name)
        for skill in self.get_skills_data():
            if skill == other_skill:
                return True
