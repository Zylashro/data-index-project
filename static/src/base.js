const openDropdown = document.getElementById('open-dropdown');
const dropdownMenu = document.getElementById('dropdown-menu');
const body = document.body;
const back = document.getElementById('back');

openDropdown.onclick = (event) => {
    dropdownMenu.classList.toggle('hidden-mobile');
};

body.onclick = (event) => {
    if (event.target.id !== 'open-dropdown') {
        dropdownMenu.classList.add('hidden-mobile');
    }
};

if (back) {
    back.onclick = (event) => {
        history.back();
    }
}
