function disactivateButtons(){
    $("#toggle>*").attr("class","btn btn-secondary")
}

function clickSingle(){
    disactivateButtons()
    $("#single").attr("class","btn btn-primary")
    $("#schedule-form").attr("style","display:none")
    $("#single-form").attr("style","display:block")
}

function clickCalendar(){
    disactivateButtons()
    $("#calendar").attr("class","btn btn-primary")
    $("#schedule-form").attr("style","display:block")
    $("#single-form").attr("style","display:none")
}

function addDate(){
    let i = 0
    while(i < 4 && states[i] != false){
        i++
    }
    displayed_divs++
    states[i] = true
    $("#day" + (i + 1)).attr("style","display:block")
    if(displayed_divs == 4){
        $("#day-buttons").attr("style","display:none")
    }
}

function removeDay(id){
    $("#days-" + (id)).val('none')
    $('#day'+(id+1)).attr("style","display:none")
    states[id] = false
    displayed_divs--
    $("#day-buttons").attr("style","display:block")
}