const searchName = document.querySelector('[name="search"]');
const searchSubmit = document.getElementById('search-submit');
const openFilter = document.getElementById('open-filter-btn');
const closeFilter = document.getElementById('close-filter-btn');
const filterContainer = document.getElementById('filter-menu');
const resetFilter = document.getElementById('reset-filter');
const radioAttack = document.getElementsByName("attack-type");
const radioLevel = document.getElementsByName("level-type");
const enemyForm = document.querySelector('[name="enemyForm"]');
const warning = document.querySelector('#warning');
const overlay = document.querySelector('#overlay');

// Reset radio fields in filter menu.
function resetRadio(name) {
    let amount = name.length;
    for(i=0; i<amount; i++) {
        name[i].checked = false;
    }
};

// Open filter menu.
openFilter.onclick = (event) => {
    filterContainer.classList.remove("hidden");
    overlay.classList.remove("hidden");
};

// Close filter menu.
closeFilter.onclick = (event) => {
    filterContainer.classList.add("hidden");
    overlay.classList.add("hidden");
};

// Reset selected radio button.
resetFilter.onclick = (event) => {
    resetRadio(radioAttack);
    resetRadio(radioLevel);
};

// Submit the search form. If search has less than two characters, show warning.
searchSubmit.onclick = (event) => {
    event.preventDefault();
    warning.classList.add("hidden");
    if (searchName.value.length > 1) {
        document.enemyForm.submit();
    } else {
        warning.classList.remove("hidden");
    }
};

// Submit form to filter the index.
enemyForm.onsubmit = (event) => {
    event.preventDefault();
    warning.classList.add("hidden");
    if (searchName.value.length > 0 && searchName.value.length < 2) {
        warning.classList.remove("hidden");
    } else {
        document.enemyForm.submit();
    }
};

// Hide warning after user closes it.
warning.onclick = (event) => {
    warning.classList.add("hidden");
};
