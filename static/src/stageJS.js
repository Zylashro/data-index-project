// const enemyForm = document.querySelector('#enemy-form');

// const nameField = document.querySelector('#search-name');
// const nameSubmit = document.querySelector('#search-name-submit');
// const nameClear = document.querySelector('#search-name-clear');
// const nameMessage = document.querySelector('#search-name-message');


const selectSubmit = document.getElementById('episode');
const clearFilter = document.getElementById('clear-filter-stage');

selectSubmit.onchange = (event) => {
    document.stageForm.submit();
};

clearFilter.onclick = (event) => {
    window.location.replace('http://127.0.0.1:5000/stage-list');
};


// nameSubmit.onclick = (event) => {
//     event.preventDefault();
//     nameMessage.classList.add("hidden");
//     if (nameField.nodeValue.length < 3) {
//         nameMessage.classList.remove("hidden");
//     } else {
//         enemyForm.
//     }
// };

// nameClear.onclick = (event) => {
//     event.preventDefault();
//     nameField.nodeValue = '';
// };


