var btnOpWhlLib = document.getElementById('openWholeLibrary');
var btnClWhlLib = document.getElementById('closeWholeLibrary');
var whlLib = document.getElementById('wholeLibrary');
var whlLibText = document.getElementById('wholeLibraryTextarea');

btnOpWhlLib.addEventListener('click', function(event) {
    btnOpWhlLib.style.display = 'none';
    btnClWhlLib.style.display = 'block';
    whlLib.style.animation = 'stretching 0.5s forwards';
    whlLibText.style.display = 'block';
    event.stopPropagation();
});

btnClWhlLib.addEventListener('click', function(event) {
    btnOpWhlLib.style.display = 'block';
    btnClWhlLib.style.display = 'none';
    whlLib.style.animation = 'compression 0.5s forwards';
    whlLibText.style.display = 'none';
    event.stopPropagation();
});

var btnOpMyLib = document.getElementById('openMyLibrary');
var btnClMyLib = document.getElementById('closeMyLibrary');
var myLib = document.getElementById('myLibrary');
var myLibText = document.getElementById('myLibraryTextarea');

btnOpMyLib.addEventListener('click', function(event) {
    btnOpMyLib.style.display = 'none';
    btnClMyLib.style.display = 'block';
    myLib.style.animation = 'stretching 0.5s forwards';
    myLibText.style.display = 'block';
    event.stopPropagation();
});

btnClMyLib.addEventListener('click', function(event) {
    btnOpMyLib.style.display = 'block';
    btnClMyLib.style.display = 'none';
    myLib.style.animation = 'compression 0.5s forwards';
    myLibText.style.display = 'none';
    event.stopPropagation();
});

var btnOpRecLib = document.getElementById('openRecomendationLibrary');
var btnClRecLib = document.getElementById('closeRecomendationLibrary');
var recLib = document.getElementById('recomendationLibrary');

btnOpRecLib.addEventListener('click', function(event) {
    btnOpRecLib.style.display = 'none';
    btnClRecLib.style.display = 'block';
    recLib.style.animation = 'stretching 0.5s forwards';
});

btnClRecLib.addEventListener('click', function(event) {
    btnOpRecLib.style.display = 'block';
    btnClRecLib.style.display = 'none';
    recLib.style.animation = 'compression 0.5s forwards';
});

//этот вариант не подходит, так как наши динамический кнопки не сразу попадают в DOM
/*document.querySelectorAll('.dop-button').forEach(button => {
    button.addEventListener('click', function() {
        console.log('функция отрабатывает!');
        const musicId = this.getAttribute('data-id');
        sendAddToLibraryRequest(musicId);
    });
});*/

// вспомогательная функция для проверки и обновления состояние кнопки
function updateLibraryButton(musicId, button, adding = true) {
    button.disabled = true; // блокируем кнопку
    button.innerText = adding ? 'Добавление...' : 'Удаление...'; // опционально меняем текст кнопки

    // выбор соответствующего URL и функции обработки в зависимости от операции
    const url = adding ? '/add-to-library/' : '/remove-from-library/';
    const processResponse = adding
        ? () => { button.innerText = 'Добавлено'; button.disabled = true; }
        : () => { button.innerText = 'Удалено'; button.remove(); };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
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
        console.log(data);
        processResponse(); // вызываем функцию для обработки ответа
    })
    .catch(e => {
        console.log('Ошибка:', e);
        button.innerText = adding ? 'Ошибка добавления' : 'Ошибка удаления';
    })
    .finally(() => {
        // если кнопку нужно снова активировать (только для добавления), делаем это здесь:
        if (adding) {
            button.disabled = false;
            button.innerText = 'Добавить';
        }
    });
}

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

// делегирование событий (идёт прослушка на клик на всём документе, и только потом проверка на принадлежность
// к классу dop-button)
// временно комментим и тестируем блокировку кликов во время выполнения запросов
/*document.addEventListener('click', function(event) {
    if (event.target.classList.contains('dop-button')) {
        console.log('функция отрабатывает');
        const musicId = event.target.getAttribute('data-id');
        sendAddToLibraryRequest(musicId);
        event.target.style.display = 'none';
    }
});*/

document.addEventListener('click', function(event) {
    if (event.target.classList.contains('dop-button') && !event.target.disabled) {
        console.log('Функция отправки запроса отрабатывает');
        const musicId = event.target.getAttribute('data-id');
        event.target.disabled = true; // отключаем кнопку во избежание повторного нажатия
        event.target.innerText = 'Добавление...'; // опционально можно сменить текст кнопки
        sendAddToLibraryRequest(musicId)
            .then(data => {
                console.log(data); // обработка данных полученных от сервера
                // код обработки успешного добавления, например:
                event.target.innerText = 'Добавлено';
                event.target.disabled = true; // если нужно, чтобы кнопка осталась неактивной
            })
            .catch(e => {
                console.log('Error:', e);
                event.target.innerText = 'Ошибка';
            })
            .finally(() => {
                // если кнопку нужно снова включить, делаем это здесь:
                // event.target.disabled = false;
                // event.target.innerText = 'Добавить';
            });
    }
});