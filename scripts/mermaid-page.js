import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';

const DEFAULT_CONFIG = {
  startOnLoad: false,
  useMaxWidth: false,
  theme: 'base',
  flowchart: {
    useMaxWidth: false,
    nodeSpacing: 30,
    rankSpacing: 40,
    curve: 'basis',
  },
  timeline: {
    useMaxWidth: false,
  },
  themeVariables: {
    fontFamily: 'Calibri, Arial, sans-serif',
    fontSize: '14px',
  },
};

function isObject(value) {
  return value && typeof value === 'object' && !Array.isArray(value);
}

function mergeConfig(base, extra) {
  const output = { ...base };
  for (const [key, value] of Object.entries(extra || {})) {
    if (isObject(value) && isObject(output[key])) {
      output[key] = mergeConfig(output[key], value);
    } else {
      output[key] = value;
    }
  }
  return output;
}

function getDiagramRatio(svg) {
  const viewBox = svg.viewBox && svg.viewBox.baseVal;
  const width =
    (viewBox && viewBox.width) ||
    parseFloat(svg.getAttribute('width')) ||
    svg.getBoundingClientRect().width ||
    1000;
  const height =
    (viewBox && viewBox.height) ||
    parseFloat(svg.getAttribute('height')) ||
    svg.getBoundingClientRect().height ||
    600;

  return height > 0 ? width / height : 1.6;
}

function pickTargetWidth(ratio) {
  if (ratio >= 3.0) return 1280;
  if (ratio >= 2.1) return 1140;
  if (ratio >= 1.35) return 980;
  if (ratio >= 0.95) return 860;
  if (ratio >= 0.65) return 760;
  return 680;
}

function normalizeMermaidDiagrams() {
  document.querySelectorAll('.mermaid svg').forEach((svg) => {
    const wrapper = svg.closest('.mermaid');
    if (!wrapper) return;

    const ratio = getDiagramRatio(svg);
    const targetWidth = wrapper.dataset.mermaidWidth || `${pickTargetWidth(ratio)}px`;

    wrapper.style.setProperty('--mermaid-target-width', targetWidth);
    wrapper.classList.toggle('mermaid-wide', ratio >= 2.1);
    wrapper.classList.toggle('mermaid-tall', ratio < 0.95);
  });
}

let resizeObserver;
let resizeHandlerAttached = false;

function installMermaidResizeHandling() {
  const schedule = () => window.requestAnimationFrame(normalizeMermaidDiagrams);

  if ('ResizeObserver' in window) {
    if (!resizeObserver) {
      resizeObserver = new ResizeObserver(schedule);
    }
    document.querySelectorAll('.mermaid').forEach((node) => resizeObserver.observe(node));
    return;
  }

  if (!resizeHandlerAttached) {
    window.addEventListener('resize', schedule);
    resizeHandlerAttached = true;
  }
}

export function initMermaidPage(overrides = {}) {
  const config = mergeConfig(DEFAULT_CONFIG, overrides);

  const start = async () => {
    mermaid.initialize(config);
    await mermaid.run({ querySelector: '.mermaid' });
    window.requestAnimationFrame(() => {
      normalizeMermaidDiagrams();
      installMermaidResizeHandling();
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start, { once: true });
  } else {
    start();
  }
}
