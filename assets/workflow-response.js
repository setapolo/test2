(() => {
  const render = (data) => {
    let target = document.getElementById('workflow-response');
    if (!target) {
      target = document.createElement('section');
      target.id = 'workflow-response';
      target.setAttribute('aria-live', 'polite');
      document.body.appendChild(target);
    }

    const title = document.createElement('h2');
    title.textContent = 'Workflow Response';
    const message = document.createElement('p');
    message.textContent = data && typeof data.text === 'string' ? data.text : 'No response available.';

    target.replaceChildren(title, message);
  };

  fetch('./api/response.json', { cache: 'no-store' })
    .then((response) => (response.ok ? response.json() : null))
    .then(render)
    .catch(() => render(null));
})();
