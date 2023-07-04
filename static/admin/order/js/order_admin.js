(function($) {
  $(document).ready(function() {
      var showDescriptionField = $('#id_show_description');
      var descriptionField = $('#id_description');

      function toggleDescriptionField() {
          if (showDescriptionField.is(':checked')) {
              descriptionField.closest('.form-row').show();
          } else {
              descriptionField.closest('.form-row').hide();
          }
      }

      toggleDescriptionField();

      showDescriptionField.change(function() {
          toggleDescriptionField();
      });
  });
})(django.jQuery);