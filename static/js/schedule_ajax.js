(function () {
  var app = document.getElementById('app');
  var API = app.dataset.api;
  var CSRF = app.dataset.csrf;
  var form = document.getElementById('form');
  var rowsEl = document.getElementById('rows');
  var alertEl = document.getElementById('alert');
  var submitBtn = document.getElementById('submit-btn');
  var cancelBtn = document.getElementById('cancel-edit');
  var title = document.getElementById('form-title');
  var editId = null;

  function showAlert(msg, ok) {
    alertEl.innerHTML = '';
    var d = document.createElement('div');
    d.className = 'msg' + (ok ? '' : ' error');
    d.textContent = msg;
    alertEl.appendChild(d);
    setTimeout(function () { alertEl.innerHTML = ''; }, 3500);
  }

  function clearErrors() {
    form.querySelectorAll('[data-err]').forEach(function (e) { e.textContent = ''; });
  }

  function showErrors(errors) {
    Object.keys(errors).forEach(function (k) {
      var el = form.querySelector('[data-err="' + k + '"]');
      if (el) el.textContent = errors[k].join(' ');
    });
  }

  function post(url, data) {
    return fetch(url, {
      method: 'POST',
      headers: { 'X-CSRFToken': CSRF, 'X-Requested-With': 'XMLHttpRequest' },
      body: new URLSearchParams(data)
    }).then(function (r) { return r.json().then(function (j) { return { status: r.status, json: j }; }); });
  }

  function cell(text) {
    var td = document.createElement('td');
    td.textContent = text;
    return td;
  }

  function hhmm(t) {
    var p = t.split(':'), h = parseInt(p[0], 10), ap = h >= 12 ? 'PM' : 'AM';
    h = h % 12 || 12;
    return (h < 10 ? '0' + h : h) + ':' + p[1] + ' ' + ap;
  }

  function render(rows) {
    rowsEl.innerHTML = '';
    if (!rows.length) {
      var tr = document.createElement('tr');
      var td = cell('Abhi schedule set nahi hai. Tab tak patients kisi bhi time par book kar sakte hain.');
      td.colSpan = 4;
      tr.appendChild(td);
      rowsEl.appendChild(tr);
      return;
    }
    rows.forEach(function (r) {
      var tr = document.createElement('tr');
      tr.appendChild(cell(r.day));
      tr.appendChild(cell(hhmm(r.start)));
      tr.appendChild(cell(hhmm(r.end)));

      var act = document.createElement('td');
      var edit = document.createElement('button');
      edit.className = 'mini ok';
      edit.textContent = 'Edit';
      edit.onclick = function () { startEdit(r); };
      var del = document.createElement('button');
      del.className = 'mini no';
      del.textContent = 'Delete';
      del.style.marginLeft = '6px';
      del.onclick = function () { removeRow(r); };
      act.appendChild(edit);
      act.appendChild(del);
      tr.appendChild(act);
      rowsEl.appendChild(tr);
    });
  }

  function load() {
    fetch(API, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (j.ok) render(j.rows);
        else showAlert(j.errors.__all__.join(' '), false);
      })
      .catch(function () { showAlert('Schedule load nahi hua. Internet check karein.', false); });
  }

  function startEdit(r) {
    editId = r.id;
    document.getElementById('id_weekday').value = r.weekday;
    document.getElementById('id_start_time').value = r.start;
    document.getElementById('id_end_time').value = r.end;
    title.textContent = 'Time badlein';
    submitBtn.textContent = 'Update';
    cancelBtn.style.display = 'block';
    clearErrors();
    form.scrollIntoView({ behavior: 'smooth' });
  }

  function resetForm() {
    editId = null;
    form.reset();
    title.textContent = 'Naya time jodein';
    submitBtn.textContent = 'Add';
    cancelBtn.style.display = 'none';
    clearErrors();
  }

  cancelBtn.onclick = resetForm;

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    clearErrors();
    submitBtn.disabled = true;
    var url = editId ? API + editId + '/update/' : API + 'add/';
    var data = {
      weekday: document.getElementById('id_weekday').value,
      start_time: document.getElementById('id_start_time').value,
      end_time: document.getElementById('id_end_time').value
    };
    post(url, data).then(function (res) {
      if (res.json.ok) {
        showAlert(editId ? 'Schedule update ho gaya.' : 'Schedule me jod diya gaya.', true);
        resetForm();
        load();
      } else {
        showErrors(res.json.errors || {});
      }
    }).catch(function () {
      showAlert('Kuch galat hua. Dobara try karein.', false);
    }).then(function () { submitBtn.disabled = false; });
  });

  function removeRow(r) {
    if (!confirm(r.day + ' ' + r.start + ' wala time hatana hai?')) return;
    post(API + r.id + '/delete/', {}).then(function (res) {
      if (res.json.ok) { showAlert('Schedule se hata diya gaya.', true); load(); }
      else showAlert('Delete nahi hua.', false);
    }).catch(function () { showAlert('Kuch galat hua. Dobara try karein.', false); });
  }

  load();
})();