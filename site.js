(() => {
  const currentPage =
    window.location.pathname.split("/").pop().toLowerCase() || "index.html";

  const nav = document.querySelector("nav");
  if (nav) {
    const isHomePage = currentPage === "index.html" || currentPage === "" || currentPage === "/";
    const navLinksHtml = isHomePage 
      ? `
          <li><a href="services.html">Services</a></li>
          <li><a href="commercial-cleaning-services.html">Cleaning</a></li>
          <li><a href="commercial-construction.html">Construction</a></li>
          <li><a href="smart-cleaning-robotics.html">Technology</a></li>
          <li><a href="#faq">FAQ</a></li>`
      : `
          <li><a href="services.html">Services</a></li>
          <li><a href="industries.html">Industries</a></li>
          <li><a href="locations.html">Locations</a></li>
          <li><a href="why-rcc-bgm.html">Why RCC-BGM</a></li>
          <li><a href="about.html">About</a></li>`;

    nav.innerHTML = `
      <div class="container nav-flex">
        <a href="index.html" class="logo" aria-label="RCC-BGM home">
          <span class="logo-icon"><i class="fa-solid fa-building-shield"></i></span>RCC<span>BGM</span>
        </a>
        <ul class="nav-links">
          ${navLinksHtml}
        </ul>
        <button class="nav-toggle" type="button" aria-label="Open navigation" aria-expanded="false">
          <i class="fa-solid fa-bars"></i>
        </button>
        <a href="contact.html" class="btn-header">Get Assessment</a>
      </div>`;

    const navToggle = nav.querySelector(".nav-toggle");
    const navLinks = nav.querySelector(".nav-links");
    navToggle?.addEventListener("click", () => {
      const open = nav.classList.toggle("nav-open");
      navToggle.setAttribute("aria-expanded", String(open));
      navToggle.setAttribute(
        "aria-label",
        open ? "Close navigation" : "Open navigation",
      );
      navToggle.querySelector("i").className = open
        ? "fa-solid fa-xmark"
        : "fa-solid fa-bars";
    });
    navLinks?.addEventListener("click", () => {
      nav.classList.remove("nav-open");
      navToggle?.setAttribute("aria-expanded", "false");
    });

    nav.querySelectorAll("a[href]").forEach((link) => {
      if (link.getAttribute("href").toLowerCase() === currentPage) {
        link.classList.add("is-active");
        link.setAttribute("aria-current", "page");
      }
    });

    // Background transition on scroll
    window.addEventListener("scroll", () => {
      if (window.scrollY > 30) {
        nav.classList.add("nav-scrolled");
      } else {
        nav.classList.remove("nav-scrolled");
      }
    });
    // Trigger initial check
    if (window.scrollY > 30) {
      nav.classList.add("nav-scrolled");
    }
  }

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (href === '#' || href === '#!') return;
      const targetEl = document.querySelector(href);
      if (targetEl) {
        e.preventDefault();
        const header = document.querySelector('nav');
        const navHeight = header ? header.offsetHeight : 0;
        const targetPosition = targetEl.getBoundingClientRect().top + window.pageYOffset - navHeight;
        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

  const footer = document.querySelector("footer");
  if (footer) {
    footer.innerHTML = `
      <div class="container f-grid">
        <div class="f-col">
          <a href="index.html" class="logo">RCC<span>BGM</span></a>
          <p class="footer-summary">Integrated commercial cleaning, maintenance, construction and building-system solutions.</p>
        </div>
        <div class="f-col">
          <h4>Core Services</h4>
          <ul>
            <li><a href="commercial-cleaning-services.html">Commercial Cleaning</a></li>
            <li><a href="facility-maintenance-services.html">Facility Maintenance</a></li>
            <li><a href="commercial-construction.html">Commercial Construction</a></li>
            <li><a href="commercial-hvac-services.html">Commercial HVAC</a></li>
            <li><a href="commercial-mep-services.html">Commercial MEP</a></li>
          </ul>
        </div>
        <div class="f-col">
          <h4>Explore</h4>
          <ul>
            <li><a href="services.html">All Services</a></li>
            <li><a href="industries.html">Industries</a></li>
            <li><a href="locations.html">Locations</a></li>
            <li><a href="why-rcc-bgm.html">Why RCC-BGM</a></li>
            <li><a href="about.html">About</a></li>
          </ul>
        </div>
        <div class="f-col">
          <h4>Contact HQ</h4>
          <p>San Jose, California<br />United States</p>
          <a href="mailto:support@rcc-bgm.com">support@rcc-bgm.com</a>
          <a class="footer-contact-link" href="contact.html">Request an assessment</a>
        </div>
      </div>`;
  }

  const items = [...document.querySelectorAll(".faq-item")];

  items.forEach((item, index) => {
    const question = item.querySelector("h4");
    const answer = item.querySelector("p");
    if (!question || !answer) return;

    const id = `faq-answer-${index + 1}`;
    answer.id = id;
    question.setAttribute("role", "button");
    question.setAttribute("tabindex", "0");
    question.setAttribute("aria-controls", id);
    question.setAttribute("aria-expanded", "false");
    item.classList.remove("is-open");

    const toggle = () => {
      const open = item.classList.toggle("is-open");
      question.setAttribute("aria-expanded", String(open));
    };

    question.addEventListener("click", toggle);
    question.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        toggle();
      }
    });
  });
})();
