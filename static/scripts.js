// Mobile Navigation Toggle
document.addEventListener("DOMContentLoaded", () => {
    const navToggle = document.querySelector(".nav-toggle")
    const navMenu = document.querySelector(".nav-menu")
  
    if (navToggle && navMenu) {
      navToggle.addEventListener("click", () => {
        navMenu.classList.toggle("active")
        navToggle.classList.toggle("active")
      })
    }
  
    // Close mobile menu when clicking on a link
    const navLinks = document.querySelectorAll(".nav-menu a")
    navLinks.forEach((link) => {
      link.addEventListener("click", () => {
        navMenu.classList.remove("active")
        navToggle.classList.remove("active")
      })
    })
  
    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]')
    anchorLinks.forEach((link) => {
      link.addEventListener("click", function (e) {
        e.preventDefault()
        const target = document.querySelector(this.getAttribute("href"))
        if (target) {
          target.scrollIntoView({
            behavior: "smooth",
            block: "start",
          })
        }
      })
    })
  
    // Navbar scroll effect
    const navbar = document.querySelector(".navbar")
    if (navbar) {
      window.addEventListener("scroll", () => {
        if (window.scrollY > 100) {
          navbar.classList.add("scrolled")
        } else {
          navbar.classList.remove("scrolled")
        }
      })
    }
  
    // Flash message close functionality
    const closeAlerts = document.querySelectorAll(".close-alert")
    closeAlerts.forEach((button) => {
      button.addEventListener("click", function () {
        this.parentElement.style.display = "none"
      })
    })
  
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll(".alert")
    flashMessages.forEach((message) => {
      setTimeout(() => {
        message.style.opacity = "0"
        setTimeout(() => {
          message.style.display = "none"
        }, 300)
      }, 5000)
    })
  
    // Animate elements on scroll
    const observerOptions = {
      threshold: 0.1,
      rootMargin: "0px 0px -50px 0px",
    }
  
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("fade-in-up")
        }
      })
    }, observerOptions)
  
    // Observe elements for animation
    const animateElements = document.querySelectorAll(".package-card, .service-card, .event-card, .catering-card")
    animateElements.forEach((el) => observer.observe(el))
  
    // Form validation
    const forms = document.querySelectorAll("form")
    forms.forEach((form) => {
      form.addEventListener("submit", (e) => {
        const requiredFields = form.querySelectorAll("[required]")
        let isValid = true
  
        requiredFields.forEach((field) => {
          if (!field.value.trim()) {
            isValid = false
            field.style.borderColor = "#dc3545"
          } else {
            field.style.borderColor = ""
          }
        })
  
        if (!isValid) {
          e.preventDefault()
          alert("Please fill in all required fields.")
        }
      })
    })
  })
  
  // Video background controls (if video exists)
  document.addEventListener("DOMContentLoaded", () => {
    const heroVideo = document.querySelector(".hero-video")
    if (heroVideo) {
      // Ensure video plays on mobile devices
      heroVideo.muted = true
      heroVideo.playsInline = true
  
      // Handle video loading errors
      heroVideo.addEventListener("error", () => {
        console.log("Video failed to load, falling back to background image")
        heroVideo.style.display = "none"
      })
    }
  })
  
document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector(".events-grid");
    
    // Clone cards to make the loop seamless
    container.innerHTML += container.innerHTML;

    let scrollSpeed = 1; // pixels per frame
    function autoScroll() {
        container.scrollLeft += scrollSpeed;
        if (container.scrollLeft >= container.scrollWidth / 2) {
            container.scrollLeft = 0; // reset when half scrolled (due to clone)
        }
        requestAnimationFrame(autoScroll);
    }
    autoScroll();
});



  // Utility function for smooth scrolling to sections
  function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId)
    if (section) {
      section.scrollIntoView({
        behavior: "smooth",
        block: "start",
      })
    }
  }
  //  calculator 
   document.addEventListener("DOMContentLoaded", function () {
          const toggle = document.getElementById("mobile-menu");
          const menu = document.getElementById("nav-menu");
      
          toggle.addEventListener("click", () => {
            menu.classList.toggle("show");
          });
        });

  // Store dish data from Flask template
        const dishData = {
            {% for dish in dishes %}
            {{ dish.id }}: {
                id: {{ dish.id }},
                name: "{{ dish.name }}",
                price: {{ dish.price }},
                category: "{{ dish.category }}",
                description: "{{ dish.description or '' }}",
                quantity: 0
            }{% if not loop.last %},{% endif %}
            {% endfor %}
        };

        // Change guest count
        function changeGuests(change) {
            const guestInput = document.getElementById('guest-count');
            let currentGuests = parseInt(guestInput.value) || 0;
            let newGuests = Math.max(1, currentGuests + change);
            guestInput.value = newGuests;
            updateTotal();
        }

        // Change dish quantity
        function changeDishQuantity(dishId, change) {
            const dish = dishData[dishId];
            if (!dish) return;

            dish.quantity = Math.max(0, dish.quantity + change);
            
            // Update UI
            document.getElementById(`qty-${dishId}`).textContent = dish.quantity;
            document.getElementById(`total-${dishId}`).textContent = dish.price * dish.quantity;
            
            // Update minus button state
            const minusBtn = document.querySelector(`[onclick="changeDishQuantity(${dishId}, -1)"]`);
            minusBtn.disabled = dish.quantity <= 0;
            
            updateTotal();
        }

        // Update total calculations
        function updateTotal() {
            const guestCount = parseInt(document.getElementById('guest-count').value) || 0;
            document.getElementById('guest-output').textContent = guestCount;

            let perGuestTotal = 0;

            // Calculate total from all dishes
            Object.values(dishData).forEach(dish => {
                perGuestTotal += dish.price * dish.quantity;
            });

            document.getElementById('per-guest-total').textContent = perGuestTotal;
            document.getElementById('final-total').textContent = perGuestTotal * guestCount;
        }

        // Get quote function
        function getQuote() {
            const guestCount = parseInt(document.getElementById('guest-count').value) || 0;
            const finalTotal = parseInt(document.getElementById('final-total').textContent) || 0;
            
            if (finalTotal === 0) {
                alert('Please select some dishes to get a quote!');
                return;
            }

            let selectedDishes = [];
            Object.values(dishData).forEach(dish => {
                if (dish.quantity > 0) {
                    selectedDishes.push(`${dish.name} x${dish.quantity}`);
                }
            });

            const message = `Quote Request:\n\nGuests: ${guestCount}\nSelected Dishes:\n${selectedDishes.join('\n')}\n\nTotal Amount: ₹${finalTotal}\n\nThank you for choosing Dream Creation!`;
            
            alert(message);
            
      
        }

        // Initialize the page
        updateTotal();




// auto play vedio 
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll("video.hero-video").forEach(video => {
        video.muted = true; // ensure mute
        video.play().catch(err => {
            console.warn("Autoplay blocked:", err);
        });
    });
});


  // Package card interactions
  document.addEventListener("DOMContentLoaded", () => {
    const packageCards = document.querySelectorAll(".package-card")
    packageCards.forEach((card) => {
      card.addEventListener("mouseenter", function () {
        this.style.transform = "translateY(-15px)"
      })
  
      card.addEventListener("mouseleave", function () {
        if (!this.classList.contains("popular")) {
          this.style.transform = "translateY(0)"
        } else {
          this.style.transform = "scale(1.05) translateY(-15px)"
        }
      })
    })
  })
  

  // #--------------------------




  
 // Simple reveal on scroll
    (function () {
      const cards = document.querySelectorAll('.dish-card');
      const io = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('in-view');
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12 });
      cards.forEach(c => io.observe(c));
    })();
  