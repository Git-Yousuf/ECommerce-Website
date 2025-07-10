function showMessage() {
    const message = document.getElementById("message");
    message.style.display = "block";
    message.style.position = "absolute";
    message.style.top = "125%";
    message.style.right = "0%";
  }
  
  function hideMessage() {
    const message = document.getElementById("message");
    message.style.display = "none";
  }
  
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".products-card").forEach((card) => {
        const counterElement = card.querySelector(".counter");
        const minusButton = card.querySelector(".fa-minus").parentElement;
        const plusButton = card.querySelector(".fa-plus").parentElement;

        let count = parseInt(counterElement.innerText, 10);

        plusButton.addEventListener("click", () => {
            count++;
            counterElement.innerText = count;
        });

        minusButton.addEventListener("click", () => {
            if (count > 1) {
                count--;
                counterElement.innerText = count;
            }
        });
    });
});

