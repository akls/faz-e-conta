// Pegar elementos do DOM
const form = document.getElementById("form")
const requiredInputs = form.querySelectorAll("input[required], select[required], textarea[required]")




// Adicionar eventos aos campos required
requiredInputs.forEach(campo =>{
    campo.classList.add("error");
    campo.addEventListener("input", () =>{
        if (campo.value){
            campo.classList.remove("error");
        }else{
            campo.classList.add("error");
        }
    })
})