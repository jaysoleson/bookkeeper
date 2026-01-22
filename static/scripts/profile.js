// PROFILE EDIT
// functionality is done in python. this is just editing visibility
let editProfileBtn = document.getElementById("editProfileBtn")
let regProfileBtn = document.getElementById("regProfileBtn")

let editBioForm = document.getElementById("editBioForm")
let currentBio = document.getElementById("currentBio")
let categoryXButtons = document.getElementsByClassName("deleteCategory")

let deleteCategoriesBtn = document.getElementById("deleteCategoriesBtn")
let changeColourBtn = document.getElementById("changeColourBtn")
let deleteTagsBtn = document.getElementById("deleteTagsBtn")

let addNewTagsForm = document.getElementById("addNewTagsForm")
let submitNewCategoryForm = document.getElementById("submitNewCategoryForm")

let nocategories = document.getElementById("nocategories")
let notags = document.getElementById("notags")

function switchToEditMode() {
    regProfileBtn.hidden = false;
    editProfileBtn.hidden = true;
    if (deleteCategoriesBtn) {
        deleteCategoriesBtn.hidden = false;
    }
    if (changeColourBtn) {
        changeColourBtn.hidden = false;
    }
    if (deleteTagsBtn) {
        deleteTagsBtn.hidden = false;
    }
    if (addNewTagsForm) {
        addNewTagsForm.hidden = false;
    }

    if (nocategories) {
        nocategories.hidden = true;
    }
    if (notags) {
        notags.hidden = true;
    }

    editBioForm.hidden = false;
    currentBio.hidden = true;
    submitNewCategoryForm.hidden = false;

    for (let i = 0; i < categoryXButtons.length; i++) {
        categoryXButtons[i].hidden = false;
    }
}

function leaveEditMode() {
    regProfileBtn.hidden = true;
    editProfileBtn.hidden = false;
    if (deleteCategoriesBtn) {
        deleteCategoriesBtn.hidden = true;
    }
    if (changeColourBtn) {
        changeColourBtn.hidden = true;
    }
    if (deleteTagsBtn) {
        deleteTagsBtn.hidden = true;
    }
    if (addNewTagsForm) {
        addNewTagsForm.hidden = true;
    }

    if (nocategories) {
        nocategories.hidden = false;
    }
    if (notags) {
        notags.hidden = false;
    }

    editBioForm.hidden = true;
    currentBio.hidden = false;
    submitNewCategoryForm.hidden = true;

    for (let i = 0; i < categoryXButtons.length; i++) {
        categoryXButtons[i].hidden = true;
    }

    refreshPage()
}

function showTextWidgetOptions() {
    document.getElementById("newWidgetContent").hidden = false;

    document.getElementById("newWidgetURL").hidden = true;
    document.getElementById("newWidgetAlt").hidden = true;
}

function showImageWidgetOptions() {
    document.getElementById("newWidgetContent").hidden = true;

    document.getElementById("newWidgetURL").hidden = false;
    document.getElementById("newWidgetAlt").hidden = false;
}

// NEW WIDGETS

function addNewWidget() {
    document.getElementById("newWidgetDiv").hidden = false;
    document.getElementById("addWidgetButton").hidden = true;
    document.getElementById("cancelNewWidgetButton").hidden = false;
}

function cancelNewWidget() {
    document.getElementById("newWidgetDiv").hidden = true;
    document.getElementById("addWidgetButton").hidden = false;
    document.getElementById("cancelNewWidgetButton").hidden = true;
}

function selectEditCategory(selectedCategory) {
    if (!document.getElementById(`checkbox-${selectedCategory}`).checked) {
        document.getElementById(selectedCategory).classList.remove("selectedCategory")
    } else {
        document.getElementById(selectedCategory).classList.add("selectedCategory")
    }
}