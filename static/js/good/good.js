/* global $ */
$(window).load(function(){

});
 // Helper function to redirect on ogin url if ajax view require login
$(document).ready(function() {
        $('.ui.sticky').sticky({
            context: '#main_left'
        });
        $('#ship_tab').hide();
        $('#about_tab').hide();
        $('.tab').click(function() {
            $('.tab').removeClass('active');
            $(this).addClass('active');
        });
        $('#tab1').click(function() {
	        $('#desc_tab').show();
	        $('#ship_tab').hide();
	        $('#about_tab').hide();
        });
        $('#translate').on('click', function(e) {
            e.preventDefault();
            $('#good_description').translate({ target : 'ru' });
        });
        $('#tab2').click(function() {
	        $('#desc_tab').hide();
	        $('#ship_tab').show();
	        $('#about_tab').hide();
        });
        $('#tab3').click(function() {
	        $('#desc_tab').hide();
	        $('#ship_tab').hide();
	        $('#about_tab').show();
        });
    // Subscribe action scripts
    if ($('#about-signup').data('action') == 'remove') {
        $('#about-signup').html('{{ unfollow }}');
        $('.green #about-signup').css('background', '#b1fe00');
        $('.orange #about-signup').css('background', '#ff6600');
        $('#about-signup').css('color', '#fff');
    } else {
        $('#about-signup').html('{{ follow }}');
        $('#about-signup').css('background', '#fffefc');
        $('.green #about-signup').css('color', '#b1fe00');
        $('.orange #about-signup').css('color', '#ff6600');
    }
    $('#about-signup').click(function(e){
        e.preventDefault();
        $.post('{% url "accounts:add_subscriber" %}',
            {
                pk: $(this).data('id'),
                action: $(this).data('action')
            },
            function (data, status, xhr) {
                check_login_url(xhr);
                if (data['status'] == 'ok') {
                    var previous_action = $('#about-signup').data('action');
                    $('#about-signup').data('action', previous_action == 'add' ? 'remove' : 'add');
                    if (previous_action == 'add') {
                        $('#about-signup').html('{{ unfollow }}');
                        $('.green #about-signup').css('background', '#b1fe00');
                        $('.orange #about-signup').css('background', '#ff6600');
                        $('#about-signup').css('color', '#fff');
                    } else {
                        $('#about-signup').html('{{ follow }}');
                        $('#about-signup').css('background', '#fffefc');
                        $('.green #about-signup').css('color', '#b1fe00');
                        $('.orange #about-signup').css('color', '#ff6600');
                    }
                }
            }
        );
    });
        // lazy load
    var page = 1;
    var empty_page = false;
    var block_request = false;
    $(window).scroll(function() {
        var margin = $(document).height() - $(window).height() - 200;
        if ($(window).scrollTop() > margin && empty_page == false && block_request == false) {
            block_request = true;
            page += 1;
            $.get('?page=' + page, function (data) {
                if (data == ''){
                    empty_page = true;
                } else {
                    block_request = false;
                    var $content = $(data);
                    $('#category-container').append($content).masonry('appended', $content);
                }
            });
        }
    });
}); //Конец ready

/*         function showMessageWindow() {
             console.log('clicked');
                $('#message-modal').show();
         }

         function closeMessage() {
             $('#message-modal').hide();
         }

         function sendMessageChat(recipient) {
             var text = $('#id_message').val();
             $.post('{% url "chat:send_message_ajax" %}', {partner: recipient, text: text}, function (data, status, xhr) {
                 if (data['status'] == 'ok') {
                     $('#message-modal').hide();
                 } else {
                     $('#message_errors').text(data['reason']);
                 }
             });
         }
*/