function makeEditable(id,textbox_id, button_id,updatePos){
    let textbox = document.getElementById(textbox_id)
    let button = document.getElementById(button_id)
    let textValue = textbox.value
    textbox.disabled = false
    button.innerHTML = "Save"
    console.log(textbox_id)
    console.log(button_id)
    console.log(updatePos)
    button.onclick = function(){
        $.ajax({
            type:"POST",
            url:id,
            data:{
                info : textbox.value,
                id : textbox_id
            }
        })
        cancel(id,textbox_id,button_id,updatePos)
    }

    let newbutton = document.createElement("Button")
    newbutton.innerHTML ="Cancel"
    newbutton.onclick = function(){
        textbox.value = textValue
        cancel(id,textbox_id, button_id,updatePos);
    }
    newbutton.id = "cancelUpdate"
    let position = document.getElementById(updatePos)
    position.appendChild(newbutton)
}

function cancel(id,textbox_id,button_id,updatePos){
    let cancelButton = document.getElementById("cancelUpdate")
    let textbox = document.getElementById(textbox_id)
    let button = document.getElementById(button_id)
    textbox.disabled = true;
    button.id = button_id
    button.innerHTML="Aggiorna"
    button.onclick = function(){
        makeEditable(id,textbox_id,button_id,updatePos)
    }
    cancelButton.remove()
}