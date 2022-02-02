var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
var stripe = Stripe("pk_test_51KO5UvJsODTnE8pPzublS0PEqyOtu4spslJiGJo4fNOV5qRvFordWelVElh6WJHmYxLZrXawIRRjDlYMRa85c136009pvo85rV");
document.querySelector("button").disabled = true;
var elements = stripe.elements();
var style = {
    base: {
        color: "#32325d",
        fontFamily: 'Arial, sans-serif',
        fontSmoothing: "antialiased",
        fontSize: "16px",
        "::placeholder": {
            color: "#32325d"
        }
    },
    invalid: {
        fontFamily: 'Arial, sans-serif',
        color: "#fa755a",
        iconColor: "#fa755a"
    }
};
var card = elements.create("card", { style: style });
// Stripe injects an iframe into the DOM
card.mount("#card-element");
card.on("change", function (event) {
    // Disable the Pay button if there are no card details in the Element
    document.querySelector("button").disabled = event.empty;
    document.querySelector("#card-error").textContent = event.error ? event.error.message : "";
});
var form = document.getElementById("payment-form");
form.addEventListener("submit", function (event) {
    event.preventDefault();
    var selectedPrice = document.getElementById("prices").value
    // Complete payment when the submit button is clicked
    fetch(`/create-payment-intent/${selectedPrice}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            email: document.getElementById('email').value
        })
    })
        .then(function (result) {
            return result.json();
        })
        .then(function (data) {
            payWithCard(stripe, card, data.clientSecret);
        });
});

// Calls stripe.confirmCardPayment
// If the card requires authentication Stripe shows a pop-up modal to
// prompt the user to enter authentication details without leaving your page.
var payWithCard = function (stripe, card, clientSecret) {
    loading(true);
    stripe
        .confirmCardPayment(clientSecret, {
            payment_method: {
                card: card
            }
        })
        .then(function (result) {
            if (result.error) {
                // Show error to your customer
                showError(result.error.message);
            } else {
                // The payment succeeded!
                orderComplete(result.paymentIntent.id);
            }
        });
};
/* ------- UI helpers ------- */
// Shows a success message when the payment is complete
var orderComplete = function (paymentIntentId) {
    loading(false);
    document
        .querySelector(".result-message a")
        .setAttribute(
            "href",
            "https://dashboard.stripe.com/test/payments/" + paymentIntentId
        );
    document.querySelector(".result-message").classList.remove("hidden");
    document.querySelector("button").disabled = true;
};
// Show the customer the error from Stripe if their card fails to charge
var showError = function (errorMsgText) {
    loading(false);
    var errorMsg = document.querySelector("#card-error");
    errorMsg.textContent = errorMsgText;
    setTimeout(function () {
        errorMsg.textContent = "";
    }, 4000);
};
// Show a spinner on payment submission
var loading = function (isLoading) {
    if (isLoading) {
        // Disable the button and show a spinner
        document.querySelector("button").disabled = true;
        document.querySelector("#spinner").classList.remove("hidden");
        document.querySelector("#button-text").classList.add("hidden");
    } else {
        document.querySelector("button").disabled = false;
        document.querySelector("#spinner").classList.add("hidden");
        document.querySelector("#button-text").classList.remove("hidden");
    }
};
