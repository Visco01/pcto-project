function enableEditing(){
    $(".form-control").prop("disabled",false);
    $(".form-select").prop("disabled",false);
}

function disabledEditing(){
    $(".form-control").prop("disabled",true);
    $(".form-select").prop("disabled",true);
}


function getFormData(){
    let controlElements = $(".form-control");
    let selectElements = $(".form-select");
    let values = {};
    for(let i = 0; i < controlElements.length; i++){
        values[controlElements.get(i).id] = controlElements.get(i).value;
    }
    for(let i = 0; i < selectElements.length; i++){
        values[selectElements.get(i).id] = selectElements.get(i).value;
    }
    return values;
}

function resetFormData(info){
    let controlElements = $(".form-control");
    let selectElements = $(".form-select");
    for(let i = 0; i < controlElements.length; i++){
        controlElements.get(i).value = info[controlElements.get(i).id]
    }
    for(let i = 0; i < selectElements.length; i++){
        selectElements.get(i).value = info[selectElements.get(i).id]
    }
}

function saveUpdate(id_course,update_button,button_lesson,info){
    info = getFormData();
    $.ajax({
        type:"POST",
        url:id_course,
        data:{
            a : JSON.stringify(info)
        },
        datatype:"json"
    });
    returnChanges(id_course,update_button,button_lesson,info)
}

function returnChanges(id_course,update_button,button_lesson,info){
    $("#buttonCancel").remove();
    $("#buttonRow").append(button_lesson);
    update_button.html("Aggiorna");
    update_button.get(0).onclick = function(){updateCourse(id_course);};
    resetFormData(info);
    disabledEditing();
}

function addCancelButton(id_course,update_button,button_lesson,info){
    button = document.createElement('button');
    button.setAttribute("class","btn btn-primary");
    button.innerHTML = "Anulla";
    button.id = "buttonCancel";
    button.onclick = function(){returnChanges(id_course,update_button,button_lesson,info);}
    document.getElementById("buttonRow").appendChild(button);
}

function updateCourse(id_course){
    enableEditing();
    let info = getFormData();
    let button_lesson = $("#lessonsButton");
    let update_button = $("#updateButton");
    update_button.get(0).innerHTML="Salva";
    update_button.get(0).onclick=function(){saveUpdate(id_course,update_button,button_lesson,info)};
    button_lesson.remove();
    addCancelButton(id_course,update_button,button_lesson,info);
}