function calculateTotal() {
    let price = parseFloat(document.getElementById("ticketPrice").value);
    let quantity = parseInt(document.getElementById("quantity").value);
    let total = price * quantity;
    document.getElementById("totalPrice").value = total.toLocaleString() + " VNĐ";
}
function changeQuantity(value) {
    let quantityInput = document.getElementById("quantity");
    let currentValue = parseInt(quantityInput.value);
    let maxTickets = parseInt(quantityInput.max);
    
    if (currentValue + value >= 1 && currentValue + value <= maxTickets) {
        quantityInput.value = currentValue + value;
    }
}