/* Les Garçons Glaciers — interactions (vanilla, sans dépendance) */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Année automatique (audit : « © 2025 » figé) */
  $$("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));

  /* En-tête : filet uniquement une fois qu'on a défilé */
  const header = $(".header");
  if (header) {
    const onScroll = () => header.classList.toggle("is-scrolled", scrollY > 8);
    onScroll();
    addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------------- Menu mobile ---------------- */
  const drawer = $("#drawer");
  const openBtn = $("[data-open-menu]");
  if (drawer && openBtn) {
    const close = () => {
      drawer.classList.remove("is-open");
      document.body.classList.remove("no-scroll");
      openBtn.setAttribute("aria-expanded", "false");
      drawer.setAttribute("aria-hidden", "true");
      openBtn.focus({ preventScroll: true });
    };
    openBtn.addEventListener("click", () => {
      drawer.classList.add("is-open");
      document.body.classList.add("no-scroll");
      openBtn.setAttribute("aria-expanded", "true");
      drawer.setAttribute("aria-hidden", "false");
      $("a, button", $(".drawer-panel", drawer))?.focus({ preventScroll: true });
    });
    $$("[data-close-menu]", drawer).forEach((b) => b.addEventListener("click", close));
    addEventListener("keydown", (e) => e.key === "Escape" && drawer.classList.contains("is-open") && close());
  }

  /* ---------------- Toast ---------------- */
  const toaster = document.createElement("div");
  toaster.className = "toaster";
  toaster.setAttribute("role", "status");
  toaster.setAttribute("aria-live", "polite");
  document.body.appendChild(toaster);
  let toastTimer;
  window.toast = (title, text = "") => {
    toaster.innerHTML = "";
    const t = document.createElement("div");
    t.className = "toast";
    t.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg><div><strong></strong><span></span></div>`;
    t.querySelector("strong").textContent = title;
    t.querySelector("span").textContent = text;
    toaster.appendChild(t);
    clearTimeout(toastTimer);
    let remaining = 5000, started = Date.now();
    const hide = () => {
      t.dataset.state = "hidden";
      t.addEventListener("transitionend", () => t.remove(), { once: true });
    };
    // Le minuteur se met en pause quand l'onglet est caché (principe Sonner)
    const schedule = () => { started = Date.now(); toastTimer = setTimeout(hide, remaining); };
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) { clearTimeout(toastTimer); remaining -= Date.now() - started; }
      else if (t.isConnected) schedule();
    });
    schedule();
  };

  /* ---------------- Ouvert / fermé + horaires du jour ---------------- */
  // 0 = dimanche. Valeurs en minutes. À confirmer avec le client (audit).
  const HOURS = {
    1: [[540, 1050]], 2: [[540, 1050]], 3: [[540, 1050]], 4: [[540, 1050]], 5: [[540, 1050]],
    6: [[540, 780]], 0: [],
  };
  const now = new Date();
  const day = now.getDay();
  const mins = now.getHours() * 60 + now.getMinutes();
  const fmt = (m) => `${Math.floor(m / 60)}h${m % 60 ? String(m % 60).padStart(2, "0") : ""}`;
  const status = $("[data-open-status]");
  if (status) {
    const slot = HOURS[day].find(([a, b]) => mins >= a && mins < b);
    const dot = $(".dot", status.parentElement);
    if (slot) {
      status.textContent = `Ouvert aujourd'hui jusqu'à ${fmt(slot[1])}`;
    } else {
      dot?.classList.add("closed");
      const later = HOURS[day].find(([a]) => mins < a);
      status.textContent = later ? `Ouvre aujourd'hui à ${fmt(later[0])}` : "Fermé pour aujourd'hui";
    }
  }
  $$(".hours tr[data-day]").forEach((tr) => {
    if (Number(tr.dataset.day) === day) tr.classList.add("today");
  });

  /* ---------------- Onglets à clip-path ---------------- */
  function setupTabs(root, onChange) {
    const list = $(".tabs-list", root);
    const overlay = $(".tabs-active", root);
    const buttons = $$("button", list);
    const move = (btn, instant) => {
      const left = btn.offsetLeft - list.offsetLeft;
      const right = list.offsetWidth - (left + btn.offsetWidth);
      if (instant) overlay.style.transition = "none";
      overlay.style.clipPath = `inset(0 ${right}px 0 ${left}px round 999px)`;
      if (instant) { overlay.offsetWidth; overlay.style.transition = ""; }
    };
    const select = (btn, instant = false) => {
      buttons.forEach((b) => b.setAttribute("aria-selected", String(b === btn)));
      move(btn, instant);
      onChange(btn.dataset.value);
    };
    buttons.forEach((b) => b.addEventListener("click", () => select(b)));
    // Navigation clavier : pas d'animation sur une action clavier
    list.addEventListener("keydown", (e) => {
      const i = buttons.findIndex((b) => b.getAttribute("aria-selected") === "true");
      const n = e.key === "ArrowRight" ? i + 1 : e.key === "ArrowLeft" ? i - 1 : null;
      if (n === null) return;
      const next = buttons[(n + buttons.length) % buttons.length];
      next.focus(); select(next, true);
    });
    const initial = buttons.find((b) => b.getAttribute("aria-selected") === "true") || buttons[0];
    requestAnimationFrame(() => select(initial, true));
    addEventListener("resize", () => {
      const cur = buttons.find((b) => b.getAttribute("aria-selected") === "true");
      cur && move(cur, true);
    });
    // Copie visuelle des compteurs dans la liste dupliquée
    return { select };
  }

  /* ---------------- Saison ---------------- */
  // Tirées des textes du site : poire en automne, clémentine en décembre,
  // pamplemousse et kiwi en janvier, orange sanguine au 1er trimestre,
  // nectarine en juillet, fraise l'été.
  const SEASON = {
    0: ["pamplemousse", "kiwi", "orange-sanguine"],
    1: ["orange-sanguine", "kiwi", "pamplemousse"],
    2: ["orange-sanguine", "duo-citron", "kiwi"],
    3: ["fraise", "duo-citron", "melon-menthe"],
    4: ["fraise", "melon-menthe", "abricot"],
    5: ["fraise", "abricot", "melon-menthe"],
    6: ["nectarine", "fraise", "abricot"],
    7: ["fraise", "nectarine", "melon-menthe"],
    8: ["poire", "framboise-poivron", "noix"],
    9: ["poire", "noix", "rhum-raisin"],
    10: ["poire", "clementine", "noix"],
    11: ["clementine", "poire", "rhum-raisin"],
  };
  const MONTHS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"];
  const inSeason = SEASON[now.getMonth()];
  $$("[data-month]").forEach((el) => (el.textContent = MONTHS[now.getMonth()]));
  $$(".flavor[data-id]").forEach((card) => {
    if (inSeason.includes(card.dataset.id)) {
      card.dataset.season = "1";
      const img = $(".flavor-img", card);
      if (img && !$(".season-chip", img)) {
        const c = document.createElement("span");
        c.className = "chip season-chip";
        c.textContent = "De saison";
        img.appendChild(c);
      }
    }
  });
  // Accueil : remplir le bloc « en ce moment »
  const seasonSlot = $("[data-season-list]");
  const tpl = $("#flavor-data");
  if (seasonSlot && tpl) {
    const data = JSON.parse(tpl.textContent);
    inSeason.forEach((id) => {
      const f = data.find((x) => x.id === id);
      if (!f) return;
      seasonSlot.insertAdjacentHTML("beforeend",
        `<article class="flavor"><div class="flavor-img"><img src="${f.img}" alt="Sorbet ${f.name.toLowerCase()} des Garçons Glaciers" loading="lazy" width="720" height="720"></div><div class="flavor-body"><h3>${f.name}</h3><p>${f.desc}</p></div></article>`);
    });
  }

  /* ---------------- Filtre « Nos glaces » ---------------- */
  const flavorTabs = $("[data-flavor-tabs]");
  if (flavorTabs) {
    const cards = $$(".flavor[data-family]");
    const note = $("[data-results]");
    const counts = { tout: cards.length, creme: 0, sorbet: 0, saison: 0 };
    cards.forEach((c) => { counts[c.dataset.family]++; if (c.dataset.season) counts.saison++; });
    $$(".count", flavorTabs).forEach((el) => (el.textContent = counts[el.dataset.count]));
    setupTabs(flavorTabs, (v) => {
      let shown = 0;
      cards.forEach((c) => {
        const ok = v === "tout" || c.dataset.family === v || (v === "saison" && c.dataset.season);
        c.hidden = !ok; if (ok) shown++;
      });
      if (note) note.textContent = `${shown} parfum${shown > 1 ? "s" : ""}`;
      history.replaceState(null, "", v === "tout" ? location.pathname : `#${v}`);
    });
    const hash = location.hash.slice(1);
    const fromHash = $(`button[data-value="${hash}"]`, $(".tabs-list", flavorTabs));
    if (fromHash) $$(".tabs-list button", flavorTabs).forEach((b) => b.setAttribute("aria-selected", String(b === fromHash)));
  }

  /* ---------------- Filtre boutique (nombre de parts) ---------------- */
  const shopTabs = $("[data-shop-tabs]");
  if (shopTabs) {
    const items = $$(".product[data-parts]");
    setupTabs(shopTabs, (v) => {
      items.forEach((p) => (p.hidden = !(v === "tout" || p.dataset.parts.split(",").includes(v))));
    });
  }

  /* ---------------- « Me prévenir » (rupture de stock) ---------------- */
  $$("[data-notify]").forEach((btn) =>
    btn.addEventListener("click", () => {
      const product = btn.dataset.notify;
      const subject = encodeURIComponent(`Me prévenir du retour : ${product}`);
      const body = encodeURIComponent(`Bonjour,\n\nPouvez-vous me prévenir quand « ${product} » sera de nouveau disponible ?\n\nMerci !`);
      location.href = `mailto:contact@lesgarconsglaciers.com?subject=${subject}&body=${body}`;
      toast("C'est noté", "Votre messagerie s'ouvre avec la demande pré-remplie.");
    })
  );

  /* ---------------- Bascule question / devis ---------------- */
  $$("[data-switch]").forEach((sw) => {
    const btns = $$("button", sw);
    const show = (btn) => {
      btns.forEach((b) => {
        const on = b === btn;
        b.setAttribute("aria-selected", String(on));
        $("#" + b.getAttribute("aria-controls")).hidden = !on;
      });
    };
    btns.forEach((b) => b.addEventListener("click", () => show(b)));
    if (location.hash === "#devis") { const d = btns.find((b) => b.dataset.key === "devis"); d && show(d); }
  });

  /* ---------------- Formulaires ----------------
     Pas de serveur : on prépare un e-mail. Pour un envoi direct, brancher
     l'attribut action sur un service (Formspree, Netlify Forms, etc.). */
  $$("form[data-mail]").forEach((form) =>
    form.addEventListener("submit", (e) => {
      if (form.getAttribute("action")) return; // un vrai back-end est branché
      e.preventDefault();
      if (!form.reportValidity()) return;
      const fd = new FormData(form);
      const lines = [];
      for (const [k, v] of fd.entries()) if (String(v).trim()) lines.push(`${k} : ${v}`);
      const subject = encodeURIComponent(form.dataset.mail);
      const body = encodeURIComponent(lines.join("\n"));
      location.href = `mailto:contact@lesgarconsglaciers.com?subject=${subject}&body=${body}`;
      toast("Message prêt à partir", "Votre messagerie s'ouvre : il ne reste qu'à cliquer sur Envoyer.");
    })
  );

  /* ---------------- Carte chargée à la demande (aucun cookie tiers avant clic) ---------------- */
  $$("[data-load-map]").forEach((btn) =>
    btn.addEventListener("click", () => {
      const box = btn.closest(".map");
      const iframe = document.createElement("iframe");
      iframe.title = "Carte : place La Fayette, Angers";
      iframe.loading = "lazy";
      iframe.referrerPolicy = "no-referrer-when-downgrade";
      iframe.src = "https://maps.google.com/maps?q=" + encodeURIComponent("Place La Fayette, 49000 Angers") + "&z=16&output=embed";
      box.appendChild(iframe);
      $(".map-placeholder", box)?.remove();
    })
  );
})();
