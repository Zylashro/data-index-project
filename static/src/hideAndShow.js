
const filterButton = document.getElementsByClassName("filter-by__btn");
const filterContainer = document.getElementsByClassName("filter-by__container");

filterButton.onclick = () => {
    filterContainer.classList.replace("hidden", "");
};
