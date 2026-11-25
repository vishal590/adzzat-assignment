'use strict';

const byId = id => document.getElementById(id);
let tasks = [];

function showTask() {
  const id = location.hash.slice(1);
  const task = tasks.find(item => item.id === id) || tasks[0];
  for (const link of byId('task-list').querySelectorAll('a')) {
    if (link.hash === '#' + task.id) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  }
  byId('task-id').textContent = task.id.toUpperCase();
  byId('difficulty').textContent = task.difficulty;
  byId('kind').textContent = task.kind;
  byId('task-title').textContent = task.title;
  byId('environment').textContent = task.environment;
  byId('difficulty-note').textContent = task.difficulty_note;
  byId('statement').replaceChildren(...task.statement.split('\n\n').map(text => {
    const paragraph = document.createElement('p');
    paragraph.textContent = text;
    return paragraph;
  }));
  document.title = task.title + ' — Taskroom';
}

async function start() {
  try {
    const response = await fetch('/api/tasks');
    if (!response.ok) throw new Error('Task endpoint returned ' + response.status);
    tasks = await response.json();
    if (!Array.isArray(tasks) || tasks.length !== 2) throw new Error('Expected two tasks');
    for (const task of tasks) {
      const link = document.createElement('a');
      link.href = '#' + task.id;
      const id = document.createElement('span');
      id.className = 'task-number';
      id.textContent = task.id.toUpperCase();
      const title = document.createElement('strong');
      title.textContent = task.title;
      const note = document.createElement('span');
      note.className = 'task-meta';
      note.textContent = task.kind + ' · ' + task.difficulty;
      link.append(id, title, note);
      byId('task-list').append(link);
    }
    showTask();
    byId('status').hidden = true;
    byId('workspace').hidden = false;
    addEventListener('hashchange', showTask);
  } catch (error) {
    byId('status').textContent = 'The collection could not load. Please reload to try again.';
    console.error(error);
  }
}

start();
