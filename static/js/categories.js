	/* global $ */
// Helper function to redirect on ogin url if ajax view require login
        function check_login_url(xhr) {
            var login_url = '{% url "accounts:login" %}' + "?next={% url 'goods:goods_modal' good.pk %}";
            if (xhr.responseURL.indexOf('login') != -1 ) {
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



$(window).load(function(){
	var options = {
        autoResize: true,
        itemWidth: 180,
	    direction: 'left',
	    align: 'left',
	    container: $('#category-container'),
	    offset: 7,
    };
    var handler = $('#category-container');
    var page = 1;
    var empty_page = false;
    var block_request = false;
    var page_type = $('#page_type').val();
    var search_request = $('#requestVal').val();
    $('#lazy_more').click(function (e) {
        e.preventDefault();
        if (empty_page == false && block_request == false) {
            block_request = true;
            page += 1;
        //Check page identifier if and define url to lazy load 
            if (page_type == 'search'){
                var query = '?query=' + search_request + '&page=' + page;
            } else {
                var query = '?filter=1&' + search_request+ '&page=' + page; //was {{search_request|safe}}
            }
            console.log(query);
            $.get(query, function (data) {
                if (data == '') {
                    empty_page = true;
                } else {
                    block_request = false;
                // Wrap data to work with masonry plugin
                    var $content = $(data);
                    $('#category-container').append($content);
                }
            });
        }
        setTimeout(function() {
            handler.wookmarkInstance.initItems();
            handler.wookmarkInstance.layout(true);;
        }, 200);
    });
    handler.wookmark(options);
});
	
$(document).ready(function() {
    $(".fancybox").fancybox({
            helpers: {
                overlay: {
                    css: {
                        'background': 'rgba(00, 00, 00, 0.9)'
                    }
                }
            },
            tpl: {
                closeBtn: '<a title="Close" class="fancybox-item fancybox-close mClose" href="javascript:;"></a>',
                next: '<a title="Next" class="fancybox-nav fancybox-next mNext" href="javascript:;"></a>',
                prev: '<a title="Previous" class="fancybox-nav fancybox-prev mPrev" href="javascript:;"></a>'
            },
            loop: true,
            type: 'iframe',
            autoSize : true,
            width: 960,
            fitToView: true, // set the specific size without scaling to the view port
            openEffect: 'none',
            closeEffect: 'none',
            nextEffect: 'none',
            prevEffect: 'none',
            padding: 0,
            beforeShow: function(){
                $(".fancybox-skin").css("backgroundColor","transparent"); // Set inner container background color
            },
            afterShow: function () {
                console.log('go!!');
                if ($('#modal-like-button').data('action') == 'add') {
                    $('#modal-like-button').find( "i" );
                } else {
                    $('#modal-like-button').find( "i" ).addClass('red');
                }
                // Send AJAX to remove/add to users likes
                $('#modal-like-button').click(function (e) {
                    e.preventDefault();
                    console.log('like');
                    var previous_action = $('#modal-like-button').data('action');
                    $.post('{% url "goods:add_user_like" %}', {
                        pk: $(this).data('id'),
                        action: $(this).data('action')
                    },
                    function (data, status, xhr) {
                        check_login_url(xhr);
                        if (data['status'] == 'ok') {
                            $('#modal-like-button').data('action', previous_action == 'add' ? 'remove' : 'add');
                            if (previous_action == 'add') {
                                $('#modal-like-button').find( "i" ).addClass('red');
                                $('#modal-likes-block').append('<br>{% trans "You like this product" %}');
                            } else {
                                $('#modal-like-button').find( "i" ).removeClass('red');
                            }
                        }
                    });
                });

            // Wish button scripsts
                // Check action atribute and set image
                if ($('#modal-wish-button').data('action') == 'add') {
                    $('#modal-wish-button').css('background','url({% static "images/goods_modal/wish-icon.png" %}) no-repeat 19px 9px');
                } else {
                    $('#modal-wish-button').css('background','url({% static "images/goods_modal/wish-icon-pressed.png" %}) no-repeat 19px 9px');
                }
            // Send AJAX to remove/add to wish list
                $('#modal-wish-button').click(function(e){
                    e.preventDefault();
                    $.post('{% url "goods:add_to_wishlist" %}',
                        {
                            pk: $(this).data('id'),
                            action: $(this).data('action')
                        },
                        function (data, status, xhr) {
                            check_login_url(xhr);
                            if (xhr.responseURL.indexOf('login') != -1 ) {
                                // Check if response doesn't contain redirect to login. If it contains - redirect to login window#}
                                window.location = '{% url "accounts:login" %}' + "?next={% url 'goods:goods_modal' good.pk %}";
                            }
                            if (data['status'] == 'ok') {
                                var previous_action = $('#modal-wish-button').data('action');
                                $('#modal-wish-button').data('action', previous_action == 'add' ? 'remove' : 'add');
                                if (previous_action == 'add') {
                                    $('#modal-wish-button').css('background','url({% static "images/goods_modal/wish-icon-pressed.png" %}) no-repeat 19px 9px');
                                } else {
                                    $('#modal-wish-button').css('background','url({% static "images/goods_modal/wish-icon.png" %}) no-repeat 19px 9px');
                                }
                            }
                        }
                    );
                });
            }
            });

// Lazy load script
    var filterPostBody = {}; // Variable to store POST request parameters
    var deliveryBlock = $('.top-pin-container');
    $('.block-delivery .row.center').click(function(){
	    $('.block-delivery').append(deliveryBlock)
    });
	    
// Like button scripts
    // Check action atribute and set image
    
});
	    /*position_left = $('#wrapper').css('margin-left').replace("px", "");
	    position_left -=50
	    $('.visibility-eye').css('margin-left', position_left);
	     window.onresize = function(){
		    position_left = $('#wrapper').css('margin-left').replace("px", "");
	        position_left -=50;

	        $('.visibility-eye').css('margin-left', position_left);
	    };
	
	    $('#wrapper').hover(
		    function(){
	            $('.big-cross, .big-cross-right').hide()},
	        function(){
	            $('.big-cross, .big-cross-right').show()
	        }
	    );
	    $('.button-icons .green-buttons').click(function(){
		
		    $(this).removeClass('active');
		    $('.orange-buttons').addClass('active');
		
		    $('.discount').css("background", "#bdfe42");
		    $('.hidden-price-panel .pay').css("background", "#ff6600").text("Редактировать");
	    });
	    $('.button-icons .orange-buttons').click(function(){
		
		    $(this).removeClass('active');
		    $('.green-buttons').addClass('active');
		    $('.discount').css("background", "#ff6600");
		    $('.hidden-price-panel .pay').css("background", "#bdfe42").text("Оплатить");
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

		    $('.block-subcategory').find('.hidden-goods').hide()
		    $('.block-subcategory').find(openSection).show()
		
	    })
        $('#your-own-category').click(function() {
		    $('.hidden-new-category').show()

		    $('.goods-img').click(function(ev){
			    ev.preventDefault()
			    ev.stopPropagation()
			    var theText = $(this).find('.selected-category')
			    $('#your-own-category').val($(theText).text())
			    $('.hidden-new-category').hide()
		    })
	    })
	    $('.hidden-new-category').click(function(){
		    $(this).hide()
		    $('.goods-img').click(function(ev){
			    ev.preventDefault()
			    ev.stopPropagation()
		    })
	    })
	    $('.hidden-goods p').click(function(ev){
		    ev.preventDefault()
		    $('.hidden-goods p').removeClass()
		    $(this).addClass('highlighted-link')
	    })
	    function validateNumber(event) {
            var key = window.event ? event.keyCode : event.which;
            if (event.keyCode == 8 || event.keyCode == 46 || event.keyCode == 37 || event.keyCode == 39) {
                return true;
            }
            else if ( key < 48 || key > 57 ) {
                return false;
            }
            else return true;
        };
        $('.number-input, .validate-me').keypress(validateNumber);
        $('.filter-toggle').click(function(){
		    $('#slider').slider()
		    $(this).next().show()
		    $(this).hide()
		    $('.overlay').show()
	    })
	    var the_height = $(document).height()
	    $('#open-category').click(function(){
            $('.big-hidden-block').toggleClass('show')
            //$('html, body').animate({scrollTop: 0},600);

            var n = the_height
       
            //$('.filter').toggleClass('filter-open')
            $('.filter').css("bottom", '0vh')
	    })


	    $('.black').click(function() {
		    $(this).toggleClass('active')
		    $(this).next().toggle()
		    //$('html, body').animate({scrollTop: $(document).height() },600);
		    var filter_height = $('.filter').outerHeight()
            if (filter_height > $(window).outerHeight()) {
    	        $('html, body').animate({scrollTop: $(document).height() },600);
    	        setTimeout(function(){
			        $('.filter').addClass('filter-open')
			    }, 500);
            }
	    })
	    $('.filter-toggle-inner, .closeAll').click(function() {
		    $('.filter').hide()
		    $('.overlay').hide()
		    $('.filter-toggle').show()
		    $('.filter').removeClass('filter-open')
		    $('.big-hidden-block').removeClass('show')
		    $('.black').removeClass("active")
		    $('.black').next().hide()
	    })
	    $('.info').click(function() {
            $('#slider-popup-1').slick()
            $('#slider-popup-2').slick()
            $('#slider-popup-3').slick()
        });

        jQuery(document).ready(function(){
            $("#price-range").slider({
                range: true,
                min: 0,
                max: 1000000,
                values: [ 0, 1000000],
                slide: function( event, ui ) {
                    $(".from .input-costs").val(ui.values[ 0 ]);
                    $(".costs-end .input-costs").val(ui.values[ 1 ]);
                },
                // Added by Victor Yamchinov to sent AJAX request on stop
                stop: function (event, ui) {
                    filterPostBody.min_cost = ui.values[0];
                    filterPostBody.max_cost = ui.values[1];
                    console.log(ui.values[0]);
                    console.log(ui.values[1]);
                    $.post('{% url "goods:goods_filter" %}', filterPostBody,
                        function (data, status, xhr) {
                            $("#count_result").text(data['count']);
                        }
                    );
                },
                function(event, ui) {
                    $(".from .input-costs").val(ui.values[0]);
                    $(".costs-end .input-costs").val(ui.values[1]);
                }
            })

            $(".from .input-costs").change(function () {
                var value = $(this).val()
                $("#price-range").slider("values", 0, parseInt(value));
            });
            $(".costs-end .input-costs").change(function () {
                var value = $(this).val()
                $("#price-range").slider("values", 1, parseInt(value));
            });

            $('.ui-slider-handle').first().text("OТ")
            $('.ui-slider-handle').last().text("ДО")
            $('.clearAll').click(function(){
	            $('.filter input').val("")
	            $("#price-range").slider("values", 0, 0);
	            $("#price-range").slider("values", 1, 1000000);
                // reset requestObject
                filterPostBody = {};
                // Set finding object to 0
                $("#count_result").text(0);
            })
        });

        $('.input-costs').bind("change keyup input click", function() {
		    if (this.value.match(/[^0-9]/g)) {
			    this.value = this.value.replace(/[^0-9]/g, '');
		    }
	    });

        // AJAX filter functions


        function sendFilterAjaxPost(postBody) {
            $.post('{% url "goods:goods_filter" %}', postBody,
                function (data, status, xhr) {
                    $("#count_result").text(data['count']);
                }
            );
        }

        function tagFunctionCliked(tag_id) {
            // Get tag id and send AJAX request to filter
            var tag_id_attr = '#tag' + tag_id; // form tagid selector
            if ($(tag_id_attr).data('action') == 'add') {
                // if array doesn't exist - create it
                if (!Array.isArray(filterPostBody.tag_id)) {
                    filterPostBody.tag_id = [];
                }
                filterPostBody.tag_id.push(tag_id);
                // change css and action
                $(tag_id_attr).data('action', 'remove');
                $(tag_id_attr).css('color', '#b1fe00');
            } else {
                // Remove selected id from array
                filterPostBody.tag_id = $.grep(filterPostBody.tag_id, function (value) {
                    return value != tag_id;
                });
                $(tag_id_attr).data('action', 'add');
                $(tag_id_attr).css('color', '#000000');
            }
            sendFilterAjaxPost(filterPostBody);
        }

        function check_login_url(xhr) {
            var login_url = '{% url "accounts:login" %}' + "?next={% url 'goods:search' %}" + "?query={{ search_request }}";
            if (xhr.responseText.indexOf('login') != -1 ) {
                // Check if response doesn't contain redirect to login. If it contains - redirect to login window
                window.location = login_url;
            }
        }

        function addTagFunctionCliked() {
            // add tag
            var new_tag_name = $('#your-own-category').val();
            $.post('{% url "goods:add_new_tag" %}', {
                    tag_name: new_tag_name
                },
                function (data, status, xhr) {
                    // Check if user logged in
                    check_login_url(xhr);
                    if (data['status'] == 'ok') {
                        // if creation success append html with new tag link to div
                        $('#tagslist').append('<p><a href="#" onclick="tagFunctionCliked(' + data['id'] +')" data-action="add" id="tag' +
                                data['id'] + '">' + new_tag_name + '</a></p>');
                        $('#your-own-category').val('');
                    }
                }
            );
        }

        // Function to react on keyup event

        // Sent AJAX request on keyup event
        // TODO: Recreate to follow DRY
        $('#name_search_filter').keyup(function () {
            filterPostBody.name = $(this).val();
            sendFilterAjaxPost(filterPostBody);
        });

        $('#min_cost_filter').keyup(function () {
            filterPostBody.min_cost = $(this).val();
            sendFilterAjaxPost(filterPostBody);
        });

        $('#max_cost_filter').keyup(function () {
            filterPostBody.max_cost = $(this).val();
            sendFilterAjaxPost(filterPostBody);
        });

        $('#location_filter').keyup(function () {
            filterPostBody.location = $(this).val();
            sendFilterAjaxPost(filterPostBody);
        });

        $('#slider-popup-1').on('afterChange', function (event, slick, currentSlide) {
            filterPostBody.deal = $(slick.$slides.get(currentSlide)).data('deal');
            sendFilterAjaxPost(filterPostBody);
        });

        $('#slider-popup-2').on('afterChange', function (event, slick, currentSlide) {
            filterPostBody.state = $(slick.$slides.get(currentSlide)).data('state');
            sendFilterAjaxPost(filterPostBody);
        });

        $('#slider-popup-3').on('afterChange', function (event, slick, currentSlide) {
            filterPostBody.delivery_form = $(slick.$slides.get(currentSlide)).data('delivery');
            sendFilterAjaxPost(filterPostBody);
        });

        $('#cooperation_filter').keyup(function () {
            filterPostBody.cooperation = $(this).val();
            sendFilterAjaxPost(filterPostBody);
        });

        $('#trade_mark_filter').keyup(function () {
            filterPostBody.trade_mark = $(this).val();
            sendFilterAjaxPost(filterPostBody);
        });

        $('#model_filter').keyup(function () {
            filterPostBody.model = $(this).val();
            sendFilterAjaxPost(filterPostBody);
        });

        $('#material_filter').keyup(function () {
            filterPostBody.material = $(this).val();
            sendFilterAjaxPost(filterPostBody);
        });

        $('#size_filter').keyup(function () {
            filterPostBody.size = $(this).val();
            sendFilterAjaxPost(filterPostBody);
        });

        $('#color_filter').keyup(function () {
            filterPostBody.color = $(this).val();
            sendFilterAjaxPost(filterPostBody);
        });

        $('#weight_filter').keyup(function () {
            filterPostBody.weight = $(this).val();
            sendFilterAjaxPost(filterPostBody);
        });

        $('#equipment_filter').keyup(function () {
            filterPostBody.equipment = $(this).val();
            sendFilterAjaxPost(filterPostBody);
        });

        $('#vendor_filter').keyup(function () {
            filterPostBody.vendor = $(this).val();
            sendFilterAjaxPost(filterPostBody);
        });
    
        function redirectToFilterResults() {
            var recursiveEncoded = $.param(filterPostBody);
            // var recursiveDecoded = decodeURIComponent( $.param(filterPostBody));
            var filter_url = '{% url "goods:search" %}' + "?filter=1&" + recursiveEncoded;
            window.location = filter_url;
        }

        function filterByDealType(deal) {
            // Commented beacause masonry doesn't correctly work with filtering

            if (deal == {{ SALE }}) {
                var data_filter = '[data-deal-filter="' + {{ BUY_SELL }} +'"], [data-deal-filter="' + {{ AUCTION }} + '"]';
            }
            var els = Array.prototype.slice.call(document.querySelectorAll(data_filter));
                for (var i = 0; i < els.length; i++) {
                    $(els[i]).hide();
                }
            $('.category-container-tab2').masonry( 'reloadItems' );
            $('.category-container-tab2').masonry( 'layout' );
        }
        });*/