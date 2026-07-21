(() => {
  // Normalize legacy page-level styles to the shared green–gold palette. Several
  // older pages contain local <style> blocks and inline styles, so variables alone
  // cannot keep the rendered experience visually consistent.
  const legacyPalette = [
    [/#e8714a/gi, "#8063c7"],
    [/#c4813a/gi, "#d96f9f"],
    [/#f09060/gi, "#b79ae4"],
    [/#f4b090/gi, "#f4d47f"],
    [/#1e1714/gi, "#302447"],
    [/#1e1a14/gi, "#3b2d55"],
    [/#181310/gi, "#392b53"],
    [/#d4c0ac/gi, "#eee7f7"],
    [/#9e8b7e/gi, "#9b8eae"],
    [/#fdf6ef/gi, "#fcf9ff"],
    [/rgba\(\s*232\s*,\s*113\s*,\s*74\s*,/gi, "rgba(128, 99, 199,"],
    [/rgba\(\s*196\s*,\s*129\s*,\s*58\s*,/gi, "rgba(217, 111, 159,"],
    [/rgba\(\s*30\s*,\s*23\s*,\s*20\s*,/gi, "rgba(48, 36, 71,"],
    [/rgba\(\s*212\s*,\s*192\s*,\s*172\s*,/gi, "rgba(238, 231, 247,"]
  ];
  const applyPalette = (value) => legacyPalette.reduce(
    (updated, [pattern, replacement]) => updated.replace(pattern, replacement), value
  );
  document.querySelectorAll("style, [style], [stop-color]").forEach((element) => {
    if (element.tagName === "STYLE") element.textContent = applyPalette(element.textContent);
    if (element.hasAttribute("style")) element.setAttribute("style", applyPalette(element.getAttribute("style")));
    if (element.hasAttribute("stop-color")) element.setAttribute("stop-color", applyPalette(element.getAttribute("stop-color")));
  });

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

    // Make 1st FAQ open by default
    if (index === 0) {
      item.classList.add("is-open");
      question.setAttribute("aria-expanded", "true");
    } else {
      item.classList.remove("is-open");
      question.setAttribute("aria-expanded", "false");
    }

    const toggle = () => {
      const isOpen = item.classList.contains("is-open");

      // Close all other items
      items.forEach((otherItem) => {
        if (otherItem !== item) {
          otherItem.classList.remove("is-open");
          otherItem.querySelector("h4")?.setAttribute("aria-expanded", "false");
        }
      });

      // Toggle current item
      const nowOpen = !isOpen;
      if (nowOpen) {
        item.classList.add("is-open");
        question.setAttribute("aria-expanded", "true");
      } else {
        item.classList.remove("is-open");
        question.setAttribute("aria-expanded", "false");
      }
    };

    item.addEventListener("click", toggle);
    question.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        toggle();
      }
    });
  });

  // Count up stats animations
  const stats = [
    { id: "stat-years", target: 15, suffix: "+" },
    { id: "stat-facilities", target: 750, suffix: "+" },
    { id: "stat-states", target: 6, suffix: "" },
    { id: "stat-support", target: 24, suffix: "/7" },
    { id: "service-stat-1", target: 1, suffix: "", pad: true },
    { id: "service-stat-2", target: 2, suffix: "", pad: true },
    { id: "service-stat-3", target: 3, suffix: "", pad: true }
  ];

  const animateStats = () => {
    stats.forEach(stat => {
      const el = document.getElementById(stat.id);
      if (!el) return;

      let current = 0;
      const duration = 1200; // ms
      const startTime = performance.now();

      const update = (timestamp) => {
        const elapsed = timestamp - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Easing out quadratic
        const ease = progress * (2 - progress);

        const value = Math.floor(ease * stat.target);
        const displayValue = stat.pad ? String(value).padStart(2, '0') : value;
        el.textContent = `${displayValue}${stat.suffix}`;

        if (progress < 1) {
          requestAnimationFrame(update);
        } else {
          const finalDisplayValue = stat.pad ? String(stat.target).padStart(2, '0') : stat.target;
          el.textContent = `${finalDisplayValue}${stat.suffix}`;
        }
      };

      requestAnimationFrame(update);
    });
  };

  const resetStats = () => {
    const defaultStats = [
      { id: "stat-years", initial: "0+" },
      { id: "stat-facilities", initial: "0+" },
      { id: "stat-states", initial: "0" },
      { id: "stat-support", initial: "0/7" },
      { id: "service-stat-1", initial: "00" },
      { id: "service-stat-2", initial: "00" },
      { id: "service-stat-3", initial: "00" }
    ];
    defaultStats.forEach(stat => {
      const el = document.getElementById(stat.id);
      if (el) {
        el.textContent = stat.initial;
      }
    });
  };

  const statsContainer = document.querySelector(".hero-stats");
  if (statsContainer) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateStats();
        } else {
          resetStats();
        }
      });
    }, { threshold: 0.1 });

    observer.observe(statsContainer);
  }

  // Reveal content progressively, while keeping the experience motion-safe.
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const revealTargets = document.querySelectorAll(
      ".service-card, .industry-card, .location-card, .feature-card, .why-card, .difference-card, .process-card, .contact-card"
    );
    revealTargets.forEach((element, index) => {
      element.classList.add("scroll-reveal");
      element.style.setProperty("--reveal-delay", `${Math.min(index % 4, 3) * 70}ms`);
    });
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealTargets.forEach((element) => revealObserver.observe(element));
  }
})();

