$(document).on('submit', '#currency-convert-form', function(event){
    event.preventDefault();
    console.log("form submitted!")
    convert_currency();
});

function convert_currency() {
    console.log("converting currency!")
    // console.log($('#amount').val())
};