/* ==========================================================================
   BHAVYA & SANYAM ROYAL WEDDING INVITATION — INTERACTIVE ENGINE
   Faithful to Luxury Wax Seal Royale Architecture
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {

  /* ------------------------------------------------------------------------
     1. WAX SEAL ROYALE OPENING & AUDIO ORCHESTRATION
     ------------------------------------------------------------------------ */
  const overlay    = document.getElementById('weiOverlay');
  const videoWrap  = document.getElementById('weiVideoWrap');
  const video      = document.getElementById('weiVideo');
  const audio      = document.getElementById('weiAudio');
  const audioBtn   = document.getElementById('weiAudioBtn');
  const iconPause  = document.getElementById('weiIconPause');
  const iconPlay   = document.getElementById('weiIconPlay');

  let sequenceStarted = false;
  let sequenceEnded   = false;
  let fallbackTimer   = null;

  function updateAudioButtonState(isPlaying) {
    if (iconPlay && iconPause) {
      if (isPlaying) {
        iconPlay.style.display = 'none';
        iconPause.style.display = 'block';
      } else {
        iconPlay.style.display = 'block';
        iconPause.style.display = 'none';
      }
    }
  }

  function playAudioSafely() {
    if (!audio) return;
    audio.muted = false;
    audio.volume = 1;
    const playPromise = audio.play();
    if (playPromise !== undefined) {
      playPromise.then(() => {
        updateAudioButtonState(true);
      }).catch(() => {
        updateAudioButtonState(false);
        const unlockAudio = () => {
          if (audio.paused) {
            audio.play().then(() => updateAudioButtonState(true)).catch(() => {});
          }
          ['click', 'touchstart', 'touchend', 'pointerdown'].forEach(evt => {
            document.removeEventListener(evt, unlockAudio);
          });
        };
        ['click', 'touchstart', 'touchend', 'pointerdown'].forEach(evt => {
          document.addEventListener(evt, unlockAudio, { passive: true, once: true });
        });
      });
    }
  }

  if (audio) {
    audio.addEventListener('play', () => updateAudioButtonState(true));
    audio.addEventListener('pause', () => updateAudioButtonState(false));
  }

  if (audioBtn) {
    audioBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (audio.paused) {
        audio.play();
        updateAudioButtonState(true);
      } else {
        audio.pause();
        updateAudioButtonState(false);
      }
    });
  }

  // Mobile video readiness
  if (video) {
    video.muted = true;
    video.defaultMuted = true;
    video.playsInline = true;
    video.setAttribute('playsinline', '');
    video.setAttribute('webkit-playsinline', '');
  }

  function startInvitationSequence() {
    if (sequenceStarted) return;
    sequenceStarted = true;

    // Trigger music immediately in user gesture stack
    playAudioSafely();

    // Lock page during reveal
    document.body.classList.add('video-active', 'envelope-active');

    // Play unveiling video
    if (video) {
      video.muted = true;
      video.currentTime = 0;
      const vp = video.play();
      if (vp && vp.catch) {
        vp.catch(() => {
          setTimeout(endInvitationSequence, 1500);
        });
      }
    }

    // Cross-fade envelope
    if (overlay) {
      overlay.style.opacity = '0';
      overlay.style.pointerEvents = 'none';
      setTimeout(() => { overlay.style.display = 'none'; }, 800);
    }

    if (videoWrap) {
      videoWrap.classList.add('wei-video-in');
    }

    // Fallback timer
    fallbackTimer = setTimeout(endInvitationSequence, 6500);
  }

  function endInvitationSequence() {
    if (sequenceEnded) return;
    sequenceEnded = true;

    if (fallbackTimer) {
      clearTimeout(fallbackTimer);
      fallbackTimer = null;
    }

    window.scrollTo({ top: 0, behavior: 'instant' });

    if (videoWrap) {
      videoWrap.classList.remove('wei-video-in');
      videoWrap.classList.add('wei-video-out');
      setTimeout(() => {
        videoWrap.style.display = 'none';
        if (video) video.pause();
      }, 1200);
    }

    document.body.classList.remove('envelope-active', 'video-active');

    if (audioBtn) {
      audioBtn.style.visibility = 'visible';
      audioBtn.style.opacity = '1';
    }
  }

  if (overlay) {
    overlay.addEventListener('click', startInvitationSequence);
    overlay.addEventListener('touchstart', startInvitationSequence, { passive: true });
  }

  if (video) {
    video.addEventListener('timeupdate', () => {
      if (video.duration && video.currentTime >= video.duration - 0.7) {
        endInvitationSequence();
      }
    });
    video.addEventListener('ended', endInvitationSequence);
  }


  /* ------------------------------------------------------------------------
     2. AMBIENT GOLD DUST CANVAS PARTICLES
     ------------------------------------------------------------------------ */
  const canvas = document.getElementById('ambient-canvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let width  = canvas.width  = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
      width  = canvas.width  = window.innerWidth;
      height = canvas.height = window.innerHeight;
    });

    const particles = [];
    const particleCount = 28;

    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 2.2 + 0.8,
        speedX: (Math.random() - 0.5) * 0.35,
        speedY: Math.random() * 0.45 + 0.25,
        opacity: Math.random() * 0.55 + 0.2,
        color: Math.random() > 0.4 ? 'rgba(197, 160, 89, ' : 'rgba(243, 229, 171, '
      });
    }

    function animateParticles() {
      ctx.clearRect(0, 0, width, height);

      particles.forEach(p => {
        p.x += p.speedX;
        p.y += p.speedY;

        if (p.y > height) {
          p.y = -10;
          p.x = Math.random() * width;
        }
        if (p.x > width) p.x = 0;
        if (p.x < 0) p.x = width;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = p.color + p.opacity + ')';
        ctx.shadowBlur = 4;
        ctx.shadowColor = 'rgba(197, 160, 89, 0.4)';
        ctx.fill();
      });

      requestAnimationFrame(animateParticles);
    }

    animateParticles();
  }


  /* ------------------------------------------------------------------------
     3. INTERACTIVE SCRATCH-TO-REVEAL DATE CARD
     ------------------------------------------------------------------------ */
  const scratchContainer = document.getElementById('scratch-date-container');
  const scratchCanvas    = document.getElementById('scratch-canvas');
  const scratchHint      = document.getElementById('scratch-hint');

  if (scratchCanvas && scratchContainer) {
    const ctx = scratchCanvas.getContext('2d');
    let isDrawing = false;
    let isRevealed = false;
    let strokesCount = 0;

    const dpr = window.devicePixelRatio || 1;
    const width = 250;
    const height = 62;

    scratchCanvas.width = width * dpr;
    scratchCanvas.height = height * dpr;
    scratchCanvas.style.width = width + 'px';
    scratchCanvas.style.height = height + 'px';
    ctx.scale(dpr, dpr);

    function initFoil() {
      const grad = ctx.createLinearGradient(0, 0, width, height);
      grad.addColorStop(0, '#E5C469');
      grad.addColorStop(0.2, '#B88728');
      grad.addColorStop(0.48, '#FFF6CE');
      grad.addColorStop(0.72, '#D49B24');
      grad.addColorStop(1, '#8C5E14');

      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, width, height);

      for (let i = 0; i < 36; i++) {
        ctx.fillStyle = Math.random() > 0.5 ? 'rgba(255, 255, 255, 0.6)' : 'rgba(110, 75, 15, 0.28)';
        ctx.beginPath();
        ctx.arc(Math.random() * width, Math.random() * height, Math.random() * 1.5 + 0.4, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.strokeStyle = 'rgba(255, 248, 215, 0.75)';
      ctx.lineWidth = 1.2;
      ctx.strokeRect(4, 4, width - 8, height - 8);

      ctx.font = '700 10.5px "Cinzel", Georgia, serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = 'rgba(75, 45, 10, 0.88)';
      ctx.shadowColor = 'rgba(255, 255, 255, 0.75)';
      ctx.shadowBlur = 2;
      ctx.fillText('✦ SCRATCH TO REVEAL DATE ✦', width / 2, height / 2);
      ctx.shadowColor = 'transparent';
    }

    initFoil();

    function getPointerPos(e) {
      const b = scratchCanvas.getBoundingClientRect();
      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      const clientY = e.touches ? e.touches[0].clientY : e.clientY;
      return { x: clientX - b.left, y: clientY - b.top };
    }

    function scratch(x, y) {
      if (isRevealed) return;
      ctx.globalCompositeOperation = 'destination-out';
      ctx.beginPath();
      ctx.arc(x, y, 18, 0, Math.PI * 2);
      ctx.fill();

      strokesCount++;
      if (strokesCount % 8 === 0) {
        checkClearedPercent();
      }
    }

    function checkClearedPercent() {
      if (isRevealed) return;
      try {
        const imgData = ctx.getImageData(0, 0, scratchCanvas.width, scratchCanvas.height);
        const pixels = imgData.data;
        let transparentPixels = 0;
        const step = 32;
        let totalSampled = 0;

        for (let i = 3; i < pixels.length; i += 4 * step) {
          totalSampled++;
          if (pixels[i] === 0) transparentPixels++;
        }

        if (transparentPixels / totalSampled > 0.35) {
          revealComplete();
        }
      } catch (err) {}
    }

    function revealComplete() {
      if (isRevealed) return;
      isRevealed = true;
      scratchCanvas.style.opacity = '0';
      scratchCanvas.style.pointerEvents = 'none';
      if (scratchHint) {
        scratchHint.innerHTML = '<span class="scratch-hint-pill"><i class="fa-solid fa-crown"></i> Auspicious Day • Thursday, 26 Nov 2026</span>';
      }
      setTimeout(() => { scratchCanvas.style.display = 'none'; }, 600);
    }

    scratchCanvas.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      isDrawing = true;
      const pos = getPointerPos(e);
      scratch(pos.x, pos.y);
    });

    window.addEventListener('pointermove', (e) => {
      if (!isDrawing) return;
      const pos = getPointerPos(e);
      scratch(pos.x, pos.y);
    });

    window.addEventListener('pointerup', () => {
      if (isDrawing) {
        isDrawing = false;
        checkClearedPercent();
      }
    });
  }


  /* ------------------------------------------------------------------------
     4. REAL-TIME LIVE WEDDING COUNTDOWN TIMER
     Target: 26th November 2026, 11:00 AM IST (+05:30)
     ------------------------------------------------------------------------ */
  const targetWeddingDate = new Date(2026, 10, 26, 11, 0, 0).getTime();
  const elDays  = document.getElementById('days');
  const elHours = document.getElementById('hours');
  const elMins  = document.getElementById('minutes');
  const elSecs  = document.getElementById('seconds');
  const prevVals = { d: null, h: null, m: null, s: null };

  function flip(el, newVal) {
    if (!el || el.textContent === newVal) return;
    el.classList.add('flip-out');
    setTimeout(() => {
      el.classList.remove('flip-out');
      el.classList.add('flip-in');
      el.textContent = newVal;
      el.offsetHeight;
      el.classList.remove('flip-in');
    }, 280);
  }

  function updateCountdown() {
    const now = new Date().getTime();
    const diff = targetWeddingDate - now;

    if (diff <= 0) {
      const container = document.getElementById('countdownContainer');
      if (container) {
        container.innerHTML = '<div style="font-family:\'Cinzel\',serif; font-size:22px; color:#8C6721; font-weight:700;">The Auspicious Wedding Day is Today!</div>';
      }
      return;
    }

    const d = String(Math.floor(diff / (1000 * 60 * 60 * 24))).padStart(2, '0');
    const h = String(Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))).padStart(2, '0');
    const m = String(Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))).padStart(2, '0');
    const s = String(Math.floor((diff % (1000 * 60)) / 1000)).padStart(2, '0');

    if (d !== prevVals.d) { flip(elDays, d); prevVals.d = d; }
    if (h !== prevVals.h) { flip(elHours, h); prevVals.h = h; }
    if (m !== prevVals.m) { flip(elMins, m); prevVals.m = m; }
    if (s !== prevVals.s) { flip(elSecs, s); prevVals.s = s; }
  }

  updateCountdown();
  setInterval(updateCountdown, 1000);


  /* ------------------------------------------------------------------------
     5. INTERACTIVE ROSE PETALS & BLESSINGS SHOWER
     ------------------------------------------------------------------------ */
  const showerBtn = document.getElementById('btn-shower-blessings');
  const blessingCountElem = document.getElementById('blessing-count');
  const coupleContainer = document.querySelector('.couple-gallery-container');

  let blessingCount = parseInt(localStorage.getItem('bhavya_sanyam_blessings') || '452', 10);
  if (blessingCountElem) {
    blessingCountElem.textContent = blessingCount.toLocaleString();
  }

  function triggerPetalShower(e) {
    blessingCount++;
    if (blessingCountElem) {
      blessingCountElem.textContent = blessingCount.toLocaleString();
    }
    localStorage.setItem('bhavya_sanyam_blessings', blessingCount.toString());

    if (showerBtn) {
      showerBtn.style.transform = 'scale(0.96)';
      setTimeout(() => { showerBtn.style.transform = ''; }, 200);
    }

    // Spawn upward floating emojis around couple cards
    const emojis = ['💖', '🌸', '✨', '🌹', '💫', '❤️', '👑', '🕊️'];
    const emojiCount = 10;
    const coupleRect = coupleContainer ? coupleContainer.getBoundingClientRect() : null;

    for (let j = 0; j < emojiCount; j++) {
      const emojiEl = document.createElement('div');
      emojiEl.className = 'floating-blessing-emoji';
      emojiEl.textContent = emojis[Math.floor(Math.random() * emojis.length)];

      let originX = window.innerWidth / 2;
      let originY = window.innerHeight * 0.65;

      if (coupleRect) {
        originX = coupleRect.left + Math.random() * coupleRect.width;
        originY = coupleRect.top + window.scrollY + Math.random() * (coupleRect.height * 0.7);
      }

      emojiEl.style.left = `${originX}px`;
      emojiEl.style.top = `${originY}px`;
      emojiEl.style.setProperty('--drift-x', `${(Math.random() - 0.5) * 140}px`);
      emojiEl.style.setProperty('--rot', `${(Math.random() - 0.5) * 60}deg`);

      document.body.appendChild(emojiEl);
      setTimeout(() => emojiEl.remove(), 2800);
    }

    // Spawn falling flower petals across screen
    const petalColors = ['#D92546', '#8B1E2F', '#FFA500', '#FFD700', '#FAD2E1', '#C5A059', '#FFFDF9'];
    const count = 34;

    for (let i = 0; i < count; i++) {
      const petal = document.createElement('div');
      petal.className = 'falling-petal';

      const isCircle = Math.random() > 0.6;
      const size = Math.floor(Math.random() * 16) + 12;
      const color = petalColors[Math.floor(Math.random() * petalColors.length)];
      const startX = Math.random() * window.innerWidth;
      const driftX = (Math.random() - 0.5) * 240 + 'px';
      const duration = (Math.random() * 2.5 + 2.8) + 's';
      const rot = (Math.random() * 720 - 360) + 'deg';

      petal.style.left = `${startX}px`;
      petal.style.top = '-20px';
      petal.style.width = `${size}px`;
      petal.style.height = `${isCircle ? size : size * 1.5}px`;
      petal.style.backgroundColor = color;
      petal.style.borderRadius = isCircle ? '50%' : '50% 0 50% 50%';
      petal.style.boxShadow = '0 2px 6px rgba(0, 0, 0, 0.18)';
      petal.style.setProperty('--drift-x', driftX);
      petal.style.setProperty('--rot', rot);
      petal.style.animationDuration = duration;

      document.body.appendChild(petal);
      setTimeout(() => petal.remove(), 5500);
    }
  }

  if (showerBtn) showerBtn.addEventListener('click', triggerPetalShower);


  /* ------------------------------------------------------------------------
     6. CEREMONY ITINERARY ACCORDION DRAWERS
     ------------------------------------------------------------------------ */
  const itineraryBtns = document.querySelectorAll('.btn-card-itinerary');
  itineraryBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const card = btn.closest('.event-card-luxury');
      if (!card) return;
      const drawer = card.querySelector('.event-itinerary-drawer');
      if (!drawer) return;

      const isOpen = drawer.classList.contains('open');

      document.querySelectorAll('.event-itinerary-drawer.open').forEach(d => {
        if (d !== drawer) {
          d.classList.remove('open');
          const parent = d.closest('.event-card-luxury');
          if (parent) {
            parent.classList.remove('itinerary-open');
            const toggle = parent.querySelector('.btn-card-itinerary');
            if (toggle) {
              toggle.classList.remove('active');
              toggle.setAttribute('aria-expanded', 'false');
            }
          }
        }
      });

      if (isOpen) {
        drawer.classList.remove('open');
        card.classList.remove('itinerary-open');
        btn.classList.remove('active');
        btn.setAttribute('aria-expanded', 'false');
      } else {
        drawer.classList.add('open');
        card.classList.add('itinerary-open');
        btn.classList.add('active');
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });


  /* ------------------------------------------------------------------------
     7. ADD TO GOOGLE CALENDAR HANDLERS
     ------------------------------------------------------------------------ */
  const calBtns = document.querySelectorAll('.cal-btn');
  calBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const title    = btn.getAttribute('data-title') || 'Bhavya & Sanyam Wedding Ceremony';
      const startIso = btn.getAttribute('data-start'); // '2026-11-26T11:00:00'
      const endIso   = btn.getAttribute('data-end') || '2026-11-26T19:00:00';
      const location = btn.getAttribute('data-location') || 'Crossroads Banquets';

      const startDate = new Date(startIso + '+05:30');
      const endDate   = new Date(endIso + '+05:30');

      const formatGCalDate = (d) => d.toISOString().replace(/-|:|\.\d+/g, '');
      const gcalUrl = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${encodeURIComponent(title)}&dates=${formatGCalDate(startDate)}/${formatGCalDate(endDate)}&details=${encodeURIComponent('Join us to celebrate the wedding union of Bhavya & Sanyam at Crossroads Banquets.')}&location=${encodeURIComponent(location)}`;

      window.open(gcalUrl, '_blank');
    });
  });

});
