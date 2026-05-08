const formUtente = document.getElementById("formUtente");
const messaggio = document.getElementById("messaggio");

function gestisciSubmit(event){
    event.preventDefault();
    
    const nome = document.getElementById("Nome").value.trim();
    const cognome = document.getElementById("Cognome").value.trim();
    const data = document.getElementById("Data").value;

    if(!nome || !cognome || !data){
        alert("Attenzione, compila tutti i campi scemo");
        return;
    }

    //Alt + 96 poi stacchi Alt
    messaggio.textContent = `Hai inserito: ${nome} ${cognome} ${data}`
}

formUtente.addEventListener("submit", gestisciSubmit);