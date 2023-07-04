(function ($) {
  $(document).ready(function () {
    $(document).on(
      "change",
      ".dynamic-workorderservice .field-service select",
      function () {
        var serviceId = $(this).val();
        var priceForWork = $(this)
          .find("option:selected")
          .data("price-for-work");
        var priceField = $(this)
          .closest(".dynamic-workorderservice")
          .find(".field-price input");

        if (priceField.val() === "0.00") {
          priceField.val(priceForWork);
        }
      }
    );
  });
})(django.jQuery);
