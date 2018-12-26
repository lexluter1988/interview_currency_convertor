$(document).on('submit', '#currency-convert-form', function(event){
    event.preventDefault();
    console.log("form submitted!");
    convert_currency();
});

function convert_currency() {
    var source = $('#id_source_currency option:selected').html();
    var dest = $('#id_destination_currency option:selected').html();
    var amount = $('#id_amount')[0].value;

    console.log("converting currency!");
    console.log(amount);
    console.log(source);
    console.log(dest);

    $.ajax({
        url : "convert/", // the endpoint
        type : "POST",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data : JSON.stringify({ currency_from : source, currency_to : dest, amount : amount}),

        // handle a successful response
        success : function(json) {
            $('#id_result').val(json);
        },

        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};