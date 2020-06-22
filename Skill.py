import re


class Skill:
    """
    A class that represents a skill
    """
    def __init__(self, name):
        """
        Skill constructor
        :param name:  string with the name of the skill
        """
        self._name = name
        self._volunteers = []  # list of volunteers that have this skill
        self._campaigns = []  # list of campaigns that needs this skill

    def is_in(self, skills):
        """

        :param skills: a list of skills (we got it from the data base)
        :return: True if the skill is in the data base, else False
        """
        for skill in skills:
            if self == skill:
                return True

    def get_name(self):
        """
        :return: string with the name of the skill
        """
        return self._name

    def __eq__(self, other):
        """
        :param other: an Skill object
        :return: True if the name of the other skill is equal to self(skill), it doesn't matter if it's upper or lower case
        """
        if isinstance(other, Skill):
            other_name = other.get_name()
            other_name = other_name.lower()
            # other_name = re.match(r'[a-z]+(\s)+[a-z]+', other_name).group(0)
            other_name = re.match(r'[a-z]+', other_name).group(0)
            if self._name == other_name:  # TODO: replace with regex
                return True
        return False

    def add_volunteer(self, volunteer):
        """
        add volunteer that have this skill to the list of the volunteers
        :param volunteer: an Volunteer object
        """
        self._volunteers += [volunteer]

    def add_campaign(self, campaign):
        """
        add campaign that need this skill to the list of the campaigns
        :param campaign: an Campaign object
        """
        self._campaigns += [campaign]

    def match_volunteer_to_campaign(self):
        """
        :return: a list of volunteers that have this skill - that's mean they match to the campaign that need volunteers
         with this skill
        """
        return self._volunteers

    def match_campaign_to_volunteer(self):
        """
        :return: a list of campaigns that need this skill - that's mean they match to the volunteer that have this skill
        """
        return self._campaigns
