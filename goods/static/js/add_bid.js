/**
 * Created by kodiers on 02/08/16.
 */
function addBid(good_id, good_bid, bid_username) {
    var btn_id = "#myBtn" + good_id;
    var btn = document.getElementById(btn_id);
    $('#id_good_bid').val(good_id);
    if (good_bid != 0) {
        $('#bid_price').text(good_bid);
        $('#bid_user').text(bid_username);
    } else {
        $('#bid_p').text('No bids yet');
    }
    var modal = document.getElementById('bid-modal');
    modal.style.display = "block";
}

function makeBid() {
    var good_id = $('#id_good_bid').val();
    var user_bid = $('#id_price').val();
    $.post('/goods/add-bid/', {id: good_id, price: user_bid}, function (data, status, xhr) {
        if (data['status'] == 'ok') {
            console.log(data);
            var modal = document.getElementById('bid-modal');
            modal.style.display = "none";
        }
    });
}

function rejectBid(good_id) {
    $.post('/goods/remove-bid/', {id: good_id}, function (data, status, xhr) {
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