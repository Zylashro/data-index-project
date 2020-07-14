
const filterButton = document.getElementsByClassName("filter-by__btn");
const filterContainer = document.getElementsByClassName("filter-by__container");
const closeFilter = document.getElementsByClassName("close-btn");

filterButton.onclick = () => {
    filterContainer.classList.remove("hidden");
};

closeFilter.onclick = () => {
    filterContainer.classList.add("hidden");
};
