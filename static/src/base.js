const openDropdown = document.getElementById('open-dropdown');
const dropdownMenu = document.getElementById('dropdown-menu');
const body = document.body;
const back = document.getElementById('back');
const topButton = document.getElementById("backToTop");
const buttonChevron = document.getElementById("back-to-top-chevron")

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

// Back to top button

topButton.onclick = (event) => {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        topButton.style.display = "block";
        buttonChevron.style.display = "block";
    } else {
        topButton.style.display = "none";
        buttonChevron.style.display = "none";
    }
}

window.onscroll = function() {scrollFunction()};
