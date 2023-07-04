// Get the price, quantity, and total fields
const priceField = document.getElementById('price');
const quantityField = document.getElementById('quantity');
const totalField = document.getElementById('total');

// Add event listeners to price and quantity fields
priceField.addEventListener('input', updateTotalAmount);
quantityField.addEventListener('input', updateTotalAmount);

function updateTotalAmount() {
  const price = parseFloat(priceField.value);
  const quantity = parseInt(quantityField.value);

  // Calculate the total amount
  const total = price * quantity;

  // Update the total field value
  totalField.value = total.toFixed(2);
}

