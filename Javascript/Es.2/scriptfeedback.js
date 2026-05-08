const formUtente = document.getElementById("formUtente");
const messaggio = document.getElementById("messaggio");

function gestisciSubmit(event){
    event.preventDefault();
    
    const nome = document.getElementById("Nome").value.trim();
    const email = document.getElementById("Email").value.trim();
    const data = document.getElementById("Data").value;
    const ora = document.getElementById("Ora").value;
    const select = document.getElementById("Selezione").value;

    if(!nome || !email || !data ||!ora){
        alert("Attenzione, compila tutti i campi scemo");
        return;
    }

    //Alt + 96 poi stacchi Alt
    messaggio.textContent = `Hai inserito: ${nome} ${email} ${data} ${ora} ${select}`
}

formUtente.addEventListener("submit", gestisciSubmit);