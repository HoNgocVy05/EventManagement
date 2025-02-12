//Tính tổng tiền vé
function calculateTotal() {
    let price = parseFloat(document.getElementById("ticketPriceInput").getAttribute("data-price")) || 0;
    let quantity = parseInt(document.getElementById("quantity").value) || 0;
    let total = price * quantity;
    document.getElementById("totalPrice").value = total.toLocaleString("en-US") + " VND";
}
//tùy chỉnh số lượng vé
function changeQuantity(value) {
    let quantityInput = document.getElementById("quantity");
    let currentValue = parseInt(quantityInput.value);
    let maxTickets = parseInt(quantityInput.max);
    
    if (currentValue + value >= 1 && currentValue + value <= maxTickets) {
        quantityInput.value = currentValue + value;
    }
}
