// app.js


// Add button
$(document).on('click', '#add-button', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: basketAddUrl,  // Ensure this URL is defined and correct
        data: {
            product_id: $('#add-button').val(),
            quantity: $('#select option:selected').text(),
            csrfmiddlewaretoken: csrfToken,  // Ensure this token is defined and correct
            action: 'post'
        },
        success: function (json) {
            // Update the quantity display without refreshing the page
            document.getElementById('basket-qty').textContent = json.qty;
            document.getElementById('total').textContent = json.total;
            setTimeout(function() {
                location.reload(true);
            }, 1000);
        },
        error: function (xhr, errmsg, err) {
            console.error(xhr.status + ": " + xhr.responseText);
        }
    });

    
});

// Delete button
$(document).on('click', '.delete-button', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: basketDeleteUrl,  // Ensure this URL is defined and correct
        data: {
            product_id: $(this).data('index'),
            csrfmiddlewaretoken: csrfToken,  // Ensure this token is defined and correct
            action: 'post'
        },
        success: function (json) {
            // Update the quantity display without refreshing the page
            document.getElementById('basket-qty').textContent = json.qty;
            document.getElementById('total').textContent = json.total;
            // Optionally, remove the item from the DOM
            $(`#item-${json.product_id}`).remove();
        },
        error: function (xhr, errmsg, err) {
            console.error(xhr.status + ": " + xhr.responseText);
        }
    });
});

// Update button
$(document).on('click', '.update-button', function (e) {
    e.preventDefault();

    var theproductid = $(this).data('index');
    $.ajax({
        type: 'POST',
        url: basketUpdateUrl,  // Ensure this URL is defined and correct
        data: {
            product_id: theproductid,
            product_quantity: $('#select' + theproductid + ' option:selected').text(),
            csrfmiddlewaretoken: csrfToken,  // Ensure this token is defined and correct
            action: 'post'
        },
        success: function (json) {
            // Update the quantity display without refreshing the page
            document.getElementById('basket-qty').textContent = json.qty;
            document.getElementById('total').textContent = json.total;
        },
        error: function (xhr, errmsg, err) {
            console.error(xhr.status + ": " + xhr.responseText);
        }
    });
});

// Function to reload the page
function reloadPage() {
    location.reload();
}

// Attach event listener to elements with the .reload class
document.addEventListener('DOMContentLoaded', function() {
    const reloadButtons = document.querySelectorAll('.reload');
    reloadButtons.forEach(function(button) {
        button.addEventListener('click', reloadPage);
    });
});





