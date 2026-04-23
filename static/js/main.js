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
    if (target.tagName === "A" || target.classList.contains("technique-item")) {
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
    if (target.tagName === "A" || target.classList.contains("technique-item")) {
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

const nav = document.querySelector("nav");
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
