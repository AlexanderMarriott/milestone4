    $(document).on('click', '#add-button', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: "{% url 'basket_add' %}",
        data: {
            product_id: $('#add-button').val(),
            quantity: $('#select option:selected').text(),
            csrfmiddlewaretoken: '{{ csrf_token }}',
            action: 'post'
        },

        success: function (json) {

        },

        error: function (xhr, errmsg, err) {

        }
    });
});