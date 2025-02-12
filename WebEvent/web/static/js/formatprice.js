//enter price
document.addEventListener("DOMContentLoaded", function () {
    let priceInput = document.getElementById("eventPrice");
    function formatCurrency(value) {
        value = value.replace(/\D/g, "");
        if (value) {
            return new Intl.NumberFormat("en-US").format(value) + " VND";
        }
        return "";
    }
    priceInput.addEventListener("input", function () {
        let rawValue = priceInput.value.replace(/\D/g, "");
        priceInput.value = formatCurrency(rawValue);
    });
    if (priceInput.value) {
        priceInput.value = formatCurrency(priceInput.value);
    }
});

window.onload = function() {
    // Kiểm tra trang hiện tại để xử lý
    if (document.getElementById('ticketPriceInput')) {
        // buyticket page
        var price = document.getElementById('ticketPriceInput').getAttribute('data-price');
        var formattedPrice = parseInt(price).toLocaleString('en-US') + ' VND';
        document.getElementById('ticketPriceInput').value = formattedPrice;
    } 
    
    if (document.getElementById('ticketPriceText')) {
        // eventdetail page
        var priceElement = document.getElementById('ticketPriceText');
        var price = parseInt(priceElement.textContent.replace(',', ''));
        var formattedPrice = price.toLocaleString('en-US') + ' VND';
        priceElement.textContent = formattedPrice;
    }
};

