/* global $ */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

$(window).load(function(){
    $('#user_lots').wookmark({
        autoResize: true,
        itemWidth: 180,
		container: $('#user_lots'),
		direction: 'left',
		align: 'left',
		offset: 7,
    });
});


$(document).ready(function(){
    //$('#revtoggle').on('click', function(){
       //$('#reviews').toggleClass('hiden'); 
    //});
    $('#lottoggle').on('click', function(){
       $('#wrapper-tabs').toggleClass('hiden'); 
    });
    
    $("#revtoggle").click(function(){
        if($("#reviews").css("height")=="90px"){
            $("#reviews").animate({height: "100%"}, 500, "linear");
            $("#rev_pointer").hide();
        }
        else if ($("#reviews").is( ":hidden" )){
            $("#reviews").slideDown('fast');
        }
        else{
            console.log('up')
            $("#reviews").slideUp('fast');
        }
    });
    
    //$('#logo-module, #banner-module, #upload-custom-banner-popup, #upload-custom-logo-popup, #complaint-popup, #reviews-popup-wrapper').modal();
    
    $('#imageCover').on('click', function(){
        $('#avaLoad').hide();
        $('#bannerLoad').show();
        $('#img-load-module').modal('show');
    });
    
    $('#avatarImageDiv').on('click', function(){
        $('#bannerLoad').hide();
        $('#avaLoad').show();
        $('#img-load-module').modal('show');
    });

    $('#upload-custom-banner-popup').modal('attach events', '#bannerLoad');
    $('#upload-custom-logo-popup').modal('attach events', '#avaLoad');
    
    
    $('#loadFile').click(function() {
        $('#bannerFile').click();
    });
    // Upload cover by AJAX
    $('#bannerLoadContainer').cropit();
    $('#btnBannerLoad').on('click', function(e){
        e.preventDefault();
        var banner = $('#bannerLoadContainer').cropit('export');
        var formdata = new FormData();
        formdata.append('cover', banner);
        $('.cropped').append('<img src="'+banner+'">');
        // Upload cropped cover on server
        $.ajax({
            url: '/accounts/upload-image/',
            type: 'POST',
            data: formdata,
            headers: {
    			'X-CSRFToken': getCookie('csrftoken')
  			},
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                if (data.status == 'ok') {
                    console.log(data.url);
                    $('#imageCover').html('<img src="' + data.url + '" width=960px height=222px>');
                    $('#upload-custom-banner-popup').modal('hide');
                }
            }
        });
    });
    $('#clsBannerLoad').click(function(e){
        e.preventDefault();
        $('#upload-custom-banner-popup').modal('hide');
    });
        
    // Upload avatar by AJAX
     $('#loadAvFile').click(function() {
        $('#avatarFile').click();
    });
    $('#avatarLoadContainer').cropit({smallImage: 'allow'});
    $('#btnAvatarLoad').on('click', function(e){
        e.preventDefault();
        var banner = $('#avatarLoadContainer').cropit('export');
        var formdata = new FormData();
        formdata.append('avatar', banner);
        $('.cropped').append('<img src="'+banner+'">');
        // Upload cropped cover on server
        $.ajax({
            url: '/accounts/upload-image/',
            type: 'POST',
            data: formdata,
            headers: {
    			'X-CSRFToken': getCookie('csrftoken')
  			},
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                if (data.status == 'ok') {
                    console.log(data.url);
                    $('#avatarImageDiv').html('<img src="' + data.url + '" width=90px height=90px class="circular">');
                    $('#upload-custom-logo-popup').modal('hide');
                }
            }
        });
    });
    
    $('#clsAvatarLoad').click(function(e){
        e.preventDefault();
        $('#upload-custom-logo-popup').modal('hide');
    });
    
    $('.ui.rating').rating('disable');

    $('#okReview').on('click', function (e) {
            // Create review send AJAX call
            e.preventDefault();
            mark = $('#rateReview').rateit('value');
            text = $('#textReview').val();
            about = '{{ profile.user.pk }}';
            $.post('{% url "accounts:add_review" %}',
                    {
                        user_id: about,
                        text: text,
                        mark: mark
                    },
                    function (data) {
                        if (data.status == 'ok') {
                            // If assition of review was successfull - add it
                            $('#rating_section').children("div.item.clearfix:last").remove();
                            var div_id = '#' + data.author;
                            var html = "<div class='item clearfix'><div class='logo-section'><img src='" + data.logo_url +
                            "' width='37px' height='36px'>" + "</div><div class='text-section'>" +
                            "<div class='headline'>" + data.author + "<span class='stars'>" +
                            "<div class='rateit smallstars' data-rateit-value='" + data.mark +
                            "' data-rateit-ispreset='true' data-rateit-readonly='true' data-rateit-starwidth='12' data-rateit-starheight='12'" +
                            "id='" + data.author + "'></div></span></div><div class='copy'>" + data.text + "</div></div></div>";
                            $('#rating_section').prepend(html);
                            $(div_id).rateit();
                            $(div_id).rateit('value', data.mark);
                            // Change total count
                            var count_prevous_count = parseInt($('#total_marks_number').text());
                            $('#total_marks_number').text(count_prevous_count + 1);
                            // Change average mark
                            var old_avg = parseFloat($('#avgMark').text());
                            var old_avg_sum = old_avg * count_prevous_count;
                            var new_avg= (old_avg_sum + Number(data.mark)) / (count_prevous_count + 1);
                            $('#avgMark').text(new_avg.toFixed(1));
                            $(".reviews-popup-wrapper, .overlay").hide();
                        } else {
                            console.log(data);
                        }
                    }
            );
        });
    
    $('#complaint_send').on('click', function(){
        $('#complaint-popup').modal('show');
    });
    
    $('#closeComplaint').on('click', function(){
        $('#complaint-popup').modal('hide');
    });
    
    $('#okComplaint').on('click', function (e) {
            e.preventDefault();
            var to_user = $('#user_id').val();
            var text = $('#textComplaint').val();
            var type = $('input[name=complaint-reason]:checked', '#complaint_reason').val();
            var block = $('input[name=blockUser]:checked', '#block-user-module').val();
            console.log(to_user);
            $.post('/complaints/add-complaint/', {
                user_id: to_user,
                text: text,
                type: type,
                block: block,
                csrfmiddlewaretoken: getCookie('csrftoken'),
            }, function (data) {
                 $("#complaint-popup").hide();
                if (data.status == 'ok') {
                    if (data.blocked == 1) {
                        $("#block-user").text("{{ unblock }}");
                        $("#block-user").attr('data-block', 'unblock');
                    }
                }
            });
        });


/*    
    function check_login_url(xhr) {
                var login_url = '{% url "accounts:login" %}' + "?next={% url 'user_page' profile.slug %}";
                if (xhr.responseText.indexOf('login') != -1 ) {
                    // Check if response doesn't contain redirect to login. If it contains - redirect to login window
                    window.location = login_url;
                }
            }

            // Subscribe action scripts
            {% trans 'Unfollow' as unfollow %}
            {% trans 'Follow' as follow %}

            if ($('#followLink').data('action') == 'remove') {
                $('#followLink').text('{{ unfollow }}');
                $('#followLink').toggleClass('alternate_color');
            } else {
                $('#followLink').text('{{ follow }}');
                $('#followLink').toggleClass('alternate_color');
            }
            $('#followLink').click(function(e){
                e.preventDefault();
                $.post('{% url "accounts:add_subscriber" %}',
                    {
                        pk: $(this).data('id'),
                        action: $(this).data('action')
                    },
                    function (data, status, xhr) {
                        check_login_url(xhr);
                        if (data['status'] == 'ok') {
                            var previous_action = $('#followLink').data('action');
                            var count_previous = parseInt($('#followers').text());
                            $('#followLink').data('action', previous_action == 'add' ? 'remove' : 'add');
                            if (previous_action == 'add') {
                                $('#followLink').text('{{ unfollow }}');
                                $('#followLink').toggleClass('alternate_color');
                                $('#followers').text(count_previous + 1);
                            } else {
                                $('#followLink').text('{{ follow }}');
                                $('#followLink').toggleClass('alternate_color');
                                $('#followers').text(count_previous - 1);
                            }
                        }
                    }
                );
            });

        {% trans 'Unblock' as unblock %}
        {% trans 'Block' as block_translated %}
        // Create complaint and sent AJAX call
        $('#okComplaint').on('click', function (e) {
            e.preventDefault();
            var to_user = '{{ profile.user.pk }}';
            var text = $('#textComplaint').val();
            var type = $('input[name=complaint-reason]:checked', '#complaint_reason').val();
            var block = $('input[name=blockUser]:checked', '#block-user-module').val();
            $.post('{% url 'complaints:add_complaint' %}', {
                user_id: to_user,
                text: text,
                type: type,
                block: block
            }, function (data) {
                 $(".complaint-popup, .overlay").hide();
                if (data.status == 'ok') {
                    if (data.blocked == 1) {
                        $("#block-user").text("{{ unblock }}");
                        $("#block-user").attr('data-block', 'unblock');
                    }
                }
            });
        });

        $("#block-user").click(function(){
            // If user is blocked - sent request to unblock
            if ($(this).data('block') == 'unblock') {
                var to_user = '{{ profile.user.pk }}';
                $.post('{% url "complaints:remove_from_block" %}', {
                    user_id: to_user
                }, function (data) {
                    if (data.status == 'ok') {
                        $("#block-user").text("{{ block_translated }}");
                        $("#block-user").attr('data-block', 'block');
                    }
                })
            } else  {
                $(this).next().show();
            }
        });

		$(".primary-stars .left, .primary-stars .right").hover(
                function(){
                    if (!$(".primary-stars .left, .primary-stars .right").hasClass("selected")) {
                        $(this).addClass("full");
                        $(this).prevAll().addClass("full");
                    }
                }, function() {
                    if (!$(".primary-stars .left, .primary-stars .right").hasClass("selected")) {
                        $(this).removeClass("full");
                        $(this).prevAll().removeClass("full");
                    }
                }
        );
        document.getElementById("file").onchange = function () {
            var input = document.getElementById("fileInputBanner");
            input.innerHTML=this.value;
        };
        document.getElementById("uploadFileLogin").onchange = function () {
            var input = document.getElementById("fileInputLogin");
            input.innerHTML=this.value;
        };

        {% if request.user.pk == profile.user.pk %}
            $(".retailer-logo-wrapper").click(function() {
                $(".upload-photo-popup-wrapper.logo-module, .overlay").show();
            });
        {% endif %}

        $(".upload-custom-banner-popup .close").click(function(){
            $(".upload-custom-banner-popup, .overlay").hide();
        });
        $(".upload-custom-logo-popup .close").click(function(){
            $(".upload-custom-logo-popup, .overlay").hide();
        });

        {% if request.user.pk == profile.user.pk %}
            $(".image-holder").click(function() {
                $(".upload-photo-popup-wrapper.banner-module, .overlay").show();
            });
        {% endif %}

        $(".complaint").click(function() {
            $(".complaint-popup, .overlay").show();
            $('html, body').animate({scrollTop: 0 },600);
        });
        $(".complaint-popup .close").click(function() {
            $(".complaint-popup, .overlay").hide();
        });
        $(".logo-module .uploadIt").click(function(){
            $(".upload-photo-popup-wrapper.logo-module").hide();
            $(".upload-custom-logo-popup").show();
        });
        $(".banner-module .uploadIt").click(function(){
            $(".banner-module").hide();
			$(".upload-custom-banner-popup").show();
		});

        $(".primary-stars .left, .primary-stars .right").click(
                function(){
                    $(".primary-stars .left, .primary-stars .right").removeClass("selected full");
                    $(this).addClass("selected");
                    $(this).prevAll().addClass("selected");
                }
        );

        $deliveryBlock = $('.top-pin-container');

        $('.block-delivery .row.center').click(function(){
            $('.block-delivery').append($deliveryBlock)
        });

        $('.visibility-eye').click(function(){
            $(this).toggleClass('active');
	        $('.additional-stats').toggleClass('show');
	        $('.category-container-tab2').masonry({
                // указываем элемент-контейнер в котором расположены блоки для динамической верстки
	            itemSelector: '#category',
	            // указываем класс элемента являющегося блоком в нашей сетке
	            singleMode: true,
	            // true - если у вас все блоки одинаковой ширины
	            isResizable: true,
	            // перестраивает блоки при изменении размеров окна
	            isAnimated: true,
	            // анимируем перестроение блоков
	            animationOptions: {
                    queue: true,
                    duration: 500
                }
	            // опции анимации - очередь и продолжительность анимации
            });

            $('.category-container-tab3').masonry({
                // указываем элемент-контейнер в котором расположены блоки для динамической верстки
	            itemSelector: '#category',
	            // указываем класс элемента являющегося блоком в нашей сетке
	            singleMode: true,
	            // true - если у вас все блоки одинаковой ширины
	            isResizable: true,
	            // перестраивает блоки при изменении размеров окна
	            isAnimated: true,
	            // анимируем перестроение блоков
	            animationOptions: {
                    queue: true,
                    duration: 500
                }
                // опции анимации - очередь и продолжительность анимации
            });
            $('.category-container-tab1').masonry({
                // указываем элемент-контейнер в котором расположены блоки для динамической верстки
	            itemSelector: '#category',
	            // указываем класс элемента являющегося блоком в нашей сетке
	            singleMode: true,
	            // true - если у вас все блоки одинаковой ширины
	            isResizable: true,
	            // перестраивает блоки при изменении размеров окна
	            isAnimated: true,
	            // анимируем перестроение блоков
	            animationOptions: {
                    queue: true,
                    duration: 500
                }
                // опции анимации - очередь и продолжительность анимации
	        });
	    });

        position_left = $('#wrapper').css('margin-left').replace("px", "");
	    position_left -=50;
	    $('.visibility-eye').css('margin-left', position_left);

	    window.onresize = function(){
            position_left = $('#wrapper').css('margin-left').replace("px", "");
            position_left -=50;
            $('.visibility-eye').css('margin-left', position_left);
        };

        $('#wrapper').hover(
                function(){
                    $('.big-cross, .big-cross-right').hide()}, function(){
                    $('.big-cross, .big-cross-right').show()
                });

        $('.button-icons .green-buttons').click(function(){
            $(this).removeClass('active');
            $('.orange-buttons').addClass('active');
            $('.discount').css("background", "#bdfe42");
            $('.hidden-price-panel .pay').css("background", "#ff6600").text("{% trans 'Edit' %}");
        });

        $('.button-icons .orange-buttons').click(function(){
            $(this).removeClass('active');
            $('.green-buttons').addClass('active');
            $('.discount').css("background", "#ff6600");
            $('.hidden-price-panel .pay').css("background", "#bdfe42").text("{% trans 'Checkout' %}");
        });

        $(".module-toggle").click(function(){
            console.log("module click");
            $(this).next().toggleClass("active");
        });

        $('.upload-photo-popup .close').click(function(){
            $('.upload-photo-popup-wrapper, .overlay').hide();
        });

        $(".infinity").click(function(){
            
	    });

        $(".text-review-section .cta").click(function(){
            $(".reviews-popup-wrapper, .overlay").show();
            $('html, body').animate({scrollTop: 0 },600);
        });

        $(".reviews-popup-wrapper .close").click(function(){
            $(".reviews-popup-wrapper, .overlay").hide();
        });

        $('.promotional-banner').slick({
            infinite: true,
            autoplay:true,
            arrows:false,
		    autoplaySpeed:12000,
		    draggable:false
	    });

	    $('.search-modal').click(function (){
            $('.search-box').show();
            $(this).parents('header').hide();
	    });

        $('.img-search').click(function (){
            $(this).parent().hide();
		    $('.blackheader.green').show();
	    });

	    $('input[class="search"]').keypress(function (e) {
            var key = e.which;
            if(key == 13)  // the enter key code
	        {
	            $(this).parent().hide();
	            $('.blackheader.green').show();
	        }
	    });

	    $('.dress-section').show();

	    $('.category-goods p').click(function(ev){
            ev.preventDefault();
		    var ID = $(this).attr('id'),
		    openSection = "."+ ID + "-section",
		    allCats = $('.category-goods p')
		    allCats.removeClass('highlighted-link')
		    $(this).addClass('highlighted-link')

		    $('.block-subcategory').find('.hidden-goods').hide();
		    $('.block-subcategory').find(openSection).show();
        });

        $('#your-own-category').click(function() {
            $('.hidden-new-category').show();
            $('.goods-img').click(function(ev){
                ev.preventDefault();
			    ev.stopPropagation();
			    var theText = $(this).find('.selected-category');
			    $('#your-own-category').val($(theText).text());
			    $('.hidden-new-category').hide();
		    });
	    });

	    $('.hidden-new-category').click(function(){
            $(this).hide();
		    $('.goods-img').click(function(ev){
                ev.preventDefault();
                ev.stopPropagation();
            });
        });

	    $('.hidden-goods p').click(function(ev){
            ev.preventDefault();
            $('.hidden-goods p').removeClass();
            $(this).addClass('highlighted-link');
        });
        function validateNumber(event) {
            var key = window.event ? event.keyCode : event.which;
            if (event.keyCode == 8 || event.keyCode == 46 || event.keyCode == 37 || event.keyCode == 39) {
                return true;
            } else if ( key < 48 || key > 57 ) {
                return false;
            } else return true;
        };

        $('.number-input, .validate-me').keypress(validateNumber);
        $('.filter-toggle').click(function(){
            $('#slider').slider();
            $(this).next().show();
            $(this).hide();
            $('.overlay').show();
        });

	    var the_height = $(document).height();
	    $('#open-category').click(function(){
            $('.big-hidden-block').toggleClass('show');
            //$('html, body').animate({scrollTop: 0},600);
            var n = the_height
            //$('.filter').toggleClass('filter-open')
            $('.filter').css("bottom", '0vh');
	    });

	    $('.black').click(function() {
            $(this).toggleClass('active');
		    $(this).next().toggle();
		    //$('html, body').animate({scrollTop: $(document).height() },600);
		    var filter_height = $('.filter').outerHeight();
            if (filter_height > $(window).outerHeight()) {
                $('html, body').animate({scrollTop: $(document).height() },600);
                setTimeout(function(){
                    $('.filter').addClass('filter-open')
                }, 500);
            };
        });

        $('.filter-toggle-inner, .closeAll').click(function() {
            $('.filter').hide();
		    $('.overlay').hide();
		    $('.filter-toggle').show();
		    $('.filter').removeClass('filter-open');
		    $('.big-hidden-block').removeClass('show');
		    $('.black').removeClass("active");
		    $('.black').next().hide();
        });

        $('.info').click(function() {
            $('#slider-popup-1').slick();
            $('#slider-popup-2').slick();
            $('#slider-popup-3').slick();
	    });*/
});