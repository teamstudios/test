/**
 * Created by kodiers on 27/07/16.
 */

function addToCart(good_id) {
    if ($('#about-cart').data('action') == 'add') {
        var url = '/cart/add-to-cart/';
        var data_action = 'remove';
        var a_text = 'In cart';
    } else {
        var url = '/cart/remove-from-cart/';
        var data_action = 'add';
        var a_text = 'Add to cart';
    }
    $.post(url, {id: good_id}, function (data, status, xhr) {
        if (data['status'] == 'ok') {
            $('#about-cart').data('action', data_action);
            $('#about-cart').text(a_text);
        } else {
            console.log(data);
        }
    });
}