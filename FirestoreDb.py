import os
from google.cloud import firestore
from DataLoader import USER_TYPES
#import self as self


class FirebaseDb:
    def __init__(self):
        """
        """
        db = firestore.Client()
        self.ngos_collection = db.collection(u'Ngos')
        self.volunteer_collection = db.collection(u'Volunteers')
        self.campaign_collection = db.collection(u'Campaigns')

    def add_ngo(self, ngos_data):
        """

        :param ngos_data:
        :return:
        """
        self.ngo_uiqueness_test(ngos_data)
        response = self.ngos_collection.add({
            u'contact_name': ngos_data["contact_name"],
            #u'ngo_number': ngos_data["ngo_number"],
            u'mail': ngos_data["mail"],
            #u'website_address': ngos_data["website_address"],
        })
        self.update_ngos(response[1].id, ngos_data)

    def add_volunteer(self, volunteers_data):
        """

        :param volunteers_data:
        :return:
        """
        self.volunteer_uiqueness_test(volunteers_data)
        response = self.volunteer_collection.add({
            u'name': volunteers_data["name"],
            u'skills': volunteers_data["skills"],
            u'mail': volunteers_data["mail"],
            u'free_time': volunteers_data["free_time"],
        })
        self.update_volunteer(response[1].id, volunteers_data)

    def add_campaign(self, campaign_data):
        """

        :param ngos_data:
        :return:
        """
        self.campaign_uiqueness_test(campaign_data)
        response = self.campaign_collection.add({
            u'id': campaign_data["id"],
            u'name': campaign_data["name"],
            u'start_date': campaign_data["start_date"],
            u'end_date': campaign_data["end_date"],

        })
        self.update_campaign(response[1].id, campaign_data)

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
            self.add_ngo(properties)

    def update_ngos(self, id,dic_update):
        """

        :param id:
        :param dic_update:
        :return:
        """
        ref = self.ngos_collection.document(id)
        ref.update(dic_update)

    def update_campaign(self, id,dic_update):
        """

        :param id:
        :param dic_update:
        :return:
        """
        ref = self.campaign_collection.document(id)
        ref.update(dic_update)


    def ngo_uiqueness_test(self, ngos_data):
        """

        :param ngos_data:
        :return:
        """
        docs = self.ngos_collection.stream()
        for doc in docs:
            #if ngos_data['ngo_number'] == doc.to_dict()['ngo_number']:
             #   raise Exception("association number is already exists")
            if ngos_data['mail'] == doc.to_dict()['mail']:
                raise Exception("mail address is already exists")
            #elif ngos_data['website_address'] == doc.to_dict()['website_address']:
             #   raise Exception("website address is already exists")


    def volunteer_uiqueness_test(self, volunteer_data):
        """

        :param volunteer_data:
        :return:
        """
        docs = self.volunteer_collection.stream()
        for doc in docs:
            if volunteer_data['mail'] == doc.to_dict()['mail']:
                raise Exception("mail address is already exists")


    def campaign_uiqueness_test(self, campaign_data):
        """

        :param volunteer_data:
        :return:
        """
        docs = self.campaign_collection.stream()
        for doc in docs:
            if campaign_data['id'] == doc.to_dict()['id']:
                raise Exception("id is already exists")


    def search_ngo(self, id):
        """

        :param id:
        :return:
        """
        self.search_collection(self.ngos_collection, id)


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


    def search_collection(self, collection, id):
        docs = collection.stream()
        for doc in docs:
            if doc.id == id:
                print(doc.to_dict())
