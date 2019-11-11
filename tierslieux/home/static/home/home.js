$(".passwordForm").submit(function(event){
    if ($("#password").val() !== $("#validation").val()) {
        $('#warningPassword').text('Mots de passes différents').show();
        event.preventDefault();
        console.log("event prevented");
    }
});

// TODO : This could maybe be done in a view :shrug: