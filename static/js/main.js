console.log("Orchard is running 🌱");
```javascript
// Orchard featured product slider
document.addEventListener("DOMContentLoaded", () => {
  const slider = document.getElementById("featured-products");
  const previous = document.getElementById("products-prev");
  const next = document.getElementById("products-next");

  if (!slider || !previous || !next) return;

  const scrollAmount = () => {
    const card = slider.querySelector(".product-card");
    if (!card) return slider.clientWidth * 0.8;

    const styles = window.getComputedStyle(slider);
    const gap = parseFloat(styles.columnGap) || 0;

    return card.getBoundingClientRect().width + gap;
  };

  previous.addEventListener("click", () => {
    slider.scrollBy({
      left: -scrollAmount(),
      behavior: "smooth"
    });
  });

  next.addEventListener("click", () => {
    slider.scrollBy({
      left: scrollAmount(),
      behavior: "smooth"
    });
  });
});
```;
