# pylint:disable=invalid-name
class ViewEntry():
    def __init__(self):
        pass

    def getCurrentEntry(self, user, entry_id):
        """
        Gets the current entry from the supplied ID
        """
        current_entry = None
        for item in user.collection:
            if item['id'] == entry_id:
                current_entry = item
                break
        return current_entry
    
    def nextIndex(self, current_index, collection):
        """
        Gets the index of the previous entry. Loops back around if you're at the end.
        """
        if current_index + 1 > len(collection) - 1:
            next_index = 0
        else:
            next_index = current_index + 1
        return next_index
    
    def prevIndex(self, current_index, collection):
        """
        Gets the index of the previous entry. Loops back around if you're at the start.
        """
        if current_index - 1 < 0:
            prev_index = len(collection) - 1
        else:
            prev_index = current_index - 1
        return prev_index

view_entry = ViewEntry()
