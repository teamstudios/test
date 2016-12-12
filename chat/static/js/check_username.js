/**
 * Created by kodiers on 14/10/15.
 * Send AJAX to check username 
 */

$(document).ready(function () {
    $('#idReceiver').keyup(function () {
        var value = $(this).val();
        $.post('/chat/check_username/', {'partner': value},
            function (data, status, xhr) {
                if (data.result) {
                    $('#usernameHint').text('Did you mean: ' + data.result);
                } else {
                    $('#usernameHint').html('<span class="hint">Users with same name not found</span>');
                }
            }
        );
        
    });
});
