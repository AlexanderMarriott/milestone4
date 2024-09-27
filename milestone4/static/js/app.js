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