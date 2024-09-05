// app.js
$(document).on('click', '#add-button', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: basketAddUrl,  // Use a variable for the URL
        data: {
            product_id: $('#add-button').val(),
            quantity: $('#select option:selected').text(),
            csrfmiddlewaretoken: csrfToken,  // Use a variable for the CSRF token
            action: 'post'
        },
        success: function (json) {
            console.log(json);
        },
        error: function (xhr, errmsg, err) {
            // Handle error
        }
    });
});