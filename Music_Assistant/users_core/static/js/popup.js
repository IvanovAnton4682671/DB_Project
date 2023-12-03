var button_show = document.getElementById('showPopup');
var button_aut = document.getElementById('showAut');
var button_reg = document.getElementById('showReg');
var popup = document.getElementById('popup');
var back_blur = document.getElementById('popup-blur');
var form_reg = document.getElementById('form-reg');
var form_aut = document.getElementById('form-aut');
var dop_div = document.getElementById('dop-div');

button_show.addEventListener('click', function(event) {
  popup.style.display = 'block';
  popup.style.animation = 'trans 0.3s forwards';
  form_reg.style.display = 'block';
  form_aut.style.display = 'none';
  back_blur.style.display = 'block';
  event.stopPropagation();
});

button_aut.addEventListener('click', function() {
  form_reg.style.display = 'none';
  form_aut.style.display = 'block';
  form_aut.style.animation = 'right 0.2s forwards';
  dop_div.style.animation = 'up 0.3s forwards';
});

button_reg.addEventListener('click', function() {
  form_aut.style.display = 'none';
  form_reg.style.display = 'block';
  form_reg.style.animation = 'left 0.2s forwards';
  dop_div.style.animation = 'down 0.3s forwards';
});

popup.addEventListener('click', function(event) {
  event.stopPropagation();
});

window.addEventListener('click', function() {
  popup.style.animation = 'a_trans 0.3s forwards';
  if (form_aut.style.display != 'none') {
    dop_div.style.animation = 'down 0.3s forwards';
  }
  back_blur.style.display = 'none';
});

var reg_passInp = document.getElementById('reg-passwordInput');
var reg_togPas = document.getElementById('reg-togglePassword');
var aut_passInp = document.getElementById('aut-passwordInput');
var aut_togPas = document.getElementById('aut-togglePassword');

reg_togPas.addEventListener('click', function() {
  if (reg_passInp.type === 'password') {
    reg_passInp.type = 'text';
    reg_togPas.style.background = 'url("eye1.svg") no-repeat center';
    reg_togPas.style.backgroundSize = 'contain';
  }
  else {
    reg_passInp.type = 'password';
    reg_togPas.style.background = 'url("eye2.svg") no-repeat center';
    reg_togPas.style.backgroundSize = 'contain';
  }
});

aut_togPas.addEventListener('click', function() {
  if (aut_passInp.type === 'password') {
    aut_passInp.type = 'text';
    aut_togPas.style.background = 'url("eye1.svg") no-repeat center';
    aut_togPas.style.backgroundSize = 'contain';
  }
  else {
    aut_passInp.type = 'password';
    aut_togPas.style.background = 'url("eye2.svg") no-repeat center';
    aut_togPas.style.backgroundSize = 'contain';
  }
});

var nick = document.getElementById('nickname');
var regE = document.getElementById('regEmail');
var passSig = document.getElementById('reg-passwordInput');
var butSig = document.getElementById('signUp');
var autE = document.getElementById('autEmail');
var passLog = document.getElementById('aut-passwordInput');
var butLog = document.getElementById('logIn');

butSig.addEventListener('click', function(event) {
  if (nick.value === '' || regE.value === '' || passSig.value === '') {
    if (nick.value === '') {
      nick.style.border = '2px solid yellow';
    }
    else {
      nick.style.border = '2px solid rgb(216, 2, 134)';
    }
    if (regE.value === '') {
      regE.style.border = '2px solid yellow';
    }
    else {
      regE.style.border = '2px solid rgb(216, 2, 134)';
    }
    if (passSig.value === '') {
      passSig.style.border = '2px solid yellow';
    }
    else {
      passSig.style.border = '2px solid rgb(216, 2, 134)';
    }
    alert('Пожалуйста, не оставляйте поля пустыми!');
    event.preventDefault();
    return;
  }
});

butLog.addEventListener('click', function(event) {
  if (autE.value === '' || passLog.value === '') {
    if (autE.value === '') {
      autE.style.border = '2px solid yellow';
    }
    else {
      autE.style.border = '2px solid rgb(216, 2, 134)';
    }
    if (passLog.value === '') {
      passLog.style.border = '2px solid yellow';
    }
    else {
      passLog.style.border = '2px solid rgb(216, 2, 134)';
    }
    alert('Пожалуйста, не оставляйте поля пустыми!');
    event.preventDefault();
    return;
  }
});