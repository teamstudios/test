/**
 * Created by kodiers on 04/08/16.
 */
function deleteFromCart(good_id) {
    var selector = '[data-goodid="' + good_id + '"]';
    $.post('/cart/remove-from-cart/', {id: good_id}, function (data, status, xhr) {
        if (data['status'] == 'ok') {
            var category_block = Array.prototype.slice.call(document.querySelectorAll(selector));
            if (category_block.length == 0) {
                console.log('Error: elements not found');
            } else {
                $('.category-container-tab2').masonry('remove', category_block[0]).masonry('layout');
            }
            var count = parseInt($('#goods_count').text());
            $('#goods_count').text(count - 1);
        } else {
            console.log(data);
        }
    });
}