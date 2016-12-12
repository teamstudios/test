/**
 * Created by kodiers on 14/10/15.
 * Chat JS file.
 */
$(document).ready(function () {
    // After document ready open WebSocket connection
    scroll_chat_window();
    var chat_id = $('#idChat').val();
    var sender = $('#idSender').val();
    var host = 'ws://localhost:8888/send_async_message/' + chat_id + '/';
    var ws = new WebSocket(host);
    ws.onopen = function (e) {
        console.log('WebSocket created');
    };
    ws.onclose = function (e) {
        console.log('WebSocket closed');
    };
    ws.onmessage = function (e) {
        var response = JSON.parse(e.data);
        if (response['Error']) {
            console.log(response);
            return;
        }
        var html_string = response['text'];
        if (response['sender_id'].toString() === sender) {
            html_string = '<div class="sender-bubble"><p class="sender"><span class="message_date"> '
                + response['datetime'] + '</span> ' + response['sender'] + ':</p><p class="chat_message">' +
                response['text'] + '</p></div>';
        } else {
            html_string = '<div class="partner-bubble"><p class="receiver"><span class="message_date">' +
                response['datetime'] + '</span> ' + response['sender'] + ':</p><p class="chat_message">' +
                response['text'] + '</p></div>';
        }
        $("div.conversation").append(html_string);
        scroll_chat_window();
    };
    $('#idSendMessageForm').on('submit', function (event) {
        event.preventDefault();
    });
    $('#idSend').click(function (event) {
        var text = $('#idText').val();
        // Clear html tags
        var clean_text = text.replace(/(<([^>]+)>)/ig, "");
        var msg = JSON.stringify({'sender': sender, 'text': clean_text});
        sendMessage(ws, msg);
        $('#idText').val('');
    })

});

function scroll_chat_window() {
    $("div.conversation").scrollTop($("div.conversation")[0].scrollHeight);
}

function sendMessage(ws, msg) {
    waitForSocketConnection(ws, function () {
        console.log('Sending message');
        ws.send(msg);
    });
};

function waitForSocketConnection(socket, callback) {
    setTimeout(function () {
        if(socket.readyState === 1) {
            if (callback !== undefined) {
                callback();
            }
            return;
        } else {
            waitForSocketConnection(socket, callback);
        }
    }, 5);
}