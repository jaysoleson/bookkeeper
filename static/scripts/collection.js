// View Toggles
let gridDisplayBtn = document.getElementById("gridDisplayBtn")
let listDisplayBtn = document.getElementById("listDisplayBtn")

let listDisplays = document.getElementsByClassName("collectionTableList")
let gridDisplays = document.getElementsByClassName("collectionTableGrid")

let categorySortBtn = document.getElementById("categorySortBtn")
let alphSortBtn = document.getElementById("alphSortBtn")
let timeSortBtn = document.getElementById("timeSortBtn")

// TODO: add docstrings for all of these functions. its confusing as heeellll

sorted_by = "category"
if (categorySortBtn.disabled == true) {
    sorted_by = "category"
} else if (alphSortBtn.disabled == true) {
    sorted_by = "alphabetical"
} else if (timeSortBtn.disabled == true) {
    sorted_by = "time"
}
current_view = "list"
if (gridDisplayBtn.disabled == true) {
    current_view = "grid"
} else if (listDisplayBtn.disabled == true) {
    current_view = "list"
}
let sortedByTime = document.getElementsByClassName(`${current_view}-time`)
let sortedByAlphabetical = document.getElementsByClassName(`${current_view}-alphabetical`)
let sortedByCategory = document.getElementsByClassName(`${current_view}-category`)

function refreshVariables() {
    sortedByTime = document.getElementsByClassName(`${current_view}-time`)
    sortedByAlphabetical = document.getElementsByClassName(`${current_view}-alphabetical`)
    sortedByCategory = document.getElementsByClassName(`${current_view}-category`)
}
refreshVariables()

function gridBtnClicked() {
    // Function that runs when the view is switched to "grid"
    // runs helpers and sets the states of the "grid" and "list" buttons
    current_view = "grid"
    refreshVariables()
    switchViews()

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
    // Function that runs when the view is switched to "list"
    // runs helpers and sets the states of the "grid" and "list" buttons
    current_view = "list"
    refreshVariables()
    switchViews()

    listDisplayBtn.classList.add("greenBtn");
    if ("blueBtn" in listDisplayBtn.classList) {
        listDisplayBtn.classList.remove("blueBtn");
    }
    listDisplayBtn.disabled = true;
    gridDisplayBtn.disabled = false;

    gridDisplayBtn.classList.add("blueBtn");
    gridDisplayBtn.classList.remove("greenBtn");

}

function switchViews() {
    // resets the display and shows the right ones based on local variables
    hideGridDisplay()
    hideListDisplay()
    if (current_view == "list") {
        showListDisplay()
        if (sorted_by == "category") {
            for (let i = 0; i < sortedByTime.length; i++) {
                sortedByTime[i].hidden = true;
            }
            for (let i = 0; i < sortedByAlphabetical.length; i++) {
                sortedByAlphabetical[i].hidden = true;
            }
            for (let i = 0; i < sortedByCategory.length; i++) {
                sortedByCategory[i].hidden = false;
            }
        } else if (sorted_by == "alphabetical") {
            for (let i = 0; i < sortedByTime.length; i++) {
                sortedByTime[i].hidden = true;
            }
            for (let i = 0; i < sortedByAlphabetical.length; i++) {
                sortedByAlphabetical[i].hidden = false;
            }
            for (let i = 0; i < sortedByCategory.length; i++) {
                sortedByCategory[i].hidden = true;
            }
        } else if (sorted_by == "time") {
            for (let i = 0; i < sortedByTime.length; i++) {
                sortedByTime[i].hidden = false;
            }
            for (let i = 0; i < sortedByAlphabetical.length; i++) {
                sortedByAlphabetical[i].hidden = true;
            }
            for (let i = 0; i < sortedByCategory.length; i++) {
                sortedByCategory[i].hidden = true;
            }
        }
    } else {
        showGridDisplay()
        if (sorted_by == "category") {
            for (let i = 0; i < sortedByTime.length; i++) {
                sortedByTime[i].style.display = "none";
            }
            for (let i = 0; i < sortedByAlphabetical.length; i++) {
                sortedByAlphabetical[i].style.display = "none";
            }
            for (let i = 0; i < sortedByCategory.length; i++) {
                sortedByCategory[i].style.display = "flex";
            }
        } else if (sorted_by == "alphabetical") {
            for (let i = 0; i < sortedByTime.length; i++) {
                sortedByTime[i].style.display = "none";
            }
            for (let i = 0; i < sortedByAlphabetical.length; i++) {
                sortedByAlphabetical[i].style.display = "flex";
            }
            for (let i = 0; i < sortedByCategory.length; i++) {
                sortedByCategory[i].style.display = "none";
            }
        } else if (sorted_by == "time") {
            for (let i = 0; i < sortedByTime.length; i++) {
                sortedByTime[i].style.display = "flex";
            }
            for (let i = 0; i < sortedByAlphabetical.length; i++) {
                sortedByAlphabetical[i].style.display = "none";
            }
            for (let i = 0; i < sortedByCategory.length; i++) {
                sortedByCategory[i].style.display = "none";
            }
        }
    }
}
// ------------------------------

// View Toggles
// hiding/showing/resorting collection isnt done here, it's done in python
// this just controls styling

function categorySortBtnClicked() {
    sorted_by = "category"
    refreshVariables()
    switchViews()
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
    timeSortBtn.disabled = false;
    alphSortBtn.disabled = false;
    categorySortBtn.disabled = true;
}

function alphSortBtnClicked() {
    sorted_by = "alphabetical"
    refreshVariables()
    switchViews()
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
    timeSortBtn.disabled = false;
    alphSortBtn.disabled = true;
    categorySortBtn.disabled = false;

}
function timeSortBtnClicked() {
    sorted_by = "time"
    refreshVariables()
    switchViews()
    if (timeSortBtn.classList.contains("blueBtn")) {
        timeSortBtn.classList.remove("blueBtn")
        timeSortBtn.classList.add("greenBtn")
    }
    if (alphSortBtn.classList.contains("greenBtn")) {
        alphSortBtn.classList.remove("greenBtn")
        alphSortBtn.classList.add("blueBtn")
    }
    if (categorySortBtn.classList.contains("greenBtn")) {
        categorySortBtn.classList.remove("greenBtn")
        categorySortBtn.classList.add("blueBtn")
    }

    timeSortBtn.disabled = true;
    alphSortBtn.disabled = false;
    categorySortBtn.disabled = false;
}

function hideListDisplay() {
    for (let i = 0; i < listDisplays.length; i++) {
        listDisplays[i].hidden = true;
    }
}
function showListDisplay() {
    for (let i = 0; i < listDisplays.length; i++) {
        listDisplays[i].hidden = false;
    }
}
function hideGridDisplay() {
    for (let i = 0; i < gridDisplays.length; i++) {
        gridDisplays[i].style.display = "none";
    }
}
function showGridDisplay() {
    for (let i = 0; i < gridDisplays.length; i++) {
        gridDisplays[i].style.display = "flex";
    }
}
