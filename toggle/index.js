$(document).ready(() => {
  $(".toggle-btn").click(function () {
    var cardId = $(this).data("target");
    var card = $("#" + cardId);

    if (card.is(":visible")) {
      card.hide(300);
      $(this).text($(this).data("original-text"));
    } else {
      card.show(300);
      $(this).text("Hide");
    }

    // card.toggle(300); // display

    // card.fadeToggle();  // opacity

    // card.slideToggle(); // height
  });
});
