const task = document.getElementById('task');
const input = document.getElementById('inputText');
const submit = document.getElementById('submitBtn');
const clear = document.getElementById('clearBtn');
const result = document.getElementById('result');
const status = document.getElementById('status');

const config = {
  qa: { endpoint: '/qa', placeholder: 'Example: Why does the Moon not fall to Earth?' },
  explain: { endpoint: '/explain', placeholder: 'Example: Explain photosynthesis to a beginner.' },
  quiz: { endpoint: '/quiz', placeholder: 'Paste a topic or passage for 3 MCQs.' },
  summarize: { endpoint: '/summarize', placeholder: 'Paste the educational passage you want summarized.' },
  learn: { endpoint: '/learn/recommendations', placeholder: 'Example: I want to learn SQL from beginner to advanced.' }
};

task.addEventListener('change', () => { input.placeholder = config[task.value].placeholder; });

function showStatus(message, isError = false) {
  status.textContent = message;
  status.classList.remove('hidden', 'error');
  if (isError) status.classList.add('error');
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
}

function renderQuiz(data) {
  const questions = data.questions || [];
  result.innerHTML = '<h3>🧠 Your Quiz</h3>' + questions.map((q, i) => `
    <div class="quiz-question">
      <strong>${i + 1}. ${escapeHtml(q.question)}</strong>
      <div class="quiz-options">
        ${q.options.map(option => `<button class="quiz-option" data-answer="${escapeHtml(q.answer)}" data-option="${escapeHtml(option)}">${escapeHtml(option)}</button>`).join('')}
      </div>
    </div>`).join('');

  result.querySelectorAll('.quiz-option').forEach(btn => btn.addEventListener('click', () => {
    const correct = btn.dataset.option === btn.dataset.answer;
    btn.classList.add(correct ? 'correct' : 'wrong');
    if (!correct) {
      const buttons = btn.parentElement.querySelectorAll('.quiz-option');
      buttons.forEach(b => { if (b.dataset.option === btn.dataset.answer) b.classList.add('correct'); });
    }
  }));
}

submit.addEventListener('click', async () => {
  const text = input.value.trim();
  if (!text) return showStatus('Please enter something first.', true);

  submit.disabled = true;
  result.classList.add('hidden');
  showStatus('EduGenie is thinking…');

  try {
    const response = await fetch(config[task.value].endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Request failed.');

    if (task.value === 'quiz') renderQuiz(data.result);
    else result.textContent = data.result;

    result.classList.remove('hidden');
    status.classList.add('hidden');
  } catch (error) {
    showStatus(error.message, true);
  } finally {
    submit.disabled = false;
  }
});

clear.addEventListener('click', () => {
  input.value = '';
  result.classList.add('hidden');
  status.classList.add('hidden');
});
