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
};