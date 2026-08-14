(function () {
  const BASE = document.body.dataset.base || "";
  const PAGE = document.body.dataset.page || "home";

  // API routing: window.SSN_API (see assets/js/config.js) can point a static
  // deployment at a backend. On github.io / file:// hosts without a backend,
  // the site runs as a read-only copy.
  const API = String(window.SSN_API || "").trim().replace(/\/+$/, "");
  const STATIC_HOST = /(^|\.)github\.io$/i.test(location.hostname) || location.protocol === "file:";
  const NO_BACKEND = STATIC_HOST && !API;

  function api(path) {
    if (!API) return path;
    if (/^https?:\/\//i.test(path)) return path;
    return API + (path.charAt(0) === "/" ? path : "/" + path);
  }
  function resolveAsset(url) {
    // Backend-relative assets (e.g. /uploads/…) need the API base on static hosts.
    if (!url) return url;
    if (url.charAt(0) === "/" && !/^\/\//.test(url) && API) return api(url);
    return url;
  }
  if (!document.querySelector('link[href*="prof.css"]')) {
    const prof = document.createElement("link");
    prof.rel = "stylesheet";
    prof.href = BASE + "assets/css/prof.css?v=inst6";
    document.head.appendChild(prof);
  }

  const NAV = [
    ["home", "Home", "index.html"],
    ["about", "About", "about/index.html"],
    ["family", "Siddeshwor Family", "family/index.html"],
    ["why-us", "Why Us?", "why-us/index.html"],
    ["academics", "Academics", "academics/index.html"],
    ["facilities", "Facilities", "facilities/index.html"],
    ["news", "News", "news/index.html"],
    ["notice", "Notice", "notice/index.html"],
    ["gallery", "Gallery", "gallery/index.html"],
    ["contact", "Contact", "contact/index.html"],
  ];

  const I18N = {
    en: {
      home: "Home", about: "About", family: "Siddeshwor Family", "why-us": "Why Us?",
      academics: "Academics", facilities: "Facilities", news: "News", notice: "Notice",
      gallery: "Gallery", contact: "Contact", apply: "Apply Now",
      contactInfo: "Contact Information", aboutUs: "About Us", sidAcad: "Siddeshwor Academics",
      newsletter: "Newsletter", stay: "Stay updated with our latest news", subscribe: "Subscribe",
      privacy: "Privacy", sitemap: "Sitemap", searchPh: "Search news, staff, pages…",
      suggest: "Suggest", suggestTitle: "Suggestion desk", suggestLead: "Share an idea for campus, class, safety or events.",
      suggestSend: "Send suggestion", suggestName: "Your name", suggestRole: "I am a",
      suggestMsg: "Your suggestion", more: "More",
    },
    ne: {
      home: "गृहपृष्ठ", about: "हाम्रो बारे", family: "सिद्धेश्वर परिवार", "why-us": "किन हामी?",
      academics: "अध्ययन", facilities: "सुविधा", news: "समाचार", notice: "सूचना",
      gallery: "ग्यालरी", contact: "सम्पर्क", apply: "भर्ना फारम",
      contactInfo: "सम्पर्क जानकारी", aboutUs: "हाम्रो बारे", sidAcad: "सिद्धेश्वर अध्ययन",
      newsletter: "समाचार पत्र", stay: "नयाँ समाचारका लागि सदस्य बन्नुहोस्", subscribe: "सदस्यता",
      privacy: "गोपनीयता", sitemap: "साइट नक्सा", searchPh: "समाचार, कर्मचारी, पृष्ठ खोज्नुहोस्…",
      suggest: "सुझाव", suggestTitle: "सुझाव डेस्क", suggestLead: "क्याम्पस, कक्षा, सुरक्षा वा कार्यक्रमका लागि विचार पठाउनुहोस्।",
      suggestSend: "सुझाव पठाउनुहोस्", suggestName: "तपाईंको नाम", suggestRole: "म हुँ",
      suggestMsg: "तपाईंको सुझाव", more: "थप",
    },
  };
  let lang = localStorage.getItem("ssn_lang") || "en";

  function t(key) { return (I18N[lang] || I18N.en)[key] || I18N.en[key] || key; }
  function href(path) { return path === "index.html" ? BASE + "index.html" : BASE + path; }

  const PRIMARY = ["home", "about", "family", "academics", "news", "contact"];
  const MORE = ["why-us", "facilities", "notice", "gallery"];

  function navItem([id, , path]) {
    const active = PAGE === id || (id === "news" && PAGE.startsWith("news")) ? "active" : "";
    return `<a class="${active}" href="${href(path)}" data-i18n="${id}">${t(id)}</a>`;
  }

  function desktopNav() {
    const main = NAV.filter(n => PRIMARY.includes(n[0])).map(navItem).join("");
    const extra = NAV.filter(n => MORE.includes(n[0])).map(navItem).join("");
    const moreOn = MORE.includes(PAGE) || PAGE === "suggest" ? "active" : "";
    return main +
      `<div class="nav-more">
        <button class="nav-more-btn ${moreOn}" type="button" id="moreBtn" data-i18n="more">${t("more")}</button>
        <div class="nav-more-menu" id="moreMenu">${extra}<a href="${href("suggest/index.html")}" data-i18n="suggest">${t("suggest")}</a></div>
      </div>` +
      `<a class="btn-apply" href="${href("apply/index.html")}" data-i18n="apply">${t("apply")}</a>`;
  }

  function mobileNavLinks() {
    return NAV.map(navItem).join("") +
      `<a href="${href("suggest/index.html")}" data-i18n="suggest">${t("suggest")}</a>` +
      `<a class="btn-apply" href="${href("apply/index.html")}" data-i18n="apply">${t("apply")}</a>`;
  }

  const header = `
    <a class="skip-link" href="#main-content">Skip to content</a>
    <div class="topbar">
      <div class="container topbar-inner">
        <div class="top-links">
          <span>Estd. 2047 B.S.</span>
          <a href="tel:01-4622730">01-4622730</a>
          <a href="mailto:mail@siddeshwor.edu.np">mail@siddeshwor.edu.np</a>
          <a href="${href("suggest/index.html")}" data-i18n="suggest">${t("suggest")}</a>
        </div>
        <div class="clock">
          <button class="lang-btn" id="langBtn" type="button">${lang === "ne" ? "English" : "नेपाली"}</button>
          <button class="icon-btn" id="searchBtn" type="button" aria-label="Search">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7" stroke-width="2"/><path stroke-width="2" stroke-linecap="round" d="M20 20l-3-3"/></svg>
          </button>
          <span id="npClock">लोड हुँदैछ...</span>
        </div>
      </div>
    </div>
    <header class="site-header" id="siteHeader">
      <div class="container header-inner">
        <a class="brand" href="${href("index.html")}">
          <img src="${BASE}assets/img/SiddeshworLogo.png" alt="Siddeshwor School Logo">
          <div>
            <h1>Shree Siddeshwor Secondary School</h1>
            <p>श्री सिद्धेश्वर माध्यमिक विद्यालय</p>
          </div>
        </a>
        <nav class="desktop">${desktopNav()}</nav>
        <button class="hamburger" id="menuBtn" aria-label="Menu" aria-expanded="false">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
        </button>
      </div>
      <div class="mobile-nav" id="mobileNav">${mobileNavLinks()}</div>
    </header>
    <div class="search-modal" id="searchModal" role="dialog" aria-label="Search">
      <div class="search-box">
        <input id="searchInput" type="search" placeholder="${t("searchPh")}" autocomplete="off">
        <div class="search-results" id="searchResults"><div class="search-empty">Type at least 2 characters</div></div>
      </div>
    </div>
  `;

  const footer = `
    <footer class="site-footer">
      <div class="container">
        <div class="footer-grid">
          <div>
            <h3 data-i18n="contactInfo">${t("contactInfo")}</h3>
            <p><a href="tel:01-4622730">01-4622730</a></p>
            <p style="margin-top:8px">Shantinagar, New Baneshwor, Kathmandu</p>
            <p style="margin-top:8px"><a href="mailto:mail@siddeshwor.edu.np">mail@siddeshwor.edu.np</a></p>
          </div>
          <div>
            <h3 data-i18n="aboutUs">${t("aboutUs")}</h3>
            <ul>
              <li><a href="${href("about/index.html")}">History</a></li>
              <li><a href="${href("about/index.html")}">Our Vision</a></li>
              <li><a href="${href("family/index.html")}">Our Team</a></li>
              <li><a href="${href("gallery/index.html")}">Gallery</a></li>
              <li><a href="${href("suggest/index.html")}" data-i18n="suggest">${t("suggest")}</a></li>
            </ul>
          </div>
          <div>
            <h3 data-i18n="sidAcad">${t("sidAcad")}</h3>
            <ul>
              <li><a href="${href("academics/index.html")}">ECD / Nursery</a></li>
              <li><a href="${href("academics/index.html")}">Basic Level (1-8)</a></li>
              <li><a href="${href("academics/index.html")}">Secondary (9-10)</a></li>
            </ul>
          </div>
          <div>
            <h3 data-i18n="newsletter">${t("newsletter")}</h3>
            <p style="margin-bottom:10px" data-i18n="stay">${t("stay")}</p>
            <form class="news-form" id="newsForm">
              <input type="email" placeholder="Your email here" required>
              <button type="submit" data-i18n="subscribe">${t("subscribe")}</button>
            </form>
          </div>
        </div>
        <div class="footer-bottom">
          <div class="links">
            <a href="${href("suggest/index.html")}" data-i18n="suggest">${t("suggest")}</a>
            <a href="${href("privacy/index.html")}" data-i18n="privacy">${t("privacy")}</a>
            <a href="${href("sitemap/index.html")}" data-i18n="sitemap">${t("sitemap")}</a>
          </div>
          <p>© Shree Siddeshwor Secondary School 2026. All Rights Reserved : Powered By TechInfosys</p>
        </div>
      </div>
    </footer>
    <a class="float-call" href="tel:01-4622730" aria-label="Call school">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h2.2a1 1 0 01.96.73l1.1 4a1 1 0 01-.27 1L7.9 10.1a12 12 0 006 6l1.37-1.1a1 1 0 011-.27l4 1.1a1 1 0 01.73.96V19a2 2 0 01-2 2h-1C9.7 21 3 14.3 3 6V5z"/></svg>
    </a>
    <button class="to-top" id="toTop" aria-label="Scroll to top">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 15l7-7 7 7"/></svg>
    </button>
    <div class="lb" id="lightbox">
      <button class="close" id="lbClose" aria-label="Close">&times;</button>
      <button class="nav prev" id="lbPrev" aria-label="Previous">‹</button>
      <img alt="">
      <button class="nav next" id="lbNext" aria-label="Next">›</button>
      <div class="count" id="lbCount"></div>
    </div>
    <div class="toast-wrap"><div class="toast" id="toast"></div></div>
    <button class="suggest-fab" id="suggestFab" type="button" aria-haspopup="dialog">
      <span class="bulb">S</span><span data-i18n="suggest">${t("suggest")}</span>
    </button>
    <div class="suggest-drawer" id="suggestDrawer" role="dialog" aria-label="Suggestion desk">
      <div class="scrim" id="suggestScrim"></div>
      <div class="suggest-panel">
        <button class="close-x" id="suggestClose" type="button" aria-label="Close">×</button>
        <p class="eyebrow" data-i18n="suggest">${t("suggest")}</p>
        <h2 data-i18n="suggestTitle">${t("suggestTitle")}</h2>
        <p class="muted" style="margin-bottom:16px" data-i18n="suggestLead">${t("suggestLead")}</p>
        <form id="drawerSuggest" data-success="Thank you. Your suggestion has reached the school office.">
          <div class="field"><label data-i18n="suggestName">${t("suggestName")} <span class="req">*</span></label><input name="name" required></div>
          <div class="field" style="margin-top:10px"><label data-i18n="suggestRole">${t("suggestRole")}</label>
            <select name="role"><option>Parent</option><option>Student</option><option>Staff</option><option>Alumni</option><option>Community</option></select>
          </div>
          <div class="field" style="margin-top:10px"><label>Email</label><input type="email" name="email"></div>
          <div class="field" style="margin-top:10px"><label>Topic</label>
            <div class="chip-row">
              <label><input type="radio" name="category" value="General" checked><span>General</span></label>
              <label><input type="radio" name="category" value="Academics"><span>Academics</span></label>
              <label><input type="radio" name="category" value="Facilities"><span>Facilities</span></label>
              <label><input type="radio" name="category" value="Events"><span>Events</span></label>
              <label><input type="radio" name="category" value="Safety"><span>Safety</span></label>
            </div>
          </div>
          <div class="field" style="margin-top:4px"><label data-i18n="suggestMsg">${t("suggestMsg")} <span class="req">*</span></label>
            <textarea name="message" rows="5" required maxlength="800"></textarea>
          </div>
          <label class="check"><input type="checkbox" name="anonymous" value="1"> Keep my name off the public board</label>
          <button class="btn" type="submit" style="width:100%;margin-top:8px" data-i18n="suggestSend">${t("suggestSend")}</button>
          <div class="alert"></div>
        </form>
        <p class="small" style="margin-top:14px"><a class="link-red" href="${href("suggest/index.html")}">Open full suggestion desk →</a></p>
      </div>
    </div>
  `;

  const mountH = document.getElementById("site-header");
  const mountF = document.getElementById("site-footer");
  if (mountH) mountH.outerHTML = header;
  if (mountF) mountF.outerHTML = footer;
  const mainEl = document.querySelector("main");
  if (mainEl && !mainEl.id) mainEl.id = "main-content";

  function applyLang() {
    document.documentElement.lang = lang === "ne" ? "ne" : "en";
    document.querySelectorAll("[data-i18n]").forEach(el => {
      const k = el.getAttribute("data-i18n");
      if (!(I18N[lang] && I18N[lang][k])) return;
      if (el.children.length) {
        const first = el.childNodes[0];
        if (first && first.nodeType === 3) first.textContent = I18N[lang][k] + " ";
        else el.prepend(I18N[lang][k] + " ");
      } else {
        el.textContent = I18N[lang][k];
      }
    });
    const inp = document.getElementById("searchInput");
    if (inp) inp.placeholder = t("searchPh");
    const btn = document.getElementById("langBtn");
    if (btn) btn.textContent = lang === "ne" ? "English" : "नेपाली";
  }
  applyLang();

  document.getElementById("langBtn")?.addEventListener("click", () => {
    lang = lang === "ne" ? "en" : "ne";
    localStorage.setItem("ssn_lang", lang);
    applyLang();
  });

  const menuBtn = document.getElementById("menuBtn");
  const mobileNav = document.getElementById("mobileNav");
  if (menuBtn && mobileNav) {
    menuBtn.addEventListener("click", () => {
      const open = mobileNav.classList.toggle("open");
      document.body.classList.toggle("nav-open", open);
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
      menuBtn.innerHTML = open
        ? '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>'
        : '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>';
    });
  }

  const moreBtn = document.getElementById("moreBtn");
  const moreMenu = document.getElementById("moreMenu");
  moreBtn?.addEventListener("click", (e) => {
    e.stopPropagation();
    moreBtn.parentElement.classList.toggle("open");
  });
  document.addEventListener("click", () => moreBtn?.parentElement.classList.remove("open"));

  const headerEl = document.getElementById("siteHeader");
  window.addEventListener("scroll", () => {
    headerEl?.classList.toggle("compact", window.scrollY > 40);
    document.getElementById("toTop")?.classList.toggle("show", window.scrollY > 400);
  });
  document.getElementById("toTop")?.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

  const drawer = document.getElementById("suggestDrawer");
  const openSuggest = () => drawer?.classList.add("open");
  const closeSuggest = () => drawer?.classList.remove("open");
  document.getElementById("suggestFab")?.addEventListener("click", openSuggest);
  document.getElementById("suggestClose")?.addEventListener("click", closeSuggest);
  document.getElementById("suggestScrim")?.addEventListener("click", closeSuggest);
  if (PAGE === "suggest") document.getElementById("suggestFab")?.style && (document.getElementById("suggestFab").style.display = "none");

  /* Search */
  const modal = document.getElementById("searchModal");
  const sInput = document.getElementById("searchInput");
  const sResults = document.getElementById("searchResults");
  function openSearch() {
    modal?.classList.add("open");
    setTimeout(() => sInput?.focus(), 30);
  }
  function closeSearch() { modal?.classList.remove("open"); }
  document.getElementById("searchBtn")?.addEventListener("click", openSearch);
  modal?.addEventListener("click", (e) => { if (e.target === modal) closeSearch(); });
  document.addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") { e.preventDefault(); openSearch(); }
    if (e.key === "Escape") {
      closeSearch();
      closeSuggest();
      moreBtn?.parentElement.classList.remove("open");
      if (mobileNav?.classList.contains("open")) menuBtn?.click();
    }
  });
  let sTimer;
  sInput?.addEventListener("input", () => {
    clearTimeout(sTimer);
    const q = sInput.value.trim();
    if (q.length < 2) { sResults.innerHTML = '<div class="search-empty">Type at least 2 characters</div>'; return; }
    if (NO_BACKEND) {
      sResults.innerHTML = '<div class="search-empty">Search needs the live site — this is a static copy. Please visit the live school website to search news, staff and pages.</div>';
      return;
    }
    sTimer = setTimeout(async () => {
      try {
        const data = await fetch(api("/api/search?q=" + encodeURIComponent(q))).then(r => r.json());
        const bits = [];
        (data.pages || []).forEach(p => bits.push(`<a href="${BASE}${p.path.replace(/^\/+/, "")}/index.html"><div><div class="k">Page</div><strong>${p.title}</strong><div class="small">${p.hint}</div></div></a>`));
        (data.news || []).forEach(n => bits.push(`<a href="${BASE}news/${n.slug}/index.html"><img src="${escAttr(n.cover)}" alt=""><div><div class="k">News</div><strong>${n.title}</strong><div class="small">${n.date_bs}</div></div></a>`));
        (data.staff || []).forEach(s => bits.push(`<a href="${BASE}family/index.html"><img src="${escAttr(s.image || "")}" alt=""><div><div class="k">Staff</div><strong>${s.name}</strong><div class="small">${s.role}${s.subject ? " · " + s.subject : ""}</div></div></a>`));
        sResults.innerHTML = bits.join("") || '<div class="search-empty">No matches</div>';
      } catch {
        sResults.innerHTML = '<div class="search-empty">Search unavailable</div>';
      }
    }, 180);
  });

  /* Clock */
  const NP_MONTHS = ["बैशाख","जेठ","असार","साउन","भदौ","असोज","कात्तिक","मंसिर","पुष","माघ","फागुन","चैत"];
  const NP_DAYS = ["आइतबार","सोमबार","मंगलबार","बुधबार","बिहिबार","शुक्रबार","शनिबार"];
  const NP_NUM = ["०","१","२","३","४","५","६","७","८","९"];
  function toNp(n) { return String(n).split("").map(c => /\d/.test(c) ? NP_NUM[+c] : c).join(""); }
  function pad(n) { return String(n).padStart(2, "0"); }
  const BS_LENGTHS = [31,31,32,32,31,30,30,30,29,29,30,30];
  const BS_EPOCH = Date.UTC(2026, 3, 14);
  function toBS(date) {
    const utc = Date.UTC(date.getFullYear(), date.getMonth(), date.getDate());
    let dayDiff = Math.floor((utc - BS_EPOCH) / 86400000);
    let year = 2083;
    const lens = BS_LENGTHS.slice();
    if (dayDiff < 0) {
      const prev = [31,32,31,32,31,30,30,30,29,29,30,30];
      return fromDiff(2082, dayDiff + prev.reduce((a,b)=>a+b,0), prev);
    }
    while (dayDiff >= lens.reduce((a,b)=>a+b,0)) { dayDiff -= lens.reduce((a,b)=>a+b,0); year += 1; }
    return fromDiff(year, dayDiff, lens);
  }
  function fromDiff(year, dayDiff, lens) {
    let month = 0;
    while (month < 12 && dayDiff >= lens[month]) { dayDiff -= lens[month]; month++; }
    return { year, month, day: dayDiff + 1 };
  }
  function tickClock() {
    const el = document.getElementById("npClock");
    if (!el) return;
    const now = new Date();
    const bs = toBS(now);
    const h = now.getHours();
    const period = h >= 4 && h < 12 ? "बिहान" : h >= 12 && h < 16 ? "दिउँसो" : h >= 16 && h < 20 ? "बेलुका" : "राति";
    const time = `${toNp(pad(h % 12 || 12))}:${toNp(pad(now.getMinutes()))}:${toNp(pad(now.getSeconds()))} ${period}`;
    const en = now.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric", timeZone: "Asia/Kathmandu" });
    el.innerHTML = `${NP_MONTHS[bs.month]} ${toNp(bs.day)}, ${NP_DAYS[now.getDay()]} <span style="opacity:.7">|</span> ${en} <span style="opacity:.7">|</span> ${time}`;
  }
  tickClock();
  setInterval(tickClock, 1000);

  /* Toast */
  function toast(msg) {
    const el = document.getElementById("toast");
    if (!el) { alert(msg); return; }
    el.textContent = msg;
    el.classList.add("show");
    setTimeout(() => el.classList.remove("show"), 3200);
  }

  /* Reveal */
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add("in"); });
  }, { threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach(el => io.observe(el));

  /* Hero */
  const slides = document.querySelectorAll(".hero-slide");
  const dots = document.querySelectorAll(".dots button");
  let hi = 0, heroTimer;
  function showHero(i) {
    if (!slides.length) return;
    hi = (i + slides.length) % slides.length;
    slides.forEach((s, n) => s.classList.toggle("active", n === hi));
    dots.forEach((d, n) => d.classList.toggle("active", n === hi));
  }
  function restartHero() {
    clearInterval(heroTimer);
    if (slides.length) heroTimer = setInterval(() => showHero(hi + 1), 5000);
  }
  dots.forEach((d, n) => d.addEventListener("click", () => { showHero(n); restartHero(); }));
  document.getElementById("heroPrev")?.addEventListener("click", () => { showHero(hi - 1); restartHero(); });
  document.getElementById("heroNext")?.addEventListener("click", () => { showHero(hi + 1); restartHero(); });
  restartHero();

  /* Carousels */
  document.querySelectorAll("[data-carousel]").forEach(wrap => {
    const track = wrap.querySelector(".carousel-track");
    const items = wrap.querySelectorAll(".slide-item");
    let i = 0;
    function perView() {
      if (window.innerWidth <= 720) return 1;
      if (window.innerWidth <= 1024) return 2;
      return parseInt(wrap.dataset.per || "4", 10);
    }
    function go(dir) {
      const pv = perView();
      const max = Math.max(0, items.length - pv);
      i = Math.min(max, Math.max(0, i + dir));
      track.style.transform = `translateX(-${i * (100 / pv)}%)`;
    }
    wrap.querySelector(".car-btn.prev")?.addEventListener("click", () => go(-1));
    wrap.querySelector(".car-btn.next")?.addEventListener("click", () => go(1));
    window.addEventListener("resize", () => go(0));
  });

  /* Counters */
  document.querySelectorAll("[data-count]").forEach(el => {
    const target = parseFloat(el.dataset.count);
    const suffix = el.dataset.suffix || "";
    const dec = el.dataset.dec ? parseInt(el.dataset.dec, 10) : 0;
    let started = false;
    const run = () => {
      if (started) return;
      started = true;
      const t0 = performance.now();
      const step = (tnow) => {
        const p = Math.min(1, (tnow - t0) / 1400);
        const val = target * (1 - Math.pow(1 - p, 3));
        el.textContent = (dec ? val.toFixed(dec) : Math.round(val)) + suffix;
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    new IntersectionObserver(es => es.forEach(e => e.isIntersecting && run()), { threshold: 0.4 }).observe(el);
  });

  /* Forms */
  function showAlert(form, text, ok) {
    const box = form.querySelector(".alert") || (() => {
      const a = document.createElement("div");
      a.className = "alert";
      form.appendChild(a);
      return a;
    })();
    box.textContent = text;
    box.style.background = ok ? "#ecfdf5" : "#fef2f2";
    box.style.color = ok ? "#065f46" : "#991b1b";
    box.classList.add("show");
  }
  async function postJSON(url, body) {
    const res = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.error || data.detail || "Request failed");
    return data;
  }
  document.querySelectorAll("form[data-success]").forEach(form => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = form.querySelector("button[type=submit]");
      if (btn) { btn.disabled = true; btn.dataset.old = btn.textContent; btn.textContent = "Sending…"; }
      const payload = {};
      form.querySelectorAll("[name]").forEach(el => {
        if (!el.name) return;
        if (el.type === "checkbox") payload[el.name] = el.checked ? (el.value || "1") : "";
        else if (el.type === "radio") { if (el.checked) payload[el.name] = el.value; }
        else payload[el.name] = el.value;
      });
      try {
        const url = PAGE === "apply" ? "/api/apply"
          : PAGE === "contact" ? "/api/contact"
          : (PAGE === "suggest" || form.id === "homeSuggest" || form.id === "drawerSuggest") ? "/api/suggest"
          : null;
        if (url) {
          if (NO_BACKEND) {
            showAlert(form, "This form needs the live site — this is a static copy. Please visit the live school website to submit.", false);
          } else {
            const data = await postJSON(api(url), payload);
            const msg = data.message || form.dataset.success;
            showAlert(form, msg, true);
            toast(msg);
            if (form.id === "drawerSuggest") setTimeout(closeSuggest, 1400);
            form.reset();
          }
        } else {
          showAlert(form, form.dataset.success, true);
          form.reset();
        }
      } catch (err) {
        showAlert(form, err.message || "Something went wrong. Please try again or email us directly.", false);
      } finally {
        if (btn) { btn.disabled = false; btn.textContent = btn.dataset.old || "Submit"; }
      }
    });
  });
  document.getElementById("newsForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = e.target.querySelector("input[type=email]")?.value || "";
    try {
      if (NO_BACKEND) {
        toast("The newsletter needs the live site — this is a static copy.");
        return;
      }
      const data = await postJSON(api("/api/newsletter"), { email });
      toast(data.message);
      e.target.reset();
    } catch (err) { toast(err.message || "Could not subscribe"); }
  });

  /* Lightbox with prev/next */
  const lb = document.getElementById("lightbox");
  const lbImg = lb?.querySelector("img");
  let lbList = [], lbI = 0;
  function openLb(i) {
    if (!lbList.length) return;
    lbI = (i + lbList.length) % lbList.length;
    const it = lbList[lbI];
    lbImg.src = it.url;
    lbImg.alt = it.alt || "";
    document.getElementById("lbCount").textContent = `${lbI + 1} / ${lbList.length}`;
    lb.classList.add("open");
  }
  function collectLb(startEl) {
    const group = startEl.closest(".gallery, .gallery-grid, main") || document;
    const nodes = [...group.querySelectorAll("[data-lb]")];
    lbList = nodes.map(a => ({ url: a.getAttribute("href") || a.querySelector("img")?.src, alt: a.querySelector("img")?.alt || "" }));
    return Math.max(0, nodes.indexOf(startEl));
  }
  document.querySelectorAll("[data-lb]").forEach(a => {
    a.addEventListener("click", (e) => { e.preventDefault(); openLb(collectLb(a)); });
  });
  document.getElementById("lbClose")?.addEventListener("click", () => lb.classList.remove("open"));
  document.getElementById("lbPrev")?.addEventListener("click", () => openLb(lbI - 1));
  document.getElementById("lbNext")?.addEventListener("click", () => openLb(lbI + 1));
  lb?.addEventListener("click", (e) => { if (e.target === lb) lb.classList.remove("open"); });
  document.addEventListener("keydown", (e) => {
    if (!lb?.classList.contains("open")) return;
    if (e.key === "Escape") lb.classList.remove("open");
    if (e.key === "ArrowLeft") openLb(lbI - 1);
    if (e.key === "ArrowRight") openLb(lbI + 1);
  });

  /* FAQ accordion */
  document.querySelectorAll(".faq-item button").forEach(btn => {
    btn.addEventListener("click", () => btn.parentElement.classList.toggle("open"));
  });

  /* Staff filters */
  const filterBar = document.getElementById("staffFilters");
  if (filterBar) {
    filterBar.addEventListener("click", (e) => {
      const b = e.target.closest("button");
      if (!b) return;
      filterBar.querySelectorAll("button").forEach(x => x.classList.toggle("on", x === b));
      const key = b.dataset.filter;
      document.querySelectorAll("[data-dept]").forEach(sec => {
        sec.style.display = (key === "all" || sec.dataset.dept === key) ? "" : "none";
      });
    });
  }

  /* News search (client) */
  const newsQ = document.getElementById("newsSearch");
  if (newsQ) {
    newsQ.addEventListener("input", () => {
      const q = newsQ.value.toLowerCase();
      document.querySelectorAll(".news-tile").forEach(card => {
        card.style.display = card.textContent.toLowerCase().includes(q) ? "" : "none";
      });
    });
  }

  /* Hydrate FAQ from API */
  const faqRoot = document.getElementById("faqRoot");
  if (faqRoot && !faqRoot.children.length && !NO_BACKEND) {
    fetch(api("/api/faq")).then(r => r.json()).then(items => {
      faqRoot.innerHTML = items.map(f => `<div class="faq-item"><button type="button">${f.question}<span>+</span></button><div class="a">${f.answer}</div></div>`).join("");
      faqRoot.querySelectorAll(".faq-item button").forEach(btn => {
        btn.addEventListener("click", () => btn.parentElement.classList.toggle("open"));
      });
    }).catch(() => {});
  }

  /* Gallery: API first, bundled JSON on static hosts; baked-in photos stay */
  function escAttr(s) {
    return String(s || "").replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
  }
  function renderGallery(root, items) {
    if (!Array.isArray(items) || !items.length) return false;
    root.innerHTML = items.map(it => {
      const url = escAttr(resolveAsset(it.url));
      const alt = escAttr(it.alt);
      const cat = escAttr(it.category || "News");
      return `<a href="${url}" data-lb data-cat="${cat}" data-cap="${alt}"><img src="${url}" alt="${alt}" loading="lazy"></a>`;
    }).join("");
    return true;
  }
  const galRoot = document.getElementById("galleryRoot");
  if (galRoot) {
    const hasStatic = galRoot.querySelector("[data-lb]");
    (async () => {
      const tries = NO_BACKEND
        ? [BASE + "assets/data/gallery.json"]
        : [api("/api/gallery"), BASE + "assets/data/gallery.json", "/assets/data/gallery.json"];
      for (const url of tries) {
        try {
          const r = await fetch(url);
          if (!r.ok) continue;
          const items = await r.json();
          if (renderGallery(galRoot, items)) {
            galRoot.querySelectorAll("[data-lb]").forEach(a => {
              a.addEventListener("click", (e) => { e.preventDefault(); openLb(collectLb(a)); });
            });
            break;
          }
        } catch (_) { /* try next source */ }
      }
      if (!galRoot.querySelector("[data-lb]") && !hasStatic) {
        galRoot.innerHTML = "<p class='muted'>Photos will appear here when the school gallery is available.</p>";
      }
    })();
    const galFilters = document.getElementById("galleryFilters");
    galFilters?.addEventListener("click", (e) => {
      const b = e.target.closest("button");
      if (!b) return;
      galFilters.querySelectorAll("button").forEach(x => x.classList.toggle("on", x === b));
      const key = b.dataset.filter;
      galRoot.querySelectorAll("[data-cat]").forEach(a => {
        a.style.display = (key === "all" || a.dataset.cat === key) ? "" : "none";
      });
    });
  }

  /* Notice ticker on home (live site only — no backend on static hosts) */
  if (PAGE === "home" && !NO_BACKEND) {
    fetch(api("/api/news")).then(r => r.json()).then(items => {
      if (!items.length) return;
      const bar = document.createElement("div");
      bar.className = "ticker";
      const links = items.slice(0, 6).map(n =>
        `<a class="ticker-item" href="${BASE}news/${n.slug}/index.html">${n.title}<span> — ${n.date_bs}</span></a><span class="ticker-sep" aria-hidden="true">·</span>`
      ).join("");
      bar.innerHTML = `<span class="ticker-label">Latest news</span><div class="ticker-track"><div class="ticker-inner"><div class="ticker-set">${links}</div><div class="ticker-set" aria-hidden="true">${links}</div></div></div>`;
      const header = document.getElementById("siteHeader");
      header?.insertAdjacentElement("afterend", bar);
    }).catch(() => {});
  }

  /* Image fallbacks */
  document.querySelectorAll("img").forEach(img => {
    img.addEventListener("error", () => {
      if (img.dataset.fallback) return;
      img.dataset.fallback = "1";
      img.src = BASE + "assets/img/SiddeshworLogo.png";
      img.style.objectFit = "contain";
      img.style.background = "#f3f4f6";
    });
  });

  const readBar = document.createElement("div");
  readBar.className = "read-bar";
  document.body.appendChild(readBar);
  const onRead = () => {
    const h = document.documentElement;
    const max = h.scrollHeight - h.clientHeight;
    readBar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + "%";
  };
  window.addEventListener("scroll", onRead, { passive: true });
  onRead();

  const article = document.querySelector(".article");
  if (article) {
    const share = document.createElement("div");
    share.className = "share-bar";
    const shareUrl = encodeURIComponent(location.href);
    const shareTitle = encodeURIComponent(document.title);
    share.innerHTML = '<span>Share</span><button type="button" id="copyLink">Copy link</button><a href="https://www.facebook.com/sharer/sharer.php?u=' + shareUrl + '" target="_blank" rel="noopener">Facebook</a><a href="https://wa.me/?text=' + shareTitle + '%20' + shareUrl + '" target="_blank" rel="noopener">WhatsApp</a>';
    article.querySelector("h1")?.insertAdjacentElement("afterend", share);
    document.getElementById("copyLink")?.addEventListener("click", async () => {
      try { await navigator.clipboard.writeText(location.href); toast("Link copied"); }
      catch { toast(location.href); }
    });
    if (!NO_BACKEND) {
      fetch(api("/api/news")).then(r => r.json()).then(items => {
        const here = location.pathname;
        const others = (items || []).filter(n => !here.includes(n.slug)).slice(0, 3);
        if (!others.length) return;
        const box = document.createElement("div");
        box.className = "related";
        box.innerHTML = "<h2 class='h2'>More from the campus</h2><div class='related-grid'>" +
          others.map(n => '<a class="news-tile" href="' + BASE + 'news/' + n.slug + '/index.html"><div class="thumb"><img src="' + n.cover + '" alt=""></div><div class="pad"><p class="date-red">' + (n.date_bs || "") + '</p><h3>' + n.title + '</h3></div></a>').join("") +
          "</div>";
        article.appendChild(box);
      }).catch(() => {});
    }
  }

  const staffQ = document.getElementById("staffSearch");
  if (staffQ) {
    staffQ.addEventListener("input", () => {
      const q = staffQ.value.toLowerCase().trim();
      document.querySelectorAll(".person").forEach(card => {
        card.style.display = !q || card.textContent.toLowerCase().includes(q) ? "" : "none";
      });
    });
  }

  document.querySelectorAll(".gallery-grid a[data-lb]").forEach(a => {
    const alt = a.querySelector("img")?.alt;
    if (alt && !a.getAttribute("data-cap")) a.setAttribute("data-cap", alt);
  });

  document.querySelectorAll("form[data-success] textarea[name=message]").forEach(ta => {
    if (ta.parentElement.querySelector(".char-count")) return;
    const n = document.createElement("div");
    n.className = "char-count";
    ta.insertAdjacentElement("afterend", n);
    const tick = () => { n.textContent = ta.value.length + " / " + (ta.maxLength > 0 ? ta.maxLength : 800); };
    ta.addEventListener("input", tick);
    tick();
  });

  const ideaBoard = document.getElementById("ideaBoard");
  if (ideaBoard) {
    if (NO_BACKEND) {
      ideaBoard.innerHTML = "<p class='muted center'>The public idea board needs the live site — this static copy does not show live office updates.</p>";
    } else {
      fetch(api("/api/suggestions/public")).then(r => r.json()).then(items => {
        if (!Array.isArray(items) || !items.length) {
          ideaBoard.innerHTML = "<p class='muted center'>Public ideas will appear here when the office marks them.</p>";
          return;
        }
        ideaBoard.innerHTML = items.map(it => {
          const label = it.status === "done" ? "We did this" : "Looking into it";
          return '<article class="idea-card ' + it.status + '"><span class="idea-tag">' + it.category + "</span><p>" + it.title + "</p><strong>" + label + "</strong></article>";
        }).join("");
      }).catch(() => {});
    }
  }

  /* Notice board: render managed notices from the API, keeping the baked-in
     routine pages as a static fallback when the backend is unavailable. */
  const noticeRoot = document.getElementById("noticeRoot");
  if (noticeRoot && PAGE === "notice") {
    const renderNotice = (n) => {
      const page = Number(n.page_num) || 1;
      const img = resolveAsset(n.image);
      const title = String(n.title || "").trim();
      const alt = title || ("Routine Page " + page);
      const isDefault = /^(routine )?page \d+$/i.test(title);
      const note = title && !isDefault
        ? `<p class="routine-note">${escAttr(title)}</p>`
        : "";
      return `<div class="routine"><h3>Page ${page}</h3><img src="${escAttr(img)}" alt="${escAttr(alt)}" loading="lazy">${note}</div>`;
    };
    if (!NO_BACKEND) {
      fetch(api("/api/notices")).then(r => {
        if (!r.ok) throw new Error("http " + r.status);
        return r.json();
      }).then(items => {
        if (!Array.isArray(items) || !items.length) return; // keep fallback pages
        noticeRoot.innerHTML = items.map(renderNotice).join("");
      }).catch(() => { /* keep the baked-in routine pages */ });
    }
  }
})();
