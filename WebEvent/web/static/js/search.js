// search tên sự kiện, hiển thị danh sách gợi ý 
document.addEventListener("DOMContentLoaded", function () {
    let searchInput = document.getElementById("searchInput");
    let suggestionsBox = document.getElementById("suggestions");

    function truncateText(text, maxLength) {
        return text.length > maxLength ? text.substring(0, maxLength) + "..." : text;
    }

    searchInput.addEventListener("input", function () {
        let query = this.value.trim();
        if (query.length > 1) {
            fetch(`/search?q=${query}&ajax=1`)
                .then(response => response.json())
                .then(data => {
                    suggestionsBox.innerHTML = "";
                    if (data.length) {
                        data.forEach(event => {
                            let item = document.createElement("li");
                            item.className = "dropdown-item suggestion-item";
                            item.innerHTML = `
                                <strong>${truncateText(event.name, 20)}</strong><br>
                                <small class="text-muted">${truncateText(event.description, 40)}</small>
                            `;
                            item.addEventListener("click", function () {
                                window.location.href = `/event/detail/${event.id}/`;
                            });
                            suggestionsBox.appendChild(item);
                        });
                        suggestionsBox.style.display = "block";
                    } else {
                        suggestionsBox.innerHTML = '<li class="dropdown-item text-muted">Không có kết quả tìm kiếm nào.</li>';
                        suggestionsBox.style.display = "block";
                    }
                });
        } else {
            suggestionsBox.style.display = "none";
        }
    });

    document.addEventListener("click", function (e) {
        if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
            suggestionsBox.style.display = "none";
        }
    });
});