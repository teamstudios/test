/**
 * Created by kodiers on 12/08/16.
 */

function disableGood(good_id) {
    $.post('/goods/disable-good/', {id: good_id}, function (data, status, xhr) {
        if (data['status'] == 'ok') {
            var selector = '[data-goodid="' + good_id + '"]';
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

function sellGood(good_id, user_id) {
    $.post('/goods/accept-bid/', {id: good_id, user_id: user_id}, function (data, status, xhr) {
        if (data['status'] == 'ok') {
            $('.cart-btn').remove();
        } else {
            console.log(data);
        }
    });
}