/* Signature Legal — site script (vanilla JS, no dependencies) */
(function () {
  "use strict";

  var doc = document.documentElement;
  doc.classList.add("js");

  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Safe sessionStorage ---------- */
  var memoryStore = {};
  function store(key, value) {
    try {
      if (value === undefined) return window.sessionStorage.getItem(key);
      window.sessionStorage.setItem(key, value);
    } catch (e) {
      if (value === undefined) return memoryStore[key] || null;
      memoryStore[key] = value;
    }
    return null;
  }

  /* ---------- Sticky header state ---------- */
  var header = document.querySelector(".site-header");
  function onScroll() {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 8);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile menu ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");

  function setMenu(open) {
    if (!toggle || !nav) return;
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    nav.classList.toggle("is-open", open);
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setMenu(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setMenu(false);
        toggle.focus();
      }
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 1080) setMenu(false);
    });
  }

  /* ---------- Reveal on scroll ---------- */
  var reveals = document.querySelectorAll(".reveal");
  if (!reduceMotion && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* ---------- Bar Council of India disclaimer ---------- */
  var CONSENT_KEY = "sl-bci-consent";
  var modal = document.getElementById("consent");

  if (modal && store(CONSENT_KEY) !== "agreed") {
    var lastFocus = document.activeElement;
    modal.hidden = false;
    document.body.classList.add("is-locked");
    var focusables = modal.querySelectorAll("button, a[href]");
    var agree = modal.querySelector("[data-consent='agree']");
    var disagree = modal.querySelector("[data-consent='disagree']");
    if (agree) agree.focus();

    modal.addEventListener("keydown", function (e) {
      if (e.key !== "Tab" || !focusables.length) return;
      var first = focusables[0];
      var last = focusables[focusables.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    if (agree) {
      agree.addEventListener("click", function () {
        store(CONSENT_KEY, "agreed");
        modal.hidden = true;
        document.body.classList.remove("is-locked");
        if (lastFocus && lastFocus.focus) lastFocus.focus();
      });
    }
    if (disagree) {
      disagree.addEventListener("click", function () {
        // Leave the site: go back if possible, otherwise to a neutral page.
        if (document.referrer && document.referrer.indexOf(location.host) === -1 && history.length > 1) {
          history.back();
        } else {
          window.location.href = "https://www.google.com/";
        }
      });
    }
  }

  /* ---------- Forms: validation + delivery ---------- */
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var PHONE_RE = /^(\+?91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}$/;
  var FIRM_EMAIL = "contact@signaturelegal.in";

  function fieldError(input, message) {
    var err = document.getElementById(input.id + "-error");
    if (err) err.textContent = message || "";
    if (message) input.setAttribute("aria-invalid", "true");
    else input.removeAttribute("aria-invalid");
  }

  function validateField(input) {
    var v = (input.value || "").trim();
    var label = input.getAttribute("data-label") || "This field";

    if (input.type === "checkbox") {
      if (input.required && !input.checked) return fieldError(input, "Please tick this box to continue."), false;
      return fieldError(input, ""), true;
    }
    if (input.type === "file") {
      var f = input.files && input.files[0];
      if (input.required && !f) return fieldError(input, "Please attach your CV."), false;
      if (f) {
        var okType = /\.(pdf|doc|docx)$/i.test(f.name);
        if (!okType) return fieldError(input, "Upload a PDF or Word file (.pdf, .doc, .docx)."), false;
        if (f.size > 5 * 1024 * 1024) return fieldError(input, "The file is larger than 5 MB. Please upload a smaller file."), false;
      }
      return fieldError(input, ""), true;
    }
    if (input.required && !v) return fieldError(input, label + " is required."), false;
    if (v && input.type === "email" && !EMAIL_RE.test(v)) return fieldError(input, "Enter an email address like name@example.com."), false;
    if (v && input.type === "tel" && !PHONE_RE.test(v)) return fieldError(input, "Enter a 10-digit Indian mobile number, e.g. +91 98765 43210."), false;
    if (v && input.minLength > 0 && v.length < input.minLength) return fieldError(input, label + " needs at least " + input.minLength + " characters."), false;
    return fieldError(input, ""), true;
  }

  function buildMailto(form) {
    var subjectBase = form.getAttribute("data-subject") || "Website enquiry";
    var lines = [];
    var subjectField = form.querySelector("[name='subject']");
    var subject = subjectBase + (subjectField && subjectField.value ? ": " + subjectField.value : "");
    Array.prototype.forEach.call(form.elements, function (el) {
      if (!el.name || el.type === "file" || el.type === "checkbox" || el.type === "submit" || el.name === "_gotcha") return;
      var lab = el.getAttribute("data-label") || el.name;
      lines.push(lab + ": " + el.value.trim());
    });
    if (form.querySelector("input[type='file']")) lines.push("", "(CV attached to this email)");
    return "mailto:" + FIRM_EMAIL + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(lines.join("\n"));
  }

  document.querySelectorAll("form[data-validate]").forEach(function (form) {
    var status = form.querySelector(".form-status");
    var inputs = form.querySelectorAll("input, select, textarea");

    inputs.forEach(function (input) {
      if (input.name === "_gotcha") return;
      input.addEventListener("blur", function () { if (input.value || input.type === "checkbox") validateField(input); });
      input.addEventListener("change", function () { if (input.getAttribute("aria-invalid")) validateField(input); });
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (status) { status.textContent = ""; status.classList.remove("is-error"); }

      var firstBad = null;
      inputs.forEach(function (input) {
        if (input.name === "_gotcha") return;
        if (!validateField(input) && !firstBad) firstBad = input;
      });
      if (firstBad) {
        firstBad.focus();
        if (status) { status.classList.add("is-error"); status.textContent = "Please correct the highlighted fields and try again."; }
        return;
      }

      // Spam trap: bots fill hidden fields.
      var trap = form.querySelector("[name='_gotcha']");
      if (trap && trap.value) return;

      var endpoint = form.getAttribute("data-endpoint") || "";
      var configured = endpoint && endpoint.indexOf("[") === -1;
      var button = form.querySelector("[type='submit']");

      if (configured) {
        if (button) { button.disabled = true; button.textContent = "Sending…"; }
        fetch(endpoint, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
          .then(function (res) {
            if (!res.ok) throw new Error("Request failed");
            form.reset();
            if (status) status.textContent = form.getAttribute("data-success") || "Thank you. Your message has been sent.";
          })
          .catch(function () {
            if (status) {
              status.classList.add("is-error");
              status.textContent = "Your message could not be sent. Please email us at " + FIRM_EMAIL + " or call +91 88923 43289.";
            }
          })
          .then(function () {
            if (button) { button.disabled = false; button.textContent = button.getAttribute("data-label") || "Send"; }
          });
      } else {
        // No form service connected yet: hand over to the visitor's email app.
        window.location.href = buildMailto(form);
        if (status) {
          status.textContent = form.querySelector("input[type='file']")
            ? "Your email app should now open with your application details. Please attach your CV to that email and send it to " + FIRM_EMAIL + "."
            : "Your email app should now open with your message ready to send to " + FIRM_EMAIL + ". If it doesn’t, please write to us directly at that address.";
        }
      }
      if (status) status.focus();
    });
  });
})();
