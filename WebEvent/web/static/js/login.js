function showPassword() {
    var x = document.getElementById("pw-input");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
}

$(document).ready(function() {
  $('.toggle-tickets').click(function() {
      var target = $(this).data('bs-target');
      $(target).stop(true, true).slideToggle(300);
  });
});