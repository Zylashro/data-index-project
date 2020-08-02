const openDropdown = document.getElementById('open-dropdown');
const dropdownMenu = document.getElementById('dropdown-menu');

openDropdown.onclick = (event) => {
    dropdownMenu.classList.remove("hidden");
}
