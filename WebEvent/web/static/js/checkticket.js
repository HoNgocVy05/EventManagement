document.addEventListener("DOMContentLoaded", function () {
    let checkTicketForm = document.getElementById("checkTicketForm");
    let checkResult = document.getElementById("checkResult");

    checkTicketForm.addEventListener("submit", function (event) {
        event.preventDefault();

        let qrCode = document.getElementById("ticketCode").value;

        fetch("{% url 'checkticket' event_id=event_id %}", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": "{{ csrf_token }}"
            },
            body: "qr_code=" + encodeURIComponent(qrCode)
        })
        .then(response => response.json())
        .then(data => {
            checkResult.innerHTML = data.message;
            checkResult.classList.remove("text-danger", "text-success");

            if (data.status === "success") {
                checkResult.classList.add("text-success");
            } else {
                checkResult.classList.add("text-danger");
            }
        })
        .catch(error => {
            checkResult.innerHTML = "Lỗi kết nối, vui lòng thử lại";
            checkResult.classList.add("text-danger");
        });
    });
});
