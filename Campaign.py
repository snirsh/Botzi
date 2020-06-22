from Data import Data
from Skill import Skill

data = Data()


class Campaign:
    """
     A class that represents a campaign
    """
    def __init__(self, name, unique_id, skills_amount):
        """
      Campaign constructor
      :param name: the name of the campaign
      :param unique_id: the id of the campaign
      :param skills_amount: list with tuples: (skill, the amount of volunteers they need from the skill)
      """
        self._name = name
        self._unique_id = unique_id
        self._volunteers = []
        self._skills = []
        # dictionary of skills and the amount of the people with the skill that the campaign need
        self._skills_amounts = {}
        # A loop that ran on all the skills the association needs (skills_amount) and if the skills exist in Data Base
        # she adds them to the association's list of skills along with the amount of people needed for talent
        for skill in skills_amount:
            skill_name = skill[0]
            skill_amount = skill[1]
            if data.is_skill_in_data(skill_name):
                skill_object = data.get_skill_from_data(skill_name)
                # if skill_object:
                skill_object.add_campaign(self)
                self._skills += [(skill_object, skill_amount)]
                self._skills_amounts[skill_name] = skill_amount

    def get_name(self):
        """
        :return: the name of the campaign
        """
        return self._name

    def amount_of_skill(self, skill):
        """
        :param skill:
        :return: the amount of the people with the skill 'skill' that the campaign need
        """
        return self._skills_amounts[skill]

    def get_priority(self):
        """
        the priority of the campaign
        :return: the priority: How many volunteers the campaign could has versus how much it needs
        """
        sum_volunteers_we_need = 0
        sum_volunteers_we_have = 0
        for skill in self._skills:
            skill_object = skill[0]
            skill_amount = skill[1]
            sum_volunteers_we_need += skill_amount
            sum_volunteers_we_have += len(skill_object.match_volunteer_to_campaign())
        return sum_volunteers_we_have / sum_volunteers_we_need

    def find_volunteers(self):
        """
        :return: a list of tuples (skill, volunteers that have the 'skill' that the campaign need their)
        """
        volunteers = []
        for skill in self._skills:
            skill_object = skill[0]
            volunteers += [(skill_object, skill_object.match_volunteer_to_campaign())]
        return volunteers

    def set_volunteers(self, founded_volunteers):
        """
        set the volunteer for this campaign to the appropriate skill
        :param founded_volunteers: volunteers that we found are match to this campaign
        """
        volunteers_set = []
        for skill in founded_volunteers:
            skill_volunteers = []
            volunteers = skill[1]
            skill_object = skill[0]
            for volunteer in volunteers:
                if not volunteer.is_catch():
                    if self.amount_of_skill(skill_object.get_name()) > len(skill_volunteers):
                        skill_volunteers += [volunteer]
                        volunteer.make_catch()
            if len(skill_volunteers) > 0:
                volunteers_set += [(skill_object, skill_volunteers)]
        self._volunteers = volunteers_set

    def get_volunteers(self):
        """
        :return: a list of tuples (skill, volunteers with the skill like the skills amount that the campaign need for
        this skill)
        """
        return self._volunteers

    def print_volunteers(self):
        """
        Prints the volunteers who have been deployed to the campaign according to each skill
        """
        print('match volunteer for ' + self._name + ' campaign:')
        for skill in self._volunteers:
            skill_obj = skill[0]
            skill_volunteers = skill[1]
            volunteers_names = []
            for vol in skill_volunteers:
                volunteers_names += [vol.get_name()]
            print('   for skill ' + skill_obj.get_name() + ' the volunteers names are: ' + str(volunteers_names))

    def print_find_volunteers(self):
        """
         Prints the volunteers who could be deployed to the campaign according to each skill
        """
        founded_volunteers = self.find_volunteers()
        print('match volunteer for ' + self._name + ' campaign:')
        for skill in founded_volunteers:
            skill_obj = skill[0]
            skill_volunteers = skill[1]
            volunteers_names = []
            for vol in skill_volunteers:
                volunteers_names += [vol.get_name()]
            print('   for skill ' + skill_obj.get_name() + ' the volunteers names are: ' + str(volunteers_names))
