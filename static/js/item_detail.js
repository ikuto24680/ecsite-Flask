/**
 * 
 */
"use-strict";

$(function() {

	calcPrice();

	$(".size_radio").on("change", function() {
		calcPrice();
	});

	$(".topping").click(function() {
		calcPrice();
	});

	$("#quantity").on("change", function() {
		calcPrice();
	});

	function calcPrice() {
		let normalPrice = 0;
		let toppingPrice = 0;
		let countChecked = $("#topping:checked").length;
		let quantity = Number($("#quantity").val());
		if ($(".size_radio:checked").val() === "M") {
			normalPrice = Number($("#priceM").val());
			toppingPrice = 200 * countChecked;
		} else {
			normalPrice = Number($("#priceL").val());
			toppingPrice = 300 * countChecked;
		}
		let totalPrice = (normalPrice + toppingPrice) * quantity;
		$("#show-total-price").text(totalPrice.toLocaleString());
	}
});