// Execute the actual served HTML/JS against the live Python endpoint.
// This verifies DOM behavior, not layout or actual browser rendering.
const assert = require('node:assert/strict');
const { JSDOM, VirtualConsole } = require('jsdom');
const base = process.env.CATALOG_URL || 'http://127.0.0.1:8000';
const checks = [];

async function waitFor(predicate, label) {
  const deadline = Date.now() + 5000;
  while (!predicate()) {
    if (Date.now() >= deadline) throw new Error('Timed out: ' + label);
    await new Promise(resolve => setTimeout(resolve, 10));
  }
}

async function open(hash = '', failApi = false) {
  const errors = [];
  const virtualConsole = new VirtualConsole();
  virtualConsole.on('jsdomError', error => errors.push(error.message));
  const dom = await JSDOM.fromURL(base + '/' + hash, {
    resources: 'usable', runScripts: 'dangerously', virtualConsole,
    beforeParse(window) {
      window.fetch = (url, options) => failApi
        ? Promise.resolve({ok: false, status: 503})
        : fetch(new URL(url, window.location.href), options);
    }
  });
  if (failApi) {
    await waitFor(() => dom.window.document.querySelector('[role="status"]').textContent.includes('could not load'), 'failure message');
  } else {
    await waitFor(() => !dom.window.document.querySelector('#workspace').hidden, 'collection loaded');
  }
  assert.deepEqual(errors, [], 'No uncaught page/script/resource errors');
  return dom;
}

async function main() {
  const response = await fetch(base + '/api/tasks');
  assert.equal(response.status, 200);
  const tasks = await response.json();
  assert.equal(tasks.length, 2);
  const dom = await open();
  try {
    const { window } = dom;
    const doc = window.document;
    const links = [...doc.querySelectorAll('nav[aria-label="Tasks"] a')];
    assert.equal(links.length, 2);
    function detailMatches(task) {
      assert.equal(doc.querySelector('h2').textContent, task.title);
      assert.equal(doc.querySelector('#difficulty').textContent, task.difficulty);
      assert.equal(doc.querySelector('#statement').textContent, task.statement.replaceAll('\n\n', ''));
      assert.equal(doc.querySelector('#environment').textContent, task.environment);
      assert.equal(doc.querySelector('#difficulty-note').textContent, task.difficulty_note);
      assert.equal(doc.querySelector('a[aria-current="page"]').hash, '#' + task.id);
    }
    detailMatches(tasks[0]);
    checks.push('Live API returns two tasks; initial list/detail matches task-01');
    links[1].click();
    await waitFor(() => doc.querySelector('h2').textContent === tasks[1].title, 'task-02 click');
    detailMatches(tasks[1]);
    checks.push('Click task-02: full statement, environment, difficulty and selected state match API');
    links[0].click();
    await waitFor(() => doc.querySelector('h2').textContent === tasks[0].title, 'task-01 click');
    detailMatches(tasks[0]);
    window.history.back();
    await waitFor(() => doc.querySelector('h2').textContent === tasks[1].title, 'back navigation');
    detailMatches(tasks[1]);
    window.history.forward();
    await waitFor(() => doc.querySelector('h2').textContent === tasks[0].title, 'forward navigation');
    detailMatches(tasks[0]);
    checks.push('Click task-01 and use back/forward: selected task and detail remain synchronized');
  } finally { dom.window.close(); }
  const direct = await open('#task-02');
  try {
    assert.equal(direct.window.document.querySelector('h2').textContent, tasks[1].title);
    checks.push('Direct #task-02 URL opens its detail');
  } finally { direct.window.close(); }
  const failure = await open('', true);
  try {
    assert.equal(failure.window.document.querySelector('#workspace').hidden, true);
    checks.push('Unavailable API displays a retry message without a partial collection');
  } finally { failure.window.close(); }
  console.log(JSON.stringify({passed: true, base, method: 'jsdom 26.1.0 + live HTTP', checks,
    limitations: ['No browser rendering, responsive layout, or real-browser compatibility verification']}, null, 2));
}

main().catch(error => { console.error(error); process.exitCode = 1; });
