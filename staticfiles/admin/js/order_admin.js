(function($) {
    $(document).ready(function() {
      var $descriptionField = $('.checkbox-dependent');
      var $hasDescriptionCheckbox = $('input[name="has_description"]');
      
      function toggleDescriptionField() {
        if ($hasDescriptionCheckbox.is(':checked')) {
          $descriptionField.show();
        } else {
          $descriptionField.hide();
        }
      }
      
      $hasDescriptionCheckbox.on('change', toggleDescriptionField);
      toggleDescriptionField();
    });
  })(django.jQuery);
  