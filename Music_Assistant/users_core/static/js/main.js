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

btnOpMyLib.addEventListener('click', function(event) {
    btnOpMyLib.style.display = 'none';
    btnClMyLib.style.display = 'block';
    myLib.style.animation = 'stretching 0.5s forwards';
    event.stopPropagation();
});

btnClMyLib.addEventListener('click', function(event) {
    btnOpMyLib.style.display = 'block';
    btnClMyLib.style.display = 'none';
    myLib.style.animation = 'compression 0.5s forwards';
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