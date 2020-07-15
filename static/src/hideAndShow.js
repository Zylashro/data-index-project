
const openFilter = document.getElementById('open-filter-btn');
const filterContainer = document.getElementById('filter-menu');
const closeFilter = document.getElementById('close-filter-btn');

openFilter.onclick = () => {
    filterContainer.classList.remove("hidden");
};

closeFilter.onclick = () => {
    filterContainer.classList.add("hidden");
};
