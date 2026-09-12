/**
 * Canvas fireworks overlay for celebratory form feedback.
 *
 * The canvas is created on demand, drawn over a transparent surface, and torn
 * down again — canvas, animation frame, timers and listeners — as soon as the
 * show ends, so a page never keeps paying for an effect that already played.
 */

const REDUCED_MOTION = "(prefers-reduced-motion: reduce)";

/** Hard ceiling so an explosion can never flood the canvas. */
const MAX_PARTICLES = 900;

/** Reference frame length; lets the simulation run at the same speed on 120 Hz screens. */
const FRAME_MS = 1000 / 60;

const FADE_MS = 300;

type Rocket = {
  x: number;
  y: number;
  vx: number;
  vy: number;
  targetY: number;
  hue: number;
};

type Particle = {
  x: number;
  y: number;
  vx: number;
  vy: number;
  hue: number;
  life: number;
  decay: number;
  size: number;
  gravity: number;
  drag: number;
  glitter: boolean;
};

export interface FireworksOptions {
  /** Shells launched before the show fades out. */
  shells?: number;
  /** Total show length in ms, including the closing fade. */
  duration?: number;
  /** Horizontal launch point of the first shell: 0 = left edge, 1 = right edge. */
  originX?: number;
}

/** The live show, so overlapping launches share one overlay instead of stacking. */
let activeShow: Promise<void> | null = null;

/**
 * Play a short fireworks show over the current page.
 *
 * Resolves once the overlay is gone, and resolves immediately when the visitor
 * asked for reduced motion or the page is hidden — callers can safely await it
 * before navigating away.
 */
export function launchFireworks({
  shells = 3,
  duration = 1400,
  originX = 0.5,
}: FireworksOptions = {}): Promise<void> {
  if (activeShow) return activeShow;

  const reducedMotion =
    typeof window !== "undefined" &&
    typeof window.matchMedia === "function" &&
    window.matchMedia(REDUCED_MOTION).matches;

  if (typeof document === "undefined" || document.hidden || reducedMotion) {
    return Promise.resolve();
  }

  const canvas = document.createElement("canvas");
  canvas.setAttribute("aria-hidden", "true");
  canvas.style.cssText = `position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:60;opacity:1;transition:opacity ${FADE_MS}ms ease-out`;

  const context = canvas.getContext("2d");
  if (!context) return Promise.resolve();

  // Aliased after the guard so TypeScript keeps the non-null type inside the
  // animation closures below.
  const ctx = context;

  // Dark pages get brighter, additively blended sparks so overlapping ones glow;
  // light pages get deeper sparks drawn normally, which would otherwise wash out
  // to white where a burst overlaps itself.
  const isDark = document.documentElement.getAttribute("data-theme") === "dark";
  const lightness = isDark ? 62 : 40;
  const blend: GlobalCompositeOperation = isDark ? "lighter" : "source-over";
  // Sparks fade out as they die; on a white page that fade reads as washed out,
  // so light pages get a head start on opacity.
  const alphaScale = isDark ? 1 : 1.6;
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const rockets: Rocket[] = [];
  const particles: Particle[] = [];
  const timers: number[] = [];
  let width = 0;
  let height = 0;
  let hue = Math.random() * 360;
  let frame = 0;
  let lastFrame = performance.now();
  let torn = false;
  let finish: () => void = () => {};

  const show = new Promise<void>((resolve) => {
    finish = resolve;
  });

  function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function launchShell(x: number) {
    // Step the hue on every shell so consecutive bursts never repeat a colour.
    hue = (hue + 47 + Math.random() * 70) % 360;

    rockets.push({
      x,
      y: height + 10,
      vx: (Math.random() - 0.5) * width * 0.0018,
      vy: -(height * 0.0155 + Math.random() * height * 0.0025),
      targetY: height * (0.12 + Math.random() * 0.3),
      hue,
    });
  }

  function explode(rocket: Rocket) {
    const scale = Math.min(width, height);
    const count = 60 + Math.round(Math.random() * 36);
    const speed = scale * (0.0032 + Math.random() * 0.0036);

    for (let i = 0; i < count; i++) {
      const angle = (i / count) * Math.PI * 2 + Math.random() * 0.08;
      const velocity = speed * (0.45 + Math.random() * 0.8);

      particles.push({
        x: rocket.x,
        y: rocket.y,
        vx: Math.cos(angle) * velocity,
        vy: Math.sin(angle) * velocity,
        hue: rocket.hue + (Math.random() - 0.5) * 34,
        life: 1,
        decay: 0.017 + Math.random() * 0.013,
        size: 1 + Math.random() * 1.4,
        gravity: scale * 0.00011,
        drag: 0.968,
        glitter: Math.random() < 0.18,
      });
    }
  }

  function update(dt: number) {
    if (particles.length > MAX_PARTICLES) {
      particles.splice(0, particles.length - MAX_PARTICLES);
    }

    for (let i = rockets.length - 1; i >= 0; i--) {
      const rocket = rockets[i];
      rocket.x += rocket.vx * dt;
      rocket.y += rocket.vy * dt;

      particles.push({
        x: rocket.x + (Math.random() - 0.5) * 3,
        y: rocket.y + 4,
        vx: (Math.random() - 0.5) * 0.5,
        vy: 0.4 + Math.random() * 0.6,
        hue: rocket.hue,
        life: 0.8,
        decay: 0.07,
        size: 1,
        gravity: 0,
        drag: 0.94,
        glitter: false,
      });

      if (rocket.y <= rocket.targetY) {
        rocket.y = rocket.targetY;
        explode(rocket);
        rockets.splice(i, 1);
      }
    }

    for (let i = particles.length - 1; i >= 0; i--) {
      const particle = particles[i];
      const drag = Math.pow(particle.drag, dt);

      particle.vx *= drag;
      particle.vy = particle.vy * drag + particle.gravity * dt;
      particle.x += particle.vx * dt;
      particle.y += particle.vy * dt;
      particle.life -= particle.decay * dt;

      if (particle.life <= 0 || particle.y > height + 40) particles.splice(i, 1);
    }
  }

  function draw() {
    // Punch a hole in the previous frame so sparks leave comet trails.
    ctx.globalCompositeOperation = "destination-out";
    ctx.fillStyle = "rgba(0, 0, 0, 0.22)";
    ctx.fillRect(0, 0, width, height);

    ctx.globalCompositeOperation = blend;
    for (const particle of particles) {
      const alpha = Math.min(Math.max(particle.life, 0) * alphaScale, 1);
      ctx.globalAlpha = particle.glitter ? alpha * (0.5 + Math.random() * 0.5) : alpha;
      ctx.fillStyle = `hsl(${particle.hue}, 100%, ${lightness}%)`;
      ctx.beginPath();
      ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.globalAlpha = 1;
    ctx.globalCompositeOperation = "source-over";
  }

  function tick(now: number) {
    const dt = Math.min((now - lastFrame) / FRAME_MS, 2.5);
    lastFrame = now;

    if (dt > 0) {
      update(dt);
      draw();
    }

    frame = requestAnimationFrame(tick);
  }

  function teardown() {
    if (torn) return;
    torn = true;

    cancelAnimationFrame(frame);
    for (const timer of timers) clearTimeout(timer);
    window.removeEventListener("resize", resize);
    window.removeEventListener("pagehide", teardown);
    document.removeEventListener("astro:before-swap", teardown);
    canvas.remove();
    activeShow = null;
    finish();
  }

  resize();
  document.body.appendChild(canvas);
  window.addEventListener("resize", resize);
  window.addEventListener("pagehide", teardown);
  document.addEventListener("astro:before-swap", teardown);

  const gap = Math.min(240, duration / (shells + 1));
  for (let i = 0; i < shells; i++) {
    const x = i === 0 ? width * originX : width * (0.18 + Math.random() * 0.64);

    if (i === 0) launchShell(x);
    else timers.push(window.setTimeout(() => launchShell(x), i * gap));
  }

  timers.push(
    window.setTimeout(
      () => {
        canvas.style.opacity = "0";
      },
      Math.max(duration - FADE_MS, gap * shells),
    ),
  );
  timers.push(window.setTimeout(teardown, duration));

  lastFrame = performance.now();
  frame = requestAnimationFrame(tick);

  activeShow = show;
  return show;
}
