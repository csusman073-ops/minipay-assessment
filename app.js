const $ = id => document.getElementById(id);

function setMessage(element, message, type = '') {
  element.textContent = message;
  element.className = `message ${type}`.trim();
}

function setResult(element, statusElement, body, ok = true) {
  element.textContent = typeof body === 'string' ? body : JSON.stringify(body, null, 2);
  statusElement.textContent = ok ? 'Success' : 'Error';
  statusElement.className = `result-status ${ok ? 'success' : 'error'}`;
}

function setLoading(button, loading) {
  button.disabled = loading;
  button.dataset.defaultLabel ||= button.innerHTML;
  button.innerHTML = loading ? 'Working...' : button.dataset.defaultLabel;
}

async function api(path, options = {}) {
  const headers = {...(options.headers || {})};
  const res = await fetch(path, {...options, headers});
  const text = await res.text();
  let body;
  try {
    body = JSON.parse(text);
  } catch {
    body = text;
  }
  if (!res.ok) {
    throw new Error(`${res.status}: ${typeof body === 'string' ? body : JSON.stringify(body)}`);
  }
  return body;
}

$('loginBtn').onclick = () => {
  const button = $('loginBtn');
  setLoading(button, true);
  setMessage($('loginResult'), 'Login successful', 'success');
  $('loginPanel').hidden = true;
  $('appPanel').hidden = false;
  $('transactionRef').value = `UI-${Date.now()}`;
  setLoading(button, false);
  button.innerHTML = 'Login <span class="btn-arrow">→</span>';
};

$('searchBtn').onclick = async () => {
  const button = $('searchBtn');
  const ref = $('searchRef').value.trim();
  if (!ref) {
    setResult($('searchResult'), $('searchStatus'), 'Enter a transaction reference.', false);
    $('searchRef').focus();
    return;
  }

  setLoading(button, true);
  $('searchStatus').textContent = 'Searching';
  $('searchStatus').className = 'result-status';
  try {
    const body = await api(`/api/payments/search?transaction_ref=${encodeURIComponent(ref)}`);
    setResult($('searchResult'), $('searchStatus'), body, true);
  } catch (e) {
    setResult($('searchResult'), $('searchStatus'), e.message, false);
  } finally {
    setLoading(button, false);
    button.innerHTML = 'Search transaction <span>→</span>';
  }
};

$('payBtn').onclick = async () => {
  const button = $('payBtn');
  const customerId = Number($('customerId').value);
  const amount = Number($('amount').value);
  const transactionRef = $('transactionRef').value.trim();

  if (!Number.isInteger(customerId) || customerId < 1) {
    setResult($('payResult'), $('payStatus'), 'Customer ID must be a positive whole number.', false);
    $('customerId').focus();
    return;
  }
  if (!Number.isFinite(amount) || amount <= 0) {
    setResult($('payResult'), $('payStatus'), 'Amount must be greater than zero.', false);
    $('amount').focus();
    return;
  }
  if (!transactionRef) {
    setResult($('payResult'), $('payStatus'), 'Enter a transaction reference.', false);
    $('transactionRef').focus();
    return;
  }

  setLoading(button, true);
  $('payStatus').textContent = 'Processing';
  $('payStatus').className = 'result-status';
  try {
    const body = await api('/api/payments', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        customer_id: customerId,
        amount,
        transaction_ref: transactionRef,
        idempotency_key: `ui-${Date.now()}`
      })
    });
    setResult($('payResult'), $('payStatus'), body, true);
  } catch (e) {
    setResult($('payResult'), $('payStatus'), e.message, false);
  } finally {
    setLoading(button, false);
    button.innerHTML = 'Submit payment <span class="btn-arrow">→</span>';
  }
};
