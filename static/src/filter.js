
const openFilter = document.getElementById('open-filter-btn');
const filterContainer = document.getElementById('filter-menu');
const closeFilter = document.getElementById('close-filter-btn');
const clearFilter = document.getElementById('clear-filter');

openFilter.onclick = (event) => {
    event.preventDefault();
    filterContainer.classList.remove("hidden");
};

closeFilter.onclick = (event) => {
    event.preventDefault();
    filterContainer.classList.add("hidden");
};

clearFilter.onclick = (event) => {
    window.location.replace('http://127.0.0.1:5000/enemy-list');
};