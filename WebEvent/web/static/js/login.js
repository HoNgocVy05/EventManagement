function showPassword() {
    var x = document.getElementById("pw-input");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
}