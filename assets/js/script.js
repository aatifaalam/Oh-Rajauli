'use strict';



/**
 * navbar toggle
 */

const navbar = document.querySelector("[data-navbar]");
const navbarLinks = document.querySelectorAll("[data-nav-link]");
const menuToggleBtn = document.querySelector("[data-menu-toggle-btn]");

menuToggleBtn.addEventListener("click", function () {
  navbar.classList.toggle("active");
  this.classList.toggle("active");
});

for (let i = 0; i < navbarLinks.length; i++) {
  navbarLinks[i].addEventListener("click", function () {
    navbar.classList.toggle("active");
    menuToggleBtn.classList.toggle("active");
  });
}



/**
 * header sticky & back to top
 */

const header = document.querySelector("[data-header]");
const backTopBtn = document.querySelector("[data-back-top-btn]");

window.addEventListener("scroll", function () {
  if (window.scrollY >= 100) {
    header.classList.add("active");
    backTopBtn.classList.add("active");
  } else {
    header.classList.remove("active");
    backTopBtn.classList.remove("active");
  }
});



/**
 * search box toggle
 */

const searchBtn = document.querySelector("[data-search-btn]");
const searchContainer = document.querySelector("[data-search-container]");
const searchSubmitBtn = document.querySelector("[data-search-submit-btn]");
const searchCloseBtn = document.querySelector("[data-search-close-btn]");

const searchBoxElems = [searchBtn, searchSubmitBtn, searchCloseBtn];

for (let i = 0; i < searchBoxElems.length; i++) {
  searchBoxElems[i].addEventListener("click", function () {
    searchContainer.classList.toggle("active");
    document.body.classList.toggle("active");
  });
}



/**
 * move cycle on scroll
 */

const deliveryBoy = document.querySelector("[data-delivery-boy]");

let deliveryBoyMove = -80;
let lastScrollPos = 0;

window.addEventListener("scroll", function () {

  let deliveryBoyTopPos = deliveryBoy.getBoundingClientRect().top;

  if (deliveryBoyTopPos < 500 && deliveryBoyTopPos > -250) {
    let activeScrollPos = window.scrollY;

    if (lastScrollPos < activeScrollPos) {
      deliveryBoyMove += 1;
    } else {
      deliveryBoyMove -= 1;
    }

    lastScrollPos = activeScrollPos;
    deliveryBoy.style.transform = `translateX(${deliveryBoyMove}px)`;
  }

});

/**
 * Backend Integration
 */

// Handle Book a Table form submission
const bookingForm = document.getElementById("booking-form");
if (bookingForm) {
  bookingForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(bookingForm);
    const data = {
      name: formData.get("full_name"),
      email: formData.get("email_address"),
      total_person: parseInt(formData.get("total_person")) || 1,
      booking_date: formData.get("booking_date") ? new Date(formData.get("booking_date")).toISOString() : new Date().toISOString(),
      message: formData.get("message"),
      phone_number: "1234567890" // Adding default as UI does not have phone field
    };

    try {
      const response = await fetch("/api/bookings", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        alert("Table booked successfully!");
        bookingForm.reset();
      } else {
        const err = await response.json();
        alert("Error booking table: " + (err.detail || "Unknown error"));
      }
    } catch (error) {
      console.error(error);
      alert("Something went wrong!");
    }
  });
}

// Handle Order Now buttons
const orderBtns = document.querySelectorAll(".food-menu-btn");
orderBtns.forEach(btn => {
  btn.addEventListener("click", async function () {
    const card = this.closest(".food-menu-card");
    const itemName = card.querySelector(".card-title").innerText;
    let priceText = card.querySelector(".price").innerText;
    // Extract numbers: e.g. ₹599.00 -> 599.00
    let priceMatch = priceText.match(/[\d.]+/);
    let price = priceMatch ? parseFloat(priceMatch[0]) : 0;

    const orderData = {
      customer_name: "Guest User",
      phone: "1234567890",
      items: [
        {
          item_name: itemName,
          quantity: 1,
          price: price
        }
      ]
    };

    try {
      const response = await fetch("/api/orders", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(orderData)
      });

      if (response.ok) {
        alert(`Successfully ordered: ${itemName}!`);
      } else {
        const err = await response.json();
        alert("Error placing order: " + (err.detail || "Unknown error"));
      }
    } catch (error) {
      console.error(error);
      alert("Something went wrong placing the order!");
    }
  });
});