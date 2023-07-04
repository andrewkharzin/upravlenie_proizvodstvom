document.addEventListener("DOMContentLoaded", function() {
    var materialSelect = document.getElementById("id_material"); // Assuming the material select element has the id 'id_material'
    var stockQuantityInput = document.getElementById("id_stock_quantity"); // Assuming the stock quantity input element has the id 'id_stock_quantity'
  
    materialSelect.addEventListener("change", function() {
      var materialId = materialSelect.value;
  
      var xhr = new XMLHttpRequest();
      xhr.open("GET", "/get_stock_quantity/?material_id=" + materialId, true); // Replace with your server-side endpoint URL
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
          var response = JSON.parse(xhr.responseText);
          stockQuantityIndocument.addEventListener("DOMContentLoaded", function() {
            var materialSelect = document.getElementById("id_material"); // Assuming the material select element has the id 'id_material'
            var stockQuantityInput = document.getElementById("id_stock_quantity"); // Assuming the stock quantity input element has the id 'id_stock_quantity'
          
            materialSelect.addEventListener("change", function() {
              var materialId = materialSelect.value;
          
              var xhr = new XMLHttpRequest();
              xhr.open("GET", "/get_stock_quantity/?material_id=" + materialId, true); // Replace with your server-side endpoint URL
              xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                  var response = JSON.parse(xhr.responseText);
                  stockQuantityInput.value = response.stock_quantity;
                }
              };
              xhr.send();
            });
          });
          put.value = response.stock_quantity;
        }
      };
      xhr.send();
    });
  });
  