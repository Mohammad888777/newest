function commentFormToggle(parent_id){
    const forms=document.getElementById(parent_id)
    if (forms.classList.contains("d-none")){
        forms.classList.remove("d-none")
    }else{
        forms.classList.add("d-none")
    }
}

function ToggleNotification(){
    const gets=document.getElementById("notification-container")
    if(gets.classList.contains("d-none")){
        gets.classList.remove("d-none")
    }else{
        gets.classList.add("d-none")
    }
}