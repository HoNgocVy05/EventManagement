// Tìm nhà tài trợ dựa vào mail
document.addEventListener("DOMContentLoaded", function () {
    let emailInput = document.getElementById("sponsor_email");
    let nameInput = document.getElementById("sponsor_name");
    let checkSponsorUrl = emailInput.getAttribute("data-url");

    emailInput.addEventListener("input", function () {
        let email = emailInput.value.trim();
        if (email.length > 5) {
            fetch(checkSponsorUrl + "?email=" + encodeURIComponent(email))
                .then(response => response.json())
                .then(data => {
                    nameInput.value = data.exists ? data.name : "Không tìm thấy nhà tài trợ";
                })
                .catch(error => console.error("Lỗi:", error));
        } else {
            nameInput.value = "";
        }
    });
});
