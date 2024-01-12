var btnOpWhlLib = document.getElementById('openWholeLibrary');
var btnClWhlLib = document.getElementById('closeWholeLibrary');
var btnSaveLib = document.getElementById('saveAddToLibrary');
var whlLib = document.getElementById('wholeLibrary');
var whlLibText = document.getElementById('wholeLibraryTextarea');

btnOpWhlLib.addEventListener('click', function(event) {
    btnOpWhlLib.style.display = 'none';
    btnClWhlLib.style.display = 'block';
    btnSaveLib.style.display = 'block';
    whlLib.style.animation = 'stretching 0.5s forwards';
    whlLibText.style.display = 'block';
    event.stopPropagation();
});

btnClWhlLib.addEventListener('click', function(event) {
    btnOpWhlLib.style.display = 'block';
    btnClWhlLib.style.display = 'none';
    btnSaveLib.style.display = 'none';
    whlLib.style.animation = 'compression 0.5s forwards';
    whlLibText.style.display = 'none';
    event.stopPropagation();
});

var btnOpMyLib = document.getElementById('openMyLibrary');
var btnClMyLib = document.getElementById('closeMyLibrary');
var btnDeleteLib = document.getElementById('saveDeleteFromLibrary');
var myLib = document.getElementById('myLibrary');
var myLibText = document.getElementById('myLibraryTextarea');

btnOpMyLib.addEventListener('click', function(event) {
    btnOpMyLib.style.display = 'none';
    btnClMyLib.style.display = 'block';
    btnDeleteLib.style.display = 'block';
    myLib.style.animation = 'stretching 0.5s forwards';
    myLibText.style.display = 'block';
    event.stopPropagation();
});

btnClMyLib.addEventListener('click', function(event) {
    btnOpMyLib.style.display = 'block';
    btnClMyLib.style.display = 'none';
    btnDeleteLib.style.display = 'none';
    myLib.style.animation = 'compression 0.5s forwards';
    myLibText.style.display = 'none';
    event.stopPropagation();
});

var btnOpRecLib = document.getElementById('openRecomendationLibrary');
var btnClRecLib = document.getElementById('closeRecomendationLibrary');
var btnFindRec = document.getElementById('findOutTheRecomendations');
var recLib = document.getElementById('recomendationLibrary');
var recLibText = document.getElementById('recLibraryTextarea');

btnOpRecLib.addEventListener('click', function(event) {
    btnOpRecLib.style.display = 'none';
    btnClRecLib.style.display = 'block';
    btnFindRec.style.display = 'block';
    recLib.style.animation = 'stretching 0.5s forwards';
    recLibText.style.display = 'block';
    event.stopPropagation();
});

btnClRecLib.addEventListener('click', function(event) {
    btnOpRecLib.style.display = 'block';
    btnClRecLib.style.display = 'none';
    btnFindRec.style.display = 'none';
    recLib.style.animation = 'compression 0.5s forwards';
    recLibText.style.display = 'none';
    event.stopPropagation();
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sendAddToLibraryRequest(musicId) {
    fetch('/add-to-library/', { // URL, по которому Django обрабатывает POST-запросы для добавления записи
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // CSRF токен, чтобы Django принял POST-запрос
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ 'music_id': musicId })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data); // обработка данных полученных от сервера
    })
    .catch(e => {
        console.log('Error:', e);
    });
}

function sendDeleteFromLibraryRequest(musicId) {
    fetch('/del-from-library/', { // URL, по которому Django обрабатывает POST-запросы для добавления записи
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // CSRF токен, чтобы Django принял POST-запрос
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ 'music_id': musicId })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data); // обработка данных полученных от сервера
    })
    .catch(e => {
        console.log('Error:', e);
    });
}

function sendFindOutRecomendations() {
    fetch('/find-out-rec/', { // URL, по которому Django обрабатывает POST-запросы для добавления записи
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // CSRF токен, чтобы Django принял POST-запрос
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({'message': 'message_body'})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data); // обработка данных полученных от сервера
        if (data.message) {
            const formattedMessage = `${data.message}<br />`;
            recLibText.innerHTML += formattedMessage;
        } else {
            console.log('Ответ не содержит message!');
        }
    })
    .catch(e => {
        console.log('Error:', e);
    });
}

// делегирование событий (идёт прослушка на клик на всём документе, и только потом проверка на принадлежность
// к классу dop-button/del-button/find-rec)
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('dop-button')) {
        const musicId = event.target.getAttribute('data-id');
        sendAddToLibraryRequest(musicId);
        event.target.style.display = 'none';
    }
    if (event.target.classList.contains('del-button')) {
        const musicId = event.target.getAttribute('data-id');
        sendDeleteFromLibraryRequest(musicId);
        event.target.style.display = 'none';
    }
    if (event.target.classList.contains('find-rec')) {
        alert("Обработка персональной музыкальной коллекции...");
        sendFindOutRecomendations();
    }
});