
const filterButton = document.getElementsByClassName("filter-by__btn");
const filterContainer = document.getElementsByClassName("filter-by__container");

filterButton.addEventListener("click", hideAndShow);

function hideAndShow(event) {
    filterContainer.classList.replace("hidden", "")
}
