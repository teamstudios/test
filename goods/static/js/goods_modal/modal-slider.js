	$(document).ready(function() {
		
		var imgPath = $('#modal-slider-button li:first-child #mini-thumbs-modal-slider img').parent().attr('href');
		$('#modal-slider-button li:first-child #mini-thumbs-modal-slider img').parent().css('border','1px solid #272727');
		$('#modal-slider-button li:first-child #mini-thumbs-modal-slider img').parent().css('padding','0px');
		$('#big-main-modal-slider').attr('src', imgPath);

		
		$('#mini-thumbs-modal-slider img').parent().bind('click',function(e) {
			e.preventDefault();
			$('#mini-thumbs-modal-slider img').parent().css('border','0px solid #272727');
			$('#mini-thumbs-modal-slider img').parent().css('padding','1px');
			var imgPath = $(this).attr('href');
			$(this).css('border','1px solid #272727');
			$(this).css('padding','0px');
			$('#big-main-modal-slider').attr('src', imgPath);
		});

	}); //Конец ready