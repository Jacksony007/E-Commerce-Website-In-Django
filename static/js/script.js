document.addEventListener("DOMContentLoaded", function () {
  const updateButton = document.getElementById("update-button");
  const removeButtons = document.getElementsByClassName("remove-button");
  const quantityInputs = document.querySelectorAll('input[type="number"]');
  const totalNumberElement = document.getElementById("total-number");

  // Update button click event
  updateButton.addEventListener("click", function () {
    updateTotal();
  });

  // Remove button click events
  for (let i = 0; i < removeButtons.length; i++) {
    const removeButton = removeButtons[i];

    removeButton.addEventListener("click", function () {
      const cartItem = this.parentElement;
      cartItem.remove();

      // Update item numbers
      updateItemNumbers();

      // Recalculate total and update UI
      updateTotal();

      // Show empty cart message if no items left
      if (document.getElementsByClassName("cart-item").length === 0) {
        document.getElementById("cart-items").style.display = "none";
        document.getElementById("empty-cart").style.display = "block";
      }
    });
  }

  // Number input change event
  quantityInputs.forEach(function (input) {
    input.addEventListener("change", function () {
      updatePrice(this);
    });
  });

  // Function to update the total
  function updateTotal() {
    const cartItems = document.getElementsByClassName("cart-item");
    let subtotal = 0;
    let totalNumber = 0;

    for (let i = 0; i < cartItems.length; i++) {
      const cartItem = cartItems[i];
      const quantity = parseInt(
        cartItem.querySelector('input[type="number"]').value
      );
      const price = parseFloat(
        cartItem.querySelector("p:nth-child(3)").textContent.slice(1)
      );
      const itemTotal = quantity * price;
      cartItem.querySelector("p:nth-child(4)").textContent =
        "$" + itemTotal.toFixed(2);
      subtotal += itemTotal;
      totalNumber += quantity;
    }

    let deliveryFee = 0;
    let discount = 0;
    let total = subtotal;

    if (subtotal < 25000) {
      deliveryFee = 5;
      total = subtotal + deliveryFee;
    } else {
      discount = subtotal * 0.03; // Calculate 3% discount
      total = subtotal - discount;
    }

    const cartTotalElement = document.getElementById("cart-total");
    cartTotalElement.querySelector("h3").textContent =
      "Total: $" + total.toFixed(2);

    // Display actual price, discount, and delivery fee
    const actualPriceElement = document.getElementById("actual-price");
    actualPriceElement.textContent = "Actual Price: $" + subtotal.toFixed(2);

    const discountPriceElement = document.getElementById("discount-price");
    if (discount > 0) {
      discountPriceElement.textContent = "Discount: $" + discount.toFixed(2);
    } else {
      discountPriceElement.textContent = "";
    }

    const deliveryFeeElement = document.getElementById("delivery-fee");
    if (deliveryFee > 0) {
      deliveryFeeElement.textContent =
        "Delivery Fee: $" + deliveryFee.toFixed(2);
    } else {
      deliveryFeeElement.textContent = "";
    }

    // Update total number of products
    totalNumberElement.textContent = totalNumber.toString();
  }

  // Function to update price when quantity changes
  function updatePrice(input) {
    const cartItem = input.parentElement;
    const quantity = parseInt(input.value);
    const price = parseFloat(
      cartItem.querySelector("p:nth-child(3)").textContent.slice(1)
    );
    const itemTotal = quantity * price;
    cartItem.querySelector("p:nth-child(4)").textContent =
      "$" + itemTotal.toFixed(2);

    updateTotal();
  }

  // Function to update item numbers
  function updateItemNumbers() {
    const cartItems = document.getElementsByClassName("cart-item");

    for (let i = 0; i < cartItems.length; i++) {
      const cartItem = cartItems[i];
      cartItem.querySelector("p:nth-child(1)").textContent = "Item #" + (i + 1);
    }

    const totalQuantityElement = document.querySelector("#total-quantity");
    totalQuantityElement.textContent = totalQuantity; // Update the total quantity in the HTML
  }

  // Initial calculation of total and update item numbers
  updateTotal();
  updateItemNumbers();
});

// Function to update the cart count
function updateCartCount() {
  $.ajax({
    url: "/getCartItemCount/",
    method: "GET",
    success: function (response) {
      var cartItemCount = response.count;
      var cartCountElement = document.getElementById("cart_count_placeholder");
      var cartCountElement1 = document.getElementById("cart_count");
      (cartCountElement.textContent = cartItemCount),
        (cartCountElement1.textContent = cartItemCount);
    },
    error: function (error) {
      console.error("Error fetching cart item count:", error);
    },
  });
}

// Update the cart count initially
updateCartCount();

// Call the updateCartCount function periodically to keep the count updated
setInterval(updateCartCount, 5000); // Refresh every 5 seconds (adjust as needed)

$(document).ready(function () {
  // Attach click event listener to elements with the specified class
  $(".add_to_cart_btn").on("click", function () {
    // Get the product ID from a data attribute or any other method based on your HTML structure
    var productId = $(this).data("product-id");

    // Call the addToCart function with the product ID
    addToCart(productId);
  });
});

function addToCart(productId) {
  // Send an AJAX request to the server
  console.log("Updating cart count...");
  $.ajax({
    type: "POST",
    url: "/add_to_cart/",
    data: {
      product_id: productId,
      csrfmiddlewaretoken: getCSRFToken(),
    },
    success: function (response) {
      // Handle the response from the server
      if (response.success) {
        alert("Product added to cart!");
      } else {
        alert("Failed to add product to cart. Please try again.");
      }
    },
    error: function (xhr, status, error) {
      console.error(xhr.responseText);
    },
  });
}

function getCSRFToken() {
  // Retrieve the CSRF token from the cookie
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Check if the cookie name matches the Django CSRF token cookie name (default is 'csrftoken')
      if (cookie.substring(0, "csrftoken".length + 1) === "csrftoken=") {
        cookieValue = decodeURIComponent(
          cookie.substring("csrftoken".length + 1)
        );
        break;
      }
    }
  }
  return cookieValue;
}

// script.js

function removeProduct(itemId) {
  const request = new XMLHttpRequest();
  request.open("POST", `/cart/remove/${itemId}/`);
  request.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
  request.setRequestHeader("Content-Type", "application/json");
  request.onload = function () {
    if (request.status === 200) {
      const response = JSON.parse(request.responseText);
      console.log(response.message);
      // Optionally, update the UI to reflect the removal of the product
    } else {
      console.error("Error removing product from cart.");
    }
  };
  request.send();
}

function getCookie(name) {
  const cookieValue = document.cookie.match(
    "(^|;)\\s*" + name + "\\s*=\\s*([^;]+)"
  );
  return cookieValue ? cookieValue.pop() : "";
}

function openConfirmationModal(itemId) {
  const confirmationModal = document.getElementById("confirmation-modal");
  confirmationModal.style.display = "block";

  const confirmButton = document.getElementById("confirm-button");
  const cancelButton = document.getElementById("cancel-button");

  confirmButton.onclick = function () {
    removeProduct(itemId);
    confirmationModal.style.display = "none";
  };

  cancelButton.onclick = function () {
    confirmationModal.style.display = "none";
  };
}
