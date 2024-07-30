document.addEventListener('DOMContentLoaded', function () {
    const checkoutButton = document.getElementById('checkout-button');
    const cartMessage = document.getElementById('cart-message');
    const cartLength = checkoutButton.getAttribute('data-cart-length');
    const orderUrl = checkoutButton.getAttribute('data-order-url');

    checkoutButton.addEventListener('click', function (event) {
        if (cartLength == 0) {
            event.preventDefault();
            cartMessage.textContent = 'Please add items to your cart before proceeding to checkout.';
            cartMessage.style.color = '#40B2E4';
        } else {
            window.location.href = orderUrl;
        }
    });
});
