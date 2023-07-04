(function($) {
  $(document).ready(function() {
    // Добавляем обработчик события изменения значения поля 'service' в инлайн форме 'WorkOrderService'
    $('.workorderservice-form select[name$="service"]').on('change', function() {
      var serviceSelect = $(this);
      var priceField = serviceSelect.closest('.workorderservice-form').find('input[name$="price"]');

      // Получаем выбранное значение поля 'service'
      var selectedService = serviceSelect.val();

      // Отправляем AJAX-запрос на сервер для получения значения 'price_for_work' по выбранному 'service'
      $.ajax({
        url: '/get_price_for_work/',
        data: {
          service: selectedService
        },
        dataType: 'json',
        success: function(data) {
          // Устанавливаем значение 'price_for_work' в поле 'price'
          priceField.val(data.price_for_work);
        },
        error: function(xhr, status, error) {
          console.log('Error:', error);
        }
      });
    });
  });
})(django.jQuery);

  