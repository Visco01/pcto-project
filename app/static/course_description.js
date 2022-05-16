function makeEditable(){
    let textbox = document.getElementById("descriptionBox")
    let button = document.getElementById("updateRequest")
    textValues = textbox.value
    console.log(textbox)
    textbox.disabled = false
    button.innerHTML = "Save"
    button.onclick = function(){
        console.log("hi")
    }

    let newbutton = document.createElement("Button")
    newbutton.innerHTML ="Cancel"
    newbutton.onclick = function(){

        textbox.remove()
        let replacement = document.createElement("textarea")
        replacement.className ="form-control"
        replacement.id = "descriptionBox"
        replacement.style = "resize:none"
        replacement.disabled = true
        replacement.rows = "3"
        replacement.innerHTML = textValues
        console.log(replacement)
        let whereto = document.getElementById("textboxArea")
        whereto.appendChild(replacement)

        cancel();

    }
    newbutton.id = "cancelUpdate"
    let position = document.getElementById("updatePos")
    position.appendChild(newbutton)
}

function cancel(){
    let cancelButton = document.getElementById("cancelUpdate")
    let button = document.getElementById("updateRequest")
    let textbox = document.getElementById("descriptionBox")
    textbox.disabled = true;
    button.innerHTML="Aggiorna"
    button.onclick = function(){
        makeEditable()
    }
    cancelButton.remove()
}