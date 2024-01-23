document.addEventListener('DOMContentLoaded', function () {
    document.addEventListener('keydown', function (event) {
        handleGlobalKeyDown(event);
    });

    setupDeleteButtonClick();

    setupCopyLinkClick();

    setupShowLinkClick();

    setupGenerateButtonClick();

    EmptyTagDiv();

    inputFilterCards();
});

function inputFilterCards() {
    const input = document.querySelector('#search-input-id');
    const cards = document.querySelectorAll('.password-item');
    input.addEventListener('input', filterCards);

    function filterCards(e) {
        const input_text = e.target.value;
        if(input_text) {
          cards.forEach((el) => {
            const title = el.querySelector('h3').innerText;
            const title_lowcase = title.toLocaleLowerCase();
            if(title_lowcase.includes(input_text) === false) {
              el.style.display = "none";
              console.log(el)
            }
            else {
              el.style.display = "block";
            }
          })
        }
        else {
          cards.forEach((el) => {
            el.style.display = "block";
          })
        }
      }
}

function EmptyTagDiv() {
    var listaSenhas = document.getElementById('listaSenhas');
    var numeroDeItens = listaSenhas.getElementsByTagName('li').length;
    blocoSenhas = document.getElementById('blocoSenhas')
    if (numeroDeItens === 0) {
        blocoSenhas.style.display = 'none'
    } else {
        blocoSenhas.style.display = 'block'
    }
}

function setIdToModal(id) {
    var botaoConfirmar = document.getElementById('botao-deletar-confirmar');
    var urlAtual = window.location.href;
    var novaUrl = urlAtual.replace("save/", "");
    botaoConfirmar.href = novaUrl + 'delete/' + id;
}

function toHomePage() {
    var urlAtual = window.location.href;
    var posicaoCore = urlAtual.indexOf("core/");
    if (posicaoCore !== -1) {
        var novaURL = urlAtual.substring(0, posicaoCore + 5);
        window.location.href = novaURL
    }
}

function randomPassword(tamanho) {
    const caracteres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_-+=<>?/[]{}|';
    let senha = '';
    for (let i = 0; i < tamanho; i++) {
        const indiceAleatorio = Math.floor(Math.random() * caracteres.length);
        senha += caracteres.charAt(indiceAleatorio);
    }
    return senha;
}

function setupGenerateButtonClick() {
    var buttonGenerate = document.getElementById('gerarSenhaBotao');
    var senhaInput = document.getElementById('senha');
    buttonGenerate.addEventListener('click', function (event) {
        senhaInput.value = randomPassword(24);
    });
}

function handleGlobalKeyDown(event) {
    var modalDelete = document.querySelector('#modal-deletar-confirmar');
    if (modalDelete.style.display === 'block') {
        if (event.keyCode === 27) {
            hideDeleteModal();
        } else if (event.keyCode === 13) {
            clickConfirmDeleteButton();
        }
    }
}

function setupDeleteButtonClick() {
    var buttonDelete = document.querySelectorAll('#id-delete-link');
    buttonDelete.forEach(function (button) {
        button.addEventListener('click', function (event) {
            handleDeleteButtonClick(event);
        });
    });
}

function handleDeleteButtonClick(event) {
    var modalDelete = document.querySelector('#modal-deletar-confirmar');
    modalDelete.style.display = 'block';

    var cancelarDelete = document.querySelector('#botao-deletar-cancelar');
    cancelarDelete.onclick = function () {
        hideDeleteModal();
    };

    var confirmarDelete = document.querySelector('#botao-deletar-confirmar');
    confirmarDelete.onclick = function () {
        hideDeleteModal();
    };
}

function setupCopyLinkClick() {
    var copyLinks = document.querySelectorAll('#id-copy-link');
    copyLinks.forEach(function (copyLink) {
        copyLink.addEventListener('click', function (event) {
            handleCopyLinkClick(event);
        });
    });
}

function handleCopyLinkClick(event) {
    event.preventDefault();
    var id = event.target.getAttribute('data-id');
    var senhaElement = document.getElementById(`idSenha${id}`);
    copyTextToClipboard(senhaElement.textContent.trim());
}

function setupShowLinkClick() {
    var showLinks = document.querySelectorAll('#id-show-link');
    showLinks.forEach(function (showLink) {
        showLink.addEventListener('click', function (event) {
            handleShowLinkClick(event);
        });
    });
}

function handleShowLinkClick(event) {
    event.preventDefault();
    var id = event.target.getAttribute('data-id');
    var senhaElement = document.getElementById(`idSenha${id}`);
    var usuarioElement = document.getElementById(`idUsuario${id}`);
    var senhaOculto = document.getElementsByClassName(`senha-oculto${id}`);
    var isTextVisible = senhaElement.classList.contains('visible');

    event.target.textContent = isTextVisible ? 'Mostrar' : 'Ocultar';
    senhaElement.classList.toggle('visible', !isTextVisible);
    usuarioElement.classList.toggle('visible', !isTextVisible);
    for (var i = 0; i < senhaOculto.length; i++) {
        senhaOculto[i].style.display = isTextVisible ? 'block' : 'none';
    }
}

function hideDeleteModal() {
    var modalDelete = document.querySelector('#modal-deletar-confirmar');
    modalDelete.style.display = 'none';
}

function clickConfirmDeleteButton() {
    var confirmarDelete = document.querySelector('#botao-deletar-confirmar');
    confirmarDelete.click();
}

function copyTextToClipboard(text) {
    var inputElement = document.createElement('input');
    inputElement.setAttribute('type', 'text');
    inputElement.setAttribute('value', text);
    inputElement.style.position = 'absolute';
    inputElement.style.left = '-9999px';

    document.body.appendChild(inputElement);
    inputElement.select();
    document.execCommand('copy');
    document.body.removeChild(inputElement);
}