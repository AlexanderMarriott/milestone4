// app.js


// add button
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
            //console.log(json);
            document.getElementById('basket-qty').textContent = json.qty;
        },
        error: function (xhr, errmsg, err) {
            // Handle error
        }
    });
});

// delete button
$(document).on('click', '.delete-button', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: basketDeleteUrl,  // Use a variable for the URL
        data: {
            product_id: $(this).data('index'),
            csrfmiddlewaretoken: csrfToken,  // Use a variable for the CSRF token
            action: 'post'
        },
        success: function (json) {
            //console.log(json);

           location.reload()
           
           document.getElementById('basket-qty').textContent = json.qty
           document.getElementById('total').textContent = json.total
        },
        error: function (xhr, errmsg, err) {
            // Handle error
        }
    });
});


// update button

$(document).on('click', '.update-button', function (e) {
    e.preventDefault();

    var theproductid = $(this).data('index');
    $.ajax({
        type: 'POST',
        url: basketUpdateUrl,  // Use a variable for the URL
        data: {
            product_id: theproductid,
            product_quantity: $('#select'+theproductid+' option:selected').text(),

            csrfmiddlewaretoken: csrfToken,  // Use a variable for the CSRF token
            action: 'post'
        },
        success: function (json) {
            //console.log(json);

           location.reload()
           
           document.getElementById('basket-qty').textContent = json.qty;
           document.getElementById('total').textContent = json.total;
        },
        error: function (xhr, errmsg, err) {
            // Handle error
        }
    });
});


// timer for message alerts

var timed_message = document.getElementById('timed-message');

setTimeout(function() {
    timed_message.style.display = 'none';
    
}, 3000);


// Complete checkout
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('form').addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission
        $.ajax({
            type: 'POST',
            url: completeOrderUrl,
            data: {
                first_name: $('#first_name').val(),
                last_name: $('#last_name').val(),
                email: $('#email').val(),
                address1: $('#address1').val(),
                address2: $('#address2').val(),
                city: $('#city').val(),
                country: $('#country').val(),
                postal_code: $('#postal_code').val(),
                csrfmiddlewaretoken: csrfToken,
                action: 'post'
            },
            success: function(json) {
                window.location.replace(paymentSuccessUrl);
            },
            error: function(xhr, errmsg, err) {
                window.location.replace(paymentFailedUrl);
            }
        });
    });
});