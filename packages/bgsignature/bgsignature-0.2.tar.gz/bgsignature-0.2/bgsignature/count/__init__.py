"""
This modules are in a separate package
to make it even more clear that their
interfaces should be the same
"""


class SignatureCounter(dict):

    def __add__(self, other):
        counter = self.__class__()  # just to return the same type of object
        for k in set(self.keys()).union(set(other.keys())):
            counter[k] = self[k] + other[k]
        return counter

    def __truediv__(self, other):
        counter = self.__class__()
        for k in self.keys():  # only on left values
            counter[k] = self[k] / other[k]
        return counter

    def to_dict(self):
        return dict(self)

    def collapse(self):
        raise NotImplementedError

    def sum1(self):
        total = sum([v for v in self.values()])
        return {k: v / total for k, v in self.items()}

    def normalize(self, other):
        div = self / other
        return div.sum1()


class GroupSignatureCounter(SignatureCounter):

    def __add__(self, other):
        group_counter = self.__class__()  # just to return the same type of object
        for group in set(self.keys()).union(set(other.keys())):
            group_counter[group] = self[group] + other[group]
        return group_counter

    def __truediv__(self, other):
        group_counter = self.__class__()  # just to return the same type of object
        for group in self.keys():
            group_counter[group] = self[group] / other  # do not expect group in the other
        return group_counter

    def to_dict(self):
        return {group: counter.to_dict() for group, counter in self.items()}

    def collapse(self):
        collapsed = self.__class__()
        for group, counter in self.items():
            collapsed[group] = counter.collapse()
        return collapsed

    def sum1(self):
        summed = {}
        for group, counter in self.items():
            summed[group] = counter.sum1()
        return summed

    def normalize(self, other):
        normalized = {}
        for group, counter in self.items():
            normalized[group] = counter.normalize(other)
        return normalized
