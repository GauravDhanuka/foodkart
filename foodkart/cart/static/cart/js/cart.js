// Function to calculate and update cart totals
function updateCart() {
  let total = 0;
  const cartBody = document.getElementById("cart-body");
  const rows = cartBody.querySelectorAll("tr:not(.total-row)");

  rows.forEach((row) => {
    const quantityInput = row.querySelector(".quantity-input");

    if (!quantityInput) {
      console.error(
        "Error: Quantity input element not found in row for product:",
        row.dataset.productName
      );
      const linePriceElement = row.querySelector(".line-price");
      if (linePriceElement) {
        linePriceElement.textContent = `AED 0.00`;
      }
      return;
    }

    // Retrieve price per kg from the data-price-per-kg attribute on the row
    const pricePerKg = parseFloat(row.dataset.pricePerKg);
    const linePriceElement = row.querySelector(".line-price");

    let quantity = parseFloat(quantityInput.value);

    // Basic validation
    if (isNaN(quantity) || quantity < 0) {
      quantity = 0;
      quantityInput.value = 0;
    }

    // Calculate the line total for the current product
    const lineTotal = quantity * pricePerKg;
    linePriceElement.textContent = `AED ${lineTotal.toFixed(2)}`;
    // Add to the overall cart total
    total += lineTotal;
  });
  document.getElementById("cart-total").textContent = `AED ${total.toFixed(2)}`;
}
document.addEventListener("DOMContentLoaded", updateCart);
