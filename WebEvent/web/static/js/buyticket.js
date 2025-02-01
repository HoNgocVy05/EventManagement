function calculateTotal() {
    let price = parseFloat(document.getElementById("ticketPrice").value);
    let quantity = parseInt(document.getElementById("quantity").value);
    let total = price * quantity;
    document.getElementById("totalPrice").value = total.toLocaleString() + " VNĐ";
}
