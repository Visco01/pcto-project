function makeEditable(id){
    textbox = document.getElementById("descriptionBox")
    let button = document.getElementById("updateRequest")
    textValue = textbox.value
    console.log(textbox)
    textbox.disabled = false
    button.innerHTML = "Save"
    button.onclick = function(){
        $.ajax({
            type:"POST",
            url:id,
            data:{info : textbox.value}
        })
        cancel()
    }

    let newbutton = document.createElement("Button")
    newbutton.innerHTML ="Cancel"
    newbutton.onclick = function(){

        textbox.value = textValue
        cancel();

    }
    newbutton.id = "cancelUpdate"
    let position = document.getElementById("updatePos")
    position.appendChild(newbutton)
}

function cancel(){
    let cancelButton = document.getElementById("cancelUpdate")
    let button = document.getElementById("updateRequest")
    textbox.disabled = true;
    button.innerHTML="Aggiorna"
    button.onclick = function(){
        makeEditable()
    }
    cancelButton.remove()
}