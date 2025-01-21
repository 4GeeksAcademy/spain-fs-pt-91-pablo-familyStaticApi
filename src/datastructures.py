"""
Update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint


class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        # example list of members
        self._members = [{'id': 100, 'name': 'John', 'last_name': self.last_name, 'age': 33, 'lucky_numbers': [7, 13, 22]},
                         {'id': self._generate_id(), 'name': 'Jane', 'age': 35, 'last_name': self.last_name, 'lucky_numbers': [10, 14, 3]},
                         {'id': self._generate_id(), 'name': 'Jimmy', 'age': 5, 'last_name': self.last_name, 'lucky_numbers': [1]}]

    # Read-only: Use this method to generate random members ID's when adding members into the list
    def _generate_id(self):
        return randint(0, 99999999)

    def add_member(self, member):
        member['id'] = self._generate_id()
        member['last_name'] = self.last_name
        self._members.append(member)
        return member
    
    def update_member(self, member, id):
        member_to_update = self.get_member(id)[0]
        member_to_update['name'] = member['name']
        member_to_update['age'] = member['age']
        member_to_update['lucky_numbers'] = member['lucky_numbers']

    def delete_member(self, id):
        member_to_remove = self.get_member(id)[0]
        self._members.remove(member_to_remove)

    def get_member(self, id):
        return [row for row in self._members if row['id'] == id]

    # This method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members
