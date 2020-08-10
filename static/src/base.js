const openDropdown = document.getElementById('open-dropdown');
const dropdownMenu = document.getElementById('dropdown-menu');
const body = document.body;
const back = document.getElementById('back');
const topButton = document.getElementById("backToTop");
const buttonChevron = document.getElementById("back-to-top-chevron")

// Open up dropdown menu on the mobile version
openDropdown.onclick = (event) => {
    dropdownMenu.classList.toggle('hidden-mobile');
};

// Close dropdown menu by clicking outside the menu list or the icon again
body.onclick = (event) => {
    if (event.target.id !== 'open-dropdown') {
        dropdownMenu.classList.add('hidden-mobile');
    }
};

// Go back to previous back in search history
if (back) {
    back.onclick = (event) => {
        history.back();
    }
}


// Click button to go back to the top of the page.
topButton.onclick = (event) => {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

// Scroll down in order for the back to top button to appear.
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
