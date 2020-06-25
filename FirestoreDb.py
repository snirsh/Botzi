import os
from google.cloud import firestore
from DataLoader import USER_TYPES


class FirebaseDb:
    def __init__(self):
        """
        """
        self._db = firestore.Client()
        self.organization_collection = self._db.collection(u'Organizations')
        self.volunteer_collection = self._db.collection(u'Volunteers')
        self.campaign_collection = self._db.collection(u'Campaigns')

    def add_organization(self, data):
        """
        add new organization to the database
        :param data:
        :return:
        """
        self.organization_uiqueness(data.get('mail'))
        response = self.organization_collection.add({
            u'name': data.get("name"),
            u'contact_name': data.get("contact_name"),
            u'contact_phone': data.get("phone"),
            u'mail': data.get("mail"),
            u'campaigns': []
            #u'website_address': ngos_data["website_address"],
        })

    def add_volunteer(self, volunteers_data):
        """
        add a volunteer to the database
        :param volunteers_data:
        :return:
        """
        self.volunteer_uiqueness(volunteers_data.get('mail'))
        response = self.volunteer_collection.add({
            u'fname': volunteers_data.get("name"),
            u'skills': volunteers_data.get("skills"),
            u'mail': volunteers_data.get("mail"),
            u'free_time': volunteers_data.get("free_time"),
            u'password': volunteers_data.get("password"),
            u'phone': volunteers_data.get('phone')
        })

    def add_campaign(self, campaign_data):
        """

        :param ngos_data:
        :return:
        """
        self.campaign_uiqueness(campaign_data.get('mail'))
        response = self.campaign_collection.add({
            # u'id': campaign_data["id"],
            u'name': campaign_data["name"],
            u'requirements': campaign_data["requirements"],
            u'start_date': campaign_data["start_date"],
            u'end_date': campaign_data["end_date"],

        })
        self.update_campaign(response[1].id, campaign_data)

    def organization_uiqueness(self, mail):
        """
        :param mail:
        :return:
        """
        docs = self.organization_collection.where(u'mail', u'==', f'{mail}').stream()
        for doc in docs:
            raise ValueError("Email already exists")

    def volunteer_uiqueness(self, mail):
        """

        :param volunteer_data:
        :return:
        """
        docs = self.volunteer_collection.where(u'mail', u'==', f'{mail}').stream()
        for doc in docs:
            raise ValueError("Email already exists")

    def campaign_uiqueness(self, mail):
        """

        :param volunteer_data:
        :return:
        """
        docs = self.campaign_collection.where(u'mail', u'==', f'{mail}').stream()
        for doc in docs:
            raise ValueError("Email already exists")

    def is_email_exist(self, mail, p_type):
        """
        check if the mail is existing in one of the db collections
        :param mail:
        :param p_type:
        :return:
        """
        if p_type == USER_TYPES[0]:
            return self.volunteer_uiqueness(mail)
        if p_type == USER_TYPES[1]:
            return self.add_campaign(mail)
        return self.organization_uiqueness(mail)

    def get_volunteers_matches(self, campaign_mail):
        camp_docs = self.campaign_collection.where(u'mail', u'==', f'{campaign_mail}').stream()
        requirements = []
        for doc in camp_docs:
            details = doc.to_dict()
            requirements.extend(details.get("requirements"))

        volunteers_docs = self.volunteer_collection.stream()
        matching_volunteers = []
        for doc in volunteers_docs:
            details = doc.to_dict()
            for skill in requirements:
                if skill in details.get("skills"):
                    matching_volunteers.append(doc.id)

        return matching_volunteers

    def get_campaigns_matches(self, volunteer_id):
        # volunteer_docs = self.volunteer_collection.where(u'mail', u'==', f'{volunteer_mail}').stream()
        volunteer_docs = self.volunteer_collection.where(u'userId', u'==', f'{volunteer_id}').stream()
        skills = []
        for doc in volunteer_docs:
            details = doc.to_dict()
            skills.extend(details.get("skills"))

        campaigns_docs = self.campaign_collection.stream()
        matching_campaigns = []
        for doc in campaigns_docs:
            details = doc.to_dict()
            for require in skills:
                if require in details.get("requirements"):
                    matching_campaigns.append(doc.id)
        return matching_campaigns

    def update_volunteer(self, id, dic_update):
        """

        :param id:
        :param dic_update:
        :return:
        """
        ref = self.volunteer_collection.document(id)
        ref.update(dic_update)

    def add_collection(self, p_type, properties):
        if p_type == USER_TYPES[0]:
            self.add_volunteer(properties)
        elif p_type == USER_TYPES[1]:
            self.add_campaign(properties)
        else:
            self.add_organization(properties)

    def update_ngos(self, id, dic_update):
        """

        :param id:
        :param dic_update:
        :return:
        """
        ref = self.organization_collection.document(id)
        ref.update(dic_update)

    def update_campaign(self, id, dic_update):
        """

        :param id:
        :param dic_update:
        :return:
        """
        ref = self.campaign_collection.document(id)
        ref.update(dic_update)

    def search_ngo(self, id):
        """

        :param id:
        :return:
        """
        self.search_collection(self.organization_collection, id)

    def search_volunteer(self, id):
        """

        :param id:
        :return:
        """
        self.search_collection(self.volunteer_collection, id)

    def search_campaign(self, id):
        """

        :param id:
        :return:
        """
        self.search_collection(self.campaign_collection, id)

    @staticmethod
    def search_collection(collection, id):
        docs = collection.stream()
        for doc in docs:
            if doc.id == id:
                print(doc.to_dict())


if __name__ == '__main__':
    db = FirebaseDb()
    v1 = {
        "name": "daniel",
        "mail": "something@gmail.com",
        "password": "123456",
        "phone": "054-2223331",
        "skills": ["skill1", "skill2"]
    }

    id = "UqmoV7XYPJO5A0aRDlja"
    refs = db.volunteer_collection
    print(f"volunteer ref: {refs.get(id)}")

    volname = refs.where(u'fname', u'==', 'danielle')
    print(f'{volname.get()}')

    volunteers = volname.stream()
    print(f"type of volunteers is {type(volunteers)}")
    print(f"the object looks like {volunteers}")

    try:
        db.volunteer_uiqueness("something23@gmail.com")
    except ValueError as err:
        print(err)

    for volunteer in volunteers:
        print(f'type of single volunteer is {type(volunteer)}')
        print(f'{volunteer.id} => {volunteer.to_dict()}')

    volunteers_result = db.get_campaigns_matches("osnat@gmail.com")
    print(volunteers_result)



