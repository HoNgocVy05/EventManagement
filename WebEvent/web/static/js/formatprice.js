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
//thay đổi format của giá tiền (ex: 100000 -> 100,000)
window.onload = function() {
    // Kiểm tra trang hiện tại để xử lý
    let priceInput = document.getElementById('ticketPriceInput');
    if (priceInput) {
        let price = priceInput.getAttribute('data-price');
        let formattedPrice = Number(price).toLocaleString('en-US') + ' VND';
        priceInput.value = formattedPrice;
    }

    let priceText = document.getElementById('ticketPriceText');
    if (priceText) {
        let price = priceText.textContent.replace(/,/g, '').trim();
        let formattedPrice = Number(price).toLocaleString('en-US') + ' VND';
        priceText.textContent = formattedPrice;
    }
};
