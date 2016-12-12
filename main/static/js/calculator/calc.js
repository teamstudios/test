$(document).ready(function() {

	// Запрет на ввод букв >>

	$('.nonnumb').bind("change keyup input click", function() {
		if (this.value.match(/[^0-9]/g)) {
			this.value = this.value.replace(/[^0-9]/g, '');
		}
	});

	// Переключение вкладок

		$('#bbtn1').click(function(){
			$('#bbtn1').addClass('bbtn-active');
			$('#bbtn2').removeClass('bbtn-active');
			$('#bbtn3').removeClass('bbtn-active');
			$('#calc1').show();
			$('#calc2').hide();
			$('#calc3').hide();
			$('#btnStart1').show();
			$('#btnStart2').hide();
			$('#btnStart3').hide();
			$('.iptclear').val(0);
			$('#commission').html('0');
			$('#return-sale').html('0');
			$('#main-sale').html('0');
		});
		$('#bbtn2').click(function(){
			$('#bbtn1').removeClass('bbtn-active');
			$('#bbtn2').addClass('bbtn-active');
			$('#bbtn3').removeClass('bbtn-active');
			$('#calc1').hide();
			$('#calc2').show();
			$('#calc3').hide();
			$('#btnStart1').hide();
			$('#btnStart2').show();
			$('#btnStart3').hide();
			$('.iptclear').val(0);
			$('#commission').html('0');
			$('#return-sale').html('0');
			$('#main-sale').html('0');
		});
		$('#bbtn3').click(function(){
			$('#bbtn1').removeClass('bbtn-active');
			$('#bbtn2').removeClass('bbtn-active');
			$('#bbtn3').addClass('bbtn-active');
			$('#calc1').hide();
			$('#calc2').hide();
			$('#calc3').show();
			$('#btnStart1').hide();
			$('#btnStart2').hide();
			$('#btnStart3').show();
			$('.iptclear').val(0);
			$('#commission').html('0');
			$('#return-sale').html('0');
			$('#main-sale').html('0');
		});
		

	// Расчет калькулятора

	$('#btnStart1').click(function(){
		var firstSale = $('#firstSale').val();
		var delivery = $('#delivery').val();

		if(firstSale != '' && firstSale != 0){

			var mainSale = parseInt(firstSale)+parseInt(delivery);
			$('#main-sale').html(mainSale);
			/*
			if(mainSale<100000){
				if(mainSale<=2499){
					var commission = mainSale/100*4.5;
					$('#commission').html(commission);
				}
				else if(mainSale<=4999){
					var commission = mainSale/100*3.9;
					$('#commission').html(commission);
				}
				else if(mainSale<=9999){
					var commission = mainSale/100*3.4;
					$('#commission').html(commission);
				}
				else if(mainSale<=24999){
					var commission = mainSale/100*2.9;
					$('#commission').html(commission);
				}
				else if(mainSale<=49999){
					var commission = mainSale/100*2.7;
					$('#commission').html(commission);
				}
				else if(mainSale<=99999){
					var commission = mainSale/100*2.4;
					$('#commission').html(commission);
				}
			}else{
				var commission = mainSale/100*1.9;
				$('#commission').html(commission);
			}*/
			var commission = mainSale/100*7;
			$('#commission').html(commission);

			var returnSale=mainSale-commission;
			$('#return-sale').html(returnSale);
		} else {
			alert('Вы должны указать цену!');
		}
	});



	$('#btnStart2').click(function(){
		var secondSale1 = $('#secondSale1').val();
		var secondSale2 = $('#secondSale2').val();
		var secondSale3 = $('#secondSale3').val();

		if(secondSale3 != '' && secondSale3 != 0){
			var secondSale = secondSale3;
		} else if(secondSale2 != '' && secondSale2 != 0) {
			var secondSale = secondSale2;
		} else if(secondSale1 != '' && secondSale1 != 0) {
			var secondSale = secondSale1;
		} else {
			var secondSale = '';
		}

		var delivery = $('#delivery').val();

		if(secondSale != ''){

			var mainSale = parseInt(secondSale)+parseInt(delivery);
			$('#main-sale').html(mainSale);
			/*
			if(mainSale<100000){
				if(mainSale<=2499){
					var commission = mainSale/100*4.5;
					$('#commission').html(commission);
				}
				else if(mainSale<=4999){
					var commission = mainSale/100*3.9;
					$('#commission').html(commission);
				}
				else if(mainSale<=9999){
					var commission = mainSale/100*3.4;
					$('#commission').html(commission);
				}
				else if(mainSale<=24999){
					var commission = mainSale/100*2.9;
					$('#commission').html(commission);
				}
				else if(mainSale<=49999){
					var commission = mainSale/100*2.7;
					$('#commission').html(commission);
				}
				else if(mainSale<=99999){
					var commission = mainSale/100*2.4;
					$('#commission').html(commission);
				}
			}else{
				var commission = mainSale/100*1.9;
				$('#commission').html(commission);
			}
			*/

			var commission = mainSale/100*7;
			$('#commission').html(commission);

			var returnSale=mainSale-commission;
			$('#return-sale').html(returnSale);
		} else {
			alert('Вы должны указать цену!');
		}
	});


	$('#btnStart3').click(function(){
		var thirdSale1 = $('#thirdSale1').val();
		var thirdSale2 = $('#thirdSale2').val();


		if(thirdSale2 != '' && thirdSale2 != 0){
			var thirdSale = thirdSale2;
		} else if(thirdSale1 != '' && thirdSale1 != 0) {
			var thirdSale = thirdSale1;
		}else {
			var thirdSale = '';
		}

		var delivery = $('#delivery').val();

		if(thirdSale != ''){

			var mainSale = parseInt(thirdSale)+parseInt(delivery);
			$('#main-sale').html(mainSale);
			/*
			if(mainSale<100000){
				if(mainSale<=2499){
					var commission = mainSale/100*4.5;
					$('#commission').html(commission);
				}
				else if(mainSale<=4999){
					var commission = mainSale/100*3.9;
					$('#commission').html(commission);
				}
				else if(mainSale<=9999){
					var commission = mainSale/100*3.4;
					$('#commission').html(commission);
				}
				else if(mainSale<=24999){
					var commission = mainSale/100*2.9;
					$('#commission').html(commission);
				}
				else if(mainSale<=49999){
					var commission = mainSale/100*2.7;
					$('#commission').html(commission);
				}
				else if(mainSale<=99999){
					var commission = mainSale/100*2.4;
					$('#commission').html(commission);
				}
			}else{
				var commission = mainSale/100*1.9;
				$('#commission').html(commission);
			}*/
			var commission = mainSale/100*7;
			$('#commission').html(commission);

			var returnSale=mainSale-commission;
			$('#return-sale').html(returnSale);
		} else {
			alert('Вы должны указать цену!');
		}
	});


	$('#resetbtn').click(function(){
		$('.iptclear').val(0);
		$('#commission').html('0');
		$('#return-sale').html('0');
		$('#main-sale').html('0');
	});
});