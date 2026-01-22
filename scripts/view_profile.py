# pylint:disable=invalid-name
class ViewProfile():
    """
    Handles all activity on the profile screen.
    Includes processing form input from user edits and grabbing info for display.
    """
    def __init__(self):
        pass

    def formPOST(self, user, form, form_submission):
        """
        Handles all form processing for the profile screen. Defers to helper functions

        :param user: All user session information.
        :param form: The entire form.
        :param form_submission: The form item being processed.
        """
        
        # CATEGORIES
        if form_submission == "submitNewCategory":
            self.submitNewCategory(form, user)
        elif form_submission == "deleteCategoriesBtn":
            self.deleteCategories(form, user)
        elif form_submission == "changeColourBtn":
            self.changeCategoryInfo(form, user)

        # TAGS
        elif form_submission == "submitNewTag":
            self.submitNewTag(form, user)
        elif form_submission == "deleteTagsBtn":
            self.deleteTags(form, user)
        
        # PROFILE INFO-- BIO
        elif form_submission == "saveBioBtn":
            self.editBio(form, user)

    # ------------------------------------------------------------------ #
    #                          FORM HELPERS                              #
    # ------------------------------------------------------------------ #

    # These helpers do not have access to the SESSION, just the USER, so they update it directly.
    def submitNewCategory(self, form, user):
        """
        Submits a new category!
        """
        new_category = form['submitNewCategory']
        new_category_colour = form['submitNewCategoryColour']
        if (new_category in user.categories) or (not new_category):
            print("Category name already in use!")
        else:
            user.categories.update({new_category:new_category_colour})
    
    def submitNewTag(self, form, user):
        """
        Submits a new tag!
        """
        new_tag = form["submitNewTag"]
        if "," in form["submitNewTag"]:
            new_tags = form["submitNewTag"].split(",")
        else:
            new_tags = [new_tag]
        for tag in new_tags:
            tag=tag.lstrip()
            if tag in user.tags:
                print("Tag name already in use!")
            else:
                user.tags.append(tag)
    
    def deleteTags(self, form, user):
        """
        Deletes tags checked by the user.
        """
        tags_to_delete = []
        for checkbox in form:
            if checkbox in user.tags:
                tags_to_delete.append(checkbox)
                print("deleting", checkbox)
        for tag in tags_to_delete:
            user.tags.remove(tag)

            for entry in user.collection:
                if tag in entry['tags']:
                    entry['tags'].remove(tag)

    def deleteCategories(self, form, user):
        """
        Handles deleting user categories, including failsafe for Unsorted.
        """
        categories_to_delete = []
        for checkbox in form:
            if checkbox in user.categories.keys():
                categories_to_delete.append(checkbox)
        for category in categories_to_delete:
            user.categories.pop(category)

            for entry in user.collection:
                if entry['category'] == category:
                    entry['category'] = "Unsorted"

    def editBio(self, form, user):
        """
        Updates the user's bio.
        """
        new_bio = form['editBio']
        user.profile_info['bio'] = new_bio
    
    def changeCategoryInfo(self, form, user):
        """
        Edits category information. Right now, it's just the colour that can be updated.
        """
        # TODO: Make names editable.
        for category in user.categories:
            if f"editCategoryColour-{category}" in form:
                user.categories[category] = form[f"editCategoryColour-{category}"]

    # ------------------------------------------------------------------ #
    #                         OTHER HELPERS                              #
    # ------------------------------------------------------------------ #

    def getProfileSubtitle(self, user):
        """
        Gets the user's profile subtitle.
        x Entries | x Categories
        """
        category_count = len([i for i in user.categories.keys()])
        entry_count = len(user.collection)

        if category_count > 0:
            category_count -= 1
        
        if entry_count == 1:
            entry_subtitle = f"{entry_count} Entry "
        else:
            entry_subtitle = f"{entry_count} Entries "

        if category_count == 1:
            category_subtitle = f"| {category_count} Category"
        else:
            category_subtitle = f"| {category_count} Categories"

        profile_subtitle = entry_subtitle + category_subtitle
        return profile_subtitle

# Class instance for import
profile = ViewProfile()
