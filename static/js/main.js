/* global $ */
function check_login_url(xhr) {
    var login_url = '{% url "accounts:login" %}' + "?next={% url 'goods:good_view' good.pk %}";
    if (xhr.responseText.indexOf('login') != -1 ) {
     // Check if response doesn't contain redirect to login. If it contains - redirect to login window
     window.location = login_url;
    }
}
// Get CSRF cookie protection
var csrftoken = $.cookie('csrftoken');
function csrfSafeMethod (method) {
    // These HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if(!csrfSafeMethod(settings.type) && !this.crossDomain) {
            // Set X-CSRFToken HTTP Header
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$(document).ready(function() {
    $('#up').hide();
    $('#search_button').on('click', function(){
        $('.hideon').each(function() {
           $(this).toggleClass('hiden'); 
        });
        $('#search_input').toggleClass('hiden');
    });
    $(window).scroll(function() {
        if($(window).scrollTop()) {
            $('#up').fadeIn();
            $(".visibility-eye").css("top","75px");
        } else {
            $('#up').fadeOut();
            $(".visibility-eye").css("top","225px");
        }
        });
    
    $('#up').click(function() {
        $('body,html').animate({scrollTop:0},100);
    });
            
    $('#vitrina-icon-bottom').hover(function(){
        $(this).transition('pulse');
    }, function(){});
    $('#cart-icon-bottom').hover(function(){
        $(this).transition('pulse');
    }, function(){});
    
    $( ".orange" ).each(function() {
        $( this ).removeClass( "orange" );
        $( this ).addClass( "olive" );
    });
});