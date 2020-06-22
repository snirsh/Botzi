
class PriorityQueue(object):
    """
    A class that represents a precedence priority queue when the elements in the class are campaign type
    """
    def __init__(self):
        """
        PriorityQueue constructor
        """
        self.queue = []

   # def __str__(self):
   #     return ' '.join([str(i) for i in self.queue])

    def isEmpty(self):
        """
        :return: True if the queue is empty, else False
        """
        return len(self.queue) == 0

    def insert(self, campaign):
        """
         inserting an campaign element in the queue
        :param campaign: an Campaign object
        """
        self.queue.append(campaign)

    def get_max(self):
        """
        popping an campaign element based on Priority
        :return: the campaign element with the highest Priority
        """
        try:
            max = 0
            for i in range(len(self.queue)):
                if self.queue[i].get_priority() > self.queue[max].get_priority():
                    max = i
            item = self.queue[max]
            del self.queue[max]
            return item
        except IndexError:
            print()
            exit()


