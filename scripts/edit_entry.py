# pylint:disable=invalid-name
class EditEntry():
    """
    Class responsible for all edit entry actions.
    Currently just handles form submission for adding, editing, and deleting.
    """
    def __init__(self):
        pass

    def formPOST(self, form_submission, form, current_entry):
        """
        Handles all form submissions that come from editing an entry.
        """
        print(form_submission)
        if form_submission in ("submitEntryTitle", "submitEntryCategory", "submitEntryIcon", "defaultImage"):
            self.editEntryCoreInfo(form, form_submission, current_entry)
        elif form_submission in ("new-widget-type"):
            self.addNewWidget(form, current_entry)
        elif "widgetEdit" in form_submission and form[form_submission]:
            self.editWidget(form, form_submission, current_entry)
        elif "deleteWidget" in form_submission:
            self.deleteWidget(form_submission, current_entry)

    def editEntryCoreInfo(self, form, form_submission, current_entry):
        """
        Edits CORE info: Title, category, icon.
        :param form: Entire form
        :param form_submission: The string of the current form submission (e.g. 'submitEntryTitle')
        :current_entry: The entry being viewed. Entire entry dict
        """

        edit_dict = {
            "submitEntryTitle": "name",
            "submitEntryCategory": "category",
            "submitEntryIcon": "icon_url",
            "defaultImage": "icon_url",
        }
        for form_value, entry_info in edit_dict.items():
            if form_submission == form_value:
                if entry_info == "icon_url":
                    if form['submitEntryIcon'] == "" or "static" in form['submitEntryIcon']:
                        # TODO: HACKYYYY
                        if form_value == "defaultImage":
                            current_entry[entry_info] = form[form_value]
                            print("CHANGING FROM DEFAULT IMG INPUT:", form[form_value])
                    else:
                        if form_value == "submitEntryIcon":
                            current_entry[entry_info] = form[form_value]
                            print("CHANGING FROM CUSTOM URL INPUT:", form[form_value])
    
    def addNewWidget(self, form, current_entry):
        """
        Adds a brand new widget.
        """
        widget_type = form['new-widget-type']
        widget_content = form['new-widget-text-content']
        widget_url = form['new-widget-url-content']
        widget_alt = form['new-widget-alt']
        widget_align = form['new-widget-align']

        new_content = widget_content if widget_content else widget_url
        if not new_content:
            return
        print("Adding widget:", new_content)

        current_entry['widgets'].append(
            {
            "type": widget_type,
            "content": new_content,
            "params": {
                "alt": widget_alt if widget_alt else None,
                "align": widget_align
                }
            }
        )
    
    def editWidget(self, form, form_submission, current_entry):
        """
        Edits the entry widget! Either content or alignment.
        """
        widget_index = int(form_submission.split("-")[1])
        try:
            editedWidget = current_entry['widgets'][widget_index]
        except IndexError as e:
            print("Edit Widget Error:", e)
            return
        if "widgetEditContent" in form_submission:
            if form[f"widgetEditContent-{widget_index}"]:
                editedWidget["content"] = form[f"widgetEditContent-{widget_index}"]
        elif "widgetEditAlign" in form_submission:
            if form[f"widgetEditAlign-{widget_index}"]:
                editedWidget["params"]["align"] = form[f"widgetEditAlign-{widget_index}"]
    
    def deleteWidget(self, form_submission, current_entry):
        """
        Deleting a widget.
        """
        widget_index = int(form_submission.split("-")[1])
        current_entry['widgets'].remove(current_entry['widgets'][widget_index])

edit_entry = EditEntry()
