const formIscrizione = document.getElementById("formFeedback");
const messaggio = document.getElementById("messaggio"); // Questo serve se lo usi altrove nella pagina
const tabellaFeedback = document.getElementById("tabellaFeedback");

formIscrizione.addEventListener("submit", gestisciSubmit);

const dati = [];

function gestisciSubmit(event){
    event.preventDefault();
    
    const nome = document.getElementById("Nome").value.trim();
    const email = document.getElementById("Email").value.trim();
    const data = document.getElementById("Data").value;
    const select = document.getElementById("Selezione").value;
    const testoMessaggio = document.getElementById("messaggio").value.trim(); // Cambiato in testoMessaggio per evitare conflitti
    const newsletter = document.getElementById("newsletter").checked;   

    if(!nome || !email || !data || !select || !testoMessaggio){
        alert("Attenzione, compila tutti i campi scemo");
        return;
    }

    //Operatote ternario
    const iscrizione = newsletter ? "Si" : "No";

    //Alt + 96 poi stacchi Alt
    //messaggio.textContent = `Hai inserito: ${nome} ${email} ${data} ${ora} ${select} ${messaggio} ${iscrizione}`;

    const riga = document.createElement("tr");

    const dato = {nome, email, data, select, messaggio: testoMessaggio, iscrizione};
    dati.push(dato);
    const campi = ["nome", "email", "data", "select", "messaggio", "iscrizione"];

   
    for(let i = 0; i < campi.length; i++){
        const cella = document.createElement("td");
        cella.textContent= dato[campi[i]];
        //alla cella appena creata assegno il testo corrispondente al dato presente nell'oggettto dato alla chiave specificata da campi[i]
        //DEVO INSERIRE LE CELLLE NELLA RIGA
        riga.appendChild(cella);
    }

    const cellaAzioni = document.createElement("td");

    const bottoneElimina = document.createElement("button");
    bottoneElimina.textContent = "ELIMINA";

    bottoneElimina.addEventListener("click", function(){
        riga.remove();
        dati.splice(dati.indexOf(dato), 1);
        //nell'array dati cerca in quale posizione si trova l'oggetto DATO, rimuovo l'oggetto DATO dall'array DATI usando il metodo splice()
        //per rimuovere l'elemento alla posizione corrisponderte all'indice dell'oggettto DATO nell'array DATI
    })

    cellaAzioni.appendChild(bottoneElimina);
    riga.appendChild(cellaAzioni);

    tabellaFeedback.appendChild(riga);
}