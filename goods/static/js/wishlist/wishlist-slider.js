	$(document).ready(function() {
		
		var imgPath = $('#wishlist-slider-button li:first-child #mini-thumbs-wishlist-slider img').parent().attr('href');
		$('#wishlist-slider-button li:first-child #mini-thumbs-wishlist-slider img').parent().css('border','1px solid #272727');
		$('#wishlist-slider-button li:first-child #mini-thumbs-wishlist-slider img').parent().css('padding','0px');
		$('#big-main-wishlist-slider').attr('src', imgPath);

		
		$('#mini-thumbs-wishlist-slider img').parent().bind('click',function(e) {
			e.preventDefault();
			$('#mini-thumbs-wishlist-slider img').parent().css('border','0px solid #272727');
			$('#mini-thumbs-wishlist-slider img').parent().css('padding','1px');
			var imgPath = $(this).attr('href');
			$(this).css('border','1px solid #272727');
			$(this).css('padding','0px');
			$('#big-main-wishlist-slider').attr('src', imgPath);
		});

	}); //Конец ready