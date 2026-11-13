// A small, static-first network: pointer proximity moves nearby nodes, and
// connected edges follow. No animation runs while the illustration is idle.
(() => {
  const svg = document.querySelector('.network-art');
  if (!svg) return;
  const nodes = [...svg.querySelectorAll('.network-node')].map((element) => {
    const x = Number(element.dataset.x), y = Number(element.dataset.y);
    return { element, x, y, px: x, py: y };
  });
  const edges = [...svg.querySelectorAll('.network-edges line')].map((element) => ({
    element, from: Number(element.dataset.from), to: Number(element.dataset.to),
  }));
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let pointer = null, active = -1, focused = false, frame = 0;

  function setActive(index) {
    if (active === index) return;
    active = index;
    nodes.forEach((node, i) => node.element.classList.toggle('is-active', i === index));
    edges.forEach((edge) => edge.element.classList.toggle('is-active', index >= 0 && (edge.from === index || edge.to === index)));
    svg.classList.toggle('has-active-node', index >= 0);
  }

  function draw() {
    frame = 0;
    let moving = false;
    nodes.forEach((node) => {
      let tx = node.x, ty = node.y;
      if (pointer && !reducedMotion.matches) {
        const dx = node.x - pointer.x, dy = node.y - pointer.y;
        const distance = Math.hypot(dx, dy);
        const influence = Math.max(0, 1 - distance / 100);
        if (distance > 0) { tx += dx / distance * influence * 13; ty += dy / distance * influence * 13; }
      }
      if (reducedMotion.matches) { node.px = tx; node.py = ty; }
      else { node.px += (tx - node.px) * 0.16; node.py += (ty - node.py) * 0.16; }
      if (Math.abs(tx - node.px) + Math.abs(ty - node.py) > 0.04) moving = true;
      else { node.px = tx; node.py = ty; }
      node.element.setAttribute('transform', `translate(${node.px.toFixed(2)} ${node.py.toFixed(2)})`);
    });
    edges.forEach(({ element, from, to }) => {
      element.setAttribute('x1', nodes[from].px.toFixed(2)); element.setAttribute('y1', nodes[from].py.toFixed(2));
      element.setAttribute('x2', nodes[to].px.toFixed(2)); element.setAttribute('y2', nodes[to].py.toFixed(2));
    });
    if (moving) frame = requestAnimationFrame(draw);
  }
  const schedule = () => { if (!frame) frame = requestAnimationFrame(draw); };
  function pointFor(event) {
    const matrix = svg.getScreenCTM();
    if (!matrix) return null;
    const point = svg.createSVGPoint(); point.x = event.clientX; point.y = event.clientY;
    return point.matrixTransform(matrix.inverse());
  }
  function updatePointer(event) {
    const point = pointFor(event);
    if (!point) return;
    pointer = point;
    let nearest = -1, best = 85;
    nodes.forEach((node, i) => {
      const distance = Math.hypot(node.x - point.x, node.y - point.y);
      if (distance < best) { nearest = i; best = distance; }
    });
    setActive(nearest);
    schedule();
  }
  svg.addEventListener('pointermove', (event) => { if (event.pointerType !== 'touch') updatePointer(event); });
  svg.addEventListener('pointerleave', () => { pointer = null; if (!focused) setActive(-1); schedule(); });
  svg.addEventListener('pointerdown', (event) => { if (event.pointerType === 'touch') updatePointer(event); });
  svg.addEventListener('focus', () => { focused = true; });
  svg.addEventListener('blur', () => { focused = false; pointer = null; setActive(-1); schedule(); });
  svg.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') { pointer = null; setActive(-1); schedule(); return; }
    const delta = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[event.key];
    if (!delta) return;
    event.preventDefault();
    const index = active < 0 ? 0 : (active + delta + nodes.length) % nodes.length;
    pointer = null; setActive(index); schedule();
  });
  reducedMotion.addEventListener('change', schedule);
})();
