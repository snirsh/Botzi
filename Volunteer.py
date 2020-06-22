#from Skill import Skill
from Data import Data

data = Data()


class Volunteer:
    """
    A class that represents a volunteer
    """
    def __init__(self, name, unique_id, skills):
        """
        Volunteer constructor
        :param name: of  Volunteer
        :param unique_id: of Volunteer
        :param skills: list of skills that the volunteer has
        """
        self._name = name
        self._unique_id = unique_id
        self._catch = False  # says if the volunteer is catch or not
        self._skills = []  # list of skills that the volunteer has and their are in the data base
        # A loop that ran on all the skills the volunteer have and if the skill exist in Data Base
        # she adds him to the volunteer's list of skills
        for skill in skills:
            if data.is_skill_in_data(skill):
                skill_object = data.get_skill_from_data(skill)
                if skill_object:
                    skill_object.add_volunteer(self)
                    self._skills += [skill_object]

    def is_catch(self):
        """
        :return: True if the volunteer is catch or not, else False
        """
        return self._catch

    def make_available(self):
        """
        make the  status of the volunteer to available for volunteering
        """
        self._catch = True

    def make_catch(self):
        """
        make the  status of the volunteer to not available for volunteering
        """
        self._catch = True

    def get_name(self):
        """
        :return: the name of the volunteer
        """
        return self._name

    def find_campaigns(self):
        """
            :return: a list with campaigns that need my skills
        """
        campaigns = []
        for skill in self._skills:
            campaigns += skill.match_campaign_to_volunteer()
        return campaigns
