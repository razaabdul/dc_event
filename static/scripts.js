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
  