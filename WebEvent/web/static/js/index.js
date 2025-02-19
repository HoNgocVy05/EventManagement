//cuộn
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener("click", function (e) {
            let targetHref = this.getAttribute("href");
            if (targetHref.startsWith("#")) {
                e.preventDefault();
                let targetId = targetHref.substring(1); 
                let targetElement = document.getElementById(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: "smooth" });
                }
            }
        });
    });
});