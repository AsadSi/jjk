const cursor = document.getElementById("cursor");
const cursorRing = document.getElementById("cursor-ring");

let mouseX = 0;
let mouseY = 0;
let ringX = 0;
let ringY = 0;

document.addEventListener("mousemove", (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
  if (cursor) {
    cursor.style.left = `${mouseX}px`;
    cursor.style.top = `${mouseY}px`;
  }
});

function animateRing() {
  ringX += (mouseX - ringX) * 0.12;
  ringY += (mouseY - ringY) * 0.12;
  if (cursorRing) {
    cursorRing.style.left = `${ringX}px`;
    cursorRing.style.top = `${ringY}px`;
  }
  requestAnimationFrame(animateRing);
}
requestAnimationFrame(animateRing);

document.addEventListener(
  "mouseenter",
  (e) => {
    const target = e.target;
    if (!(target instanceof HTMLElement) || !cursor || !cursorRing) return;
    if (
      target.tagName === "A" ||
      target.classList.contains("technique-item") ||
      target.classList.contains("theme-toggle")
    ) {
      cursor.style.width = "6px";
      cursor.style.height = "6px";
      cursorRing.style.width = "56px";
      cursorRing.style.height = "56px";
      cursorRing.style.opacity = "0.2";
    }
  },
  true
);

document.addEventListener(
  "mouseleave",
  (e) => {
    const target = e.target;
    if (!(target instanceof HTMLElement) || !cursor || !cursorRing) return;
    if (
      target.tagName === "A" ||
      target.classList.contains("technique-item") ||
      target.classList.contains("theme-toggle")
    ) {
      cursor.style.width = "10px";
      cursor.style.height = "10px";
      cursorRing.style.width = "36px";
      cursorRing.style.height = "36px";
      cursorRing.style.opacity = "0.4";
    }
  },
  true
);

const revealElements = document.querySelectorAll(".reveal");
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.classList.add("visible");
        }, i * 80);
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.1, rootMargin: "0px 0px -60px 0px" }
);
revealElements.forEach((el) => observer.observe(el));

const bgText = document.querySelector(".hero-bg-text");
window.addEventListener("scroll", () => {
  if (bgText) {
    bgText.style.transform = `translate(-50%, calc(-50% + ${window.scrollY * 0.3}px))`;
  }
});

const nav = document.querySelector("nav.site-nav");
const navAnchors = document.querySelectorAll('.nav-links a[href^="#"]');
const sectionIds = [...navAnchors]
  .map((link) => link.getAttribute("href"))
  .filter((href) => href && href.startsWith("#"))
  .map((href) => href.slice(1));
const trackedSections = sectionIds
  .map((id) => document.getElementById(id))
  .filter((el) => el instanceof HTMLElement);

function updateNavState() {
  if (nav) {
    nav.classList.toggle("nav-scrolled", window.scrollY > 20);
  }
}

function markActiveLink(activeId) {
  navAnchors.forEach((link) => {
    const href = link.getAttribute("href");
    link.classList.toggle("active", href === `#${activeId}`);
  });
}

if (trackedSections.length > 0) {
  const navObserver = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (visible?.target?.id) {
        markActiveLink(visible.target.id);
      }
    },
    { threshold: 0.25, rootMargin: "-35% 0px -45% 0px" }
  );
  trackedSections.forEach((section) => navObserver.observe(section));
}

updateNavState();
window.addEventListener("scroll", updateNavState);

/* Theme (light / JJK dark) */
const metaThemeColor = document.getElementById("meta-theme-color");
const themeToggle = document.getElementById("theme-toggle");

function currentTheme() {
  return document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
}

function applyThemeMeta(theme) {
  if (metaThemeColor) {
    metaThemeColor.setAttribute("content", theme === "dark" ? "#0b0a0d" : "#fafaf7");
  }
}

function syncThemeToggleLabel() {
  if (!themeToggle) return;
  const isDark = currentTheme() === "dark";
  themeToggle.setAttribute("aria-label", isDark ? "Switch to light theme" : "Switch to dark theme");
  themeToggle.setAttribute("title", isDark ? "Light theme" : "Dark theme");
}

function setTheme(theme) {
  if (theme !== "light" && theme !== "dark") return;
  document.documentElement.setAttribute("data-theme", theme);
  try {
    localStorage.setItem("jjk-theme", theme);
  } catch (e) {
    /* ignore */
  }
  applyThemeMeta(theme);
  syncThemeToggleLabel();
}

if (themeToggle) {
  themeToggle.addEventListener("click", () => {
    setTheme(currentTheme() === "dark" ? "light" : "dark");
  });
}
syncThemeToggleLabel();
applyThemeMeta(currentTheme());

/* Mobile nav dropdown */
const navToggle = document.getElementById("site-nav-toggle");
function setNavOpen(open) {
  if (!nav) return;
  nav.classList.toggle("nav-open", open);
  document.body.classList.toggle("nav-menu-open", open);
  if (navToggle) {
    navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    navToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  }
}

function closeNav() {
  setNavOpen(false);
}

if (navToggle && nav) {
  navToggle.addEventListener("click", () => {
    setNavOpen(!nav.classList.contains("nav-open"));
  });
  nav.querySelectorAll(".nav-links a").forEach((link) => {
    link.addEventListener("click", () => {
      if (window.matchMedia("(max-width: 767px)").matches) closeNav();
    });
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeNav();
  });
  document.addEventListener("click", (e) => {
    if (!nav.classList.contains("nav-open")) return;
    const t = e.target;
    if (!(t instanceof Node)) return;
    if (!nav.contains(t)) closeNav();
  });
}

/* Characters registry: filter without full page reload */
const registryRoot = document.getElementById("character-registry");
if (registryRoot) {
  const form = document.getElementById("registry-filter-form");
  const searchInput = document.getElementById("registry-search");
  const affiliationSelect = document.getElementById("registry-affiliation");
  const clearBtn = document.getElementById("registry-clear");
  const grid = document.getElementById("registry-grid");
  const filterStatus = document.getElementById("registry-filter-status");
  const resultNum = document.getElementById("registry-result-num");
  const tagSearch = document.getElementById("registry-tag-search");
  const tagAff = document.getElementById("registry-tag-aff");
  const emptyState = document.getElementById("registry-empty");
  const showAllBtn = document.getElementById("registry-show-all");

  const cards = grid ? [...grid.querySelectorAll("[data-slug].character-card")] : [];

  function cardMatches(el, searchLower, affiliation) {
    const name = (el.dataset.name || "").toLowerCase();
    const jp = (el.dataset.jp || "").toLowerCase();
    if (searchLower) {
      if (!name.includes(searchLower) && !jp.includes(searchLower)) return false;
    }
    if (affiliation) {
      const affPart = affiliation.toLowerCase();
      const list = (el.dataset.affiliations || "")
        .split("|")
        .map((s) => s.trim())
        .filter(Boolean);
      if (!list.some((a) => a.toLowerCase().includes(affPart))) return false;
    }
    return true;
  }

  function pushRegistryUrl(searchRaw, affiliation) {
    const params = new URLSearchParams();
    if (searchRaw.trim()) params.set("search", searchRaw.trim());
    if (affiliation) params.set("affiliation", affiliation);
    const qs = params.toString();
    const next = qs ? `/characters?${qs}` : "/characters";
    window.history.replaceState({}, "", next);
  }

  let searchDebounce;

  function applyFilters(syncUrl = true) {
    const searchRaw = searchInput?.value ?? "";
    const searchLower = searchRaw.trim().toLowerCase();
    const affiliation = affiliationSelect?.value ?? "";

    let visible = 0;
    cards.forEach((card) => {
      const ok = cardMatches(card, searchLower, affiliation);
      card.classList.toggle("character-card--hidden", !ok);
      if (ok) visible += 1;
    });

    if (resultNum) resultNum.textContent = String(visible);

    const hasFilter = Boolean(searchRaw.trim() || affiliation);
    if (filterStatus) filterStatus.hidden = !hasFilter;
    if (clearBtn) clearBtn.hidden = !hasFilter;

    if (tagSearch) {
      tagSearch.hidden = !searchRaw.trim();
      tagSearch.textContent = searchRaw.trim() ? `Search: "${searchRaw.trim()}"` : "";
    }
    if (tagAff) {
      tagAff.hidden = !affiliation;
      tagAff.textContent = affiliation ? `Affiliation: ${affiliation}` : "";
    }

    if (emptyState) emptyState.hidden = visible > 0 || cards.length === 0;

    if (syncUrl) pushRegistryUrl(searchRaw, affiliation);
  }

  function scheduleApply() {
    clearTimeout(searchDebounce);
    searchDebounce = setTimeout(() => applyFilters(true), 280);
  }

  searchInput?.addEventListener("input", scheduleApply);
  affiliationSelect?.addEventListener("change", () => applyFilters(true));

  form?.addEventListener("submit", (e) => {
    e.preventDefault();
    applyFilters(true);
  });

  clearBtn?.addEventListener("click", () => {
    if (searchInput) searchInput.value = "";
    if (affiliationSelect) affiliationSelect.value = "";
    applyFilters(true);
  });

  showAllBtn?.addEventListener("click", () => clearBtn?.click());

  window.addEventListener("popstate", () => {
    const params = new URLSearchParams(window.location.search);
    if (searchInput) searchInput.value = params.get("search") || "";
    if (affiliationSelect) affiliationSelect.value = params.get("affiliation") || "";
    applyFilters(false);
  });

  applyFilters(true);
}

const kanjiLayer = document.getElementById("kanji-bg");
const kanjiPool = ["呪", "術", "廻", "戦", "領", "域", "展", "開", "式", "霊", "影", "無", "量", "空", "黒", "閃", "斬", "祓"];

function placeKanjiGlyph(glyph) {
  const char = kanjiPool[Math.floor(Math.random() * kanjiPool.length)];
  glyph.textContent = char;
  glyph.style.left = `${Math.random() * 94}%`;
  glyph.style.top = `${Math.random() * 88}%`;
  glyph.style.fontSize = `${Math.floor(Math.random() * 36) + 28}px`;
  glyph.style.animationDuration = `${Math.floor(Math.random() * 6) + 8}s`;
}

if (kanjiLayer) {
  const glyphCount = 18;
  for (let i = 0; i < glyphCount; i += 1) {
    const glyph = document.createElement("span");
    glyph.className = "kanji-glyph";
    placeKanjiGlyph(glyph);
    // Staggered positive delays preserve smooth fade-in on first load.
    glyph.style.animationDelay = `${(Math.random() * 4).toFixed(2)}s`;
    // Reposition only when a cycle completes to avoid visual popping.
    glyph.addEventListener("animationiteration", () => {
      placeKanjiGlyph(glyph);
    });
    kanjiLayer.appendChild(glyph);
  }
}
