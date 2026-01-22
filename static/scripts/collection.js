// View Toggles
let gridDisplayBtn = document.getElementById("gridDisplayBtn")
let listDisplayBtn = document.getElementById("listDisplayBtn")

let gridDisplay = document.getElementById("collectionTableGrid")
let listDisplay = document.getElementById("collectionTableList")

function gridBtnClicked() {
    listDisplay.hidden = true;
    gridDisplay.style.display = "flex";

    gridDisplayBtn.classList.add("greenBtn");
    if ("blueBtn" in gridDisplayBtn.classList) {
        gridDisplayBtn.classList.remove("blueBtn");
    }
    gridDisplayBtn.disabled = true;
    listDisplayBtn.disabled = false;

    listDisplayBtn.classList.add("blueBtn");
    listDisplayBtn.classList.remove("greenBtn");
    
}

function listBtnClicked() {
    listDisplay.hidden = false;
    gridDisplay.style.display = "none";

    listDisplayBtn.classList.add("greenBtn");
    if ("blueBtn" in listDisplayBtn.classList) {
        listDisplayBtn.classList.remove("blueBtn");
    }
    listDisplayBtn.disabled = true;
    gridDisplayBtn.disabled = false;

    gridDisplayBtn.classList.add("blueBtn");
    gridDisplayBtn.classList.remove("greenBtn");
}
// ------------------------------

function refreshPage() {
    window.location.reload();
}

// View Toggles

let categorySortBtn = document.getElementById("categorySortBtn")
let alphSortBtn = document.getElementById("alphSortBtn")
let timeSortBtn = document.getElementById("timeSortBtn")
// hiding/showing/resorting collection isnt done here, it's done in python
// this just controls styling

function categorySortBtnClicked() {
    console.log("CATEGORY BUTTON")
    categorySortBtn.classList.add("greenBtn")
    if (categorySortBtn.classList.contains("blueBtn")) {
        categorySortBtn.classList.remove("blueBtn")
    }
    if (timeSortBtn.classList.contains("greenBtn")) {
        timeSortBtn.classList.remove("greenBtn")
        timeSortBtn.classList.add("blueBtn")
    }
    if (alphSortBtn.classList.contains("greenBtn")) {
        alphSortBtn.classList.remove("greenBtn")
        alphSortBtn.classList.add("blueBtn")
    }
    refreshPage()
}
function alphSortBtnClicked() {
    console.log("ALPH BUTTON")
    alphSortBtn.classList.add("greenBtn")
    if (alphSortBtn.classList.contains("blueBtn")) {
        alphSortBtn.classList.remove("blueBtn")
    }
    if (timeSortBtn.classList.contains("greenBtn")) {
        timeSortBtn.classList.remove("greenBtn")
        timeSortBtn.classList.add("blueBtn")
    }
    if (categorySortBtn.classList.contains("greenBtn")) {
        categorySortBtn.classList.remove("greenBtn")
        categorySortBtn.classList.add("blueBtn")
    }
    refreshPage()
}
function timeSortBtnClicked() {
    console.log("TIME BUTTON")
    timeSortBtn.classList.add("greenBtn")
    if (timeSortBtn.classList.contains("blueBtn")) {
        timeSortBtn.classList.remove("blueBtn")
    }
    if (alphSortBtn.classList.contains("greenBtn")) {
        alphSortBtn.classList.remove("greenBtn")
        alphSortBtn.classList.add("blueBtn")
    }
    if (categorySortBtn.classList.contains("greenBtn")) {
        categorySortBtn.classList.remove("greenBtn")
        categorySortBtn.classList.add("blueBtn")
    }
    refreshPage()
}


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

    console.log(categoryXButtons)
    for (let i = 0; i < categoryXButtons.length ; i++) {
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
    console.log("SELECTED", selectedCategory)
    if (!document.getElementById(`checkbox-${selectedCategory}`).checked) {
        document.getElementById(selectedCategory).classList.remove("selectedCategory")
    } else {
        document.getElementById(selectedCategory).classList.add("selectedCategory")
    }
}