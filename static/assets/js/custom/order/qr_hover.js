
<script>
  document.addEventListener("DOMContentLoaded", function() {
    // Add an event listener to the QR code
    $(".qr-code").on("mouseenter", function() {
      var orderNumber = $(this).data("order-number");
      var customerName = $(this).data("customer-name");
      var orderDate = $(this).data("order-date");
      var deadline = $(this).data("deadline");
  
      // Display the order details in a tooltip or any other desired way
      var tooltipContent = "Order Number: " + orderNumber + "<br>"
                          + "Customer Name: " + customerName + "<br>"
                          + "Order Date: " + orderDate + "<br>"
                          + "Deadline: " + deadline;
  
      $(this).attr("title", tooltipContent);
    });
  });
</script>