$(document).ready(function() {

// Определяем первую картинку и включаем её

	$('.slider').each(function() {
		var urlBigImg = $(this).find('ul li:first a').attr('href');
		$(this).find('ul li:first a').parent().parent().siblings('img').attr('src', urlBigImg);
		$(this).find('ul li:first').addClass('active');
	});

// Переключатель картинок

	$('.slider ul li a').bind('click', function(e) {
		e.preventDefault();
		$(this).parent().parent().parent().find('ul li').removeClass('active');
		$(this).parent().addClass('active');
		var urlBigImg = $(this).attr('href');
		$(this).parent().parent().siblings('img').attr('src', urlBigImg);
	});

}); //End Ready