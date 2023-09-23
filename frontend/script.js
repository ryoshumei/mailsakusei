// count exampleTextarea characters and show in counter
function countChar(val) {
    const len = val.value.length;
    if (len >= 500) {
        val.value = val.value.substring(0, 500);
    } else {
        $('#charCount').text(500 - len);
    }
}
// countChar exampleTextarea always on load
$(document).ready(function() {
    var len = $('#exampleTextarea').val().length;
    $('#charCount').text(500 - len);

    // Bind the countChar function to the input event of the textarea
    $('#exampleTextarea').on('input', function() {
        countChar(this);
    });

});

//when the user clicks on the button, send the data to the server
$('#generate').click(function(event) {
    //stop navigating to the page given in the form action
    event.preventDefault();
    // #exampleTextarea cant be empty
    if ($('#exampleTextarea').val() == '') {
        $('#resultOutput').html('Please enter a text');
        $('#resultOutputDiv').removeClass('d-none');
        return;
    }
    //get the data from the form field both recipient,signature and exampleTextarea
    const recipient = $('#recipient').val();
    const signature = $('#signature').val();
    const text = $('#exampleTextarea').val();
    // make a object with the data
    const data = {
        recipient: recipient,
        signature: signature,
        text: text
    }
    //convert the object to a JSON string
    const json = JSON.stringify(data);
    // clear #resultOutput
    $('#resultOutput').val('');
    //show the user that the data is being processed using a loading gif image
    $('#resultOutput').val('Processing please wait...');
    //remove d-none class from the #resultOutputDiv if exists
    $('#resultOutputDiv').removeClass('d-none');
    //ajax call, a function that takes an object as a json and sends it to the server
    $.ajax({
        type: 'POST',
        url: '/api/generate',
        data: json,
        contentType: 'application/json',
        dataType: 'json',
        //accepts the response from the server
        success: function(data) {
            console.log('success');
            console.log(JSON.stringify(data));
            const output = data.result;
            //show the result in the resultOutput field
            $('#resultOutput').val(output);
            console.log('success');



        }
        //if the ajax call fails, show the user an error message
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.log('error');
        $('#resultOutput').html('Error: ' + + jqXHR.responseText + ' ' + textStatus + ' ' + errorThrown);
    });
});