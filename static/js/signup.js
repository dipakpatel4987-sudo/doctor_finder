(function () {
  var pass = function () { return document.getElementById('id_password').value; };
  var rules = {
    id_first_name: function (v) { return v.trim().length >= 3 ? '' : 'Naam kam se kam 3 akshar ka ho'; },
    id_email: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) ? '' : 'Sahi email daalein'; },
    id_phone: function (v) { return /^[6-9]\d{9}$/.test(v) ? '' : '10 digit number (6-9 se shuru)'; },
    id_password: function (v) { return v.length >= 8 ? '' : 'Password kam se kam 8 akshar ka ho'; },
    id_confirm: function (v) { return (v !== '' && v === pass()) ? '' : 'Password match nahi karta'; },
    id_role: function (v) { return v ? '' : 'Patient ya Doctor chuniye'; }
  };

  function check(id) {
    var el = document.getElementById(id);
    var msg = rules[id](el.value);
    el.nextElementSibling.textContent = msg;
    el.classList.remove('valid', 'invalid');
    el.classList.add(msg ? 'invalid' : 'valid');
    return msg === '';
  }

  Object.keys(rules).forEach(function (id) {
    var el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('input', function () {
      check(id);
      if (id === 'id_password' && document.getElementById('id_confirm').value) check('id_confirm');
    });
    el.addEventListener('change', function () { check(id); });
  });

  document.getElementById('signup-form').addEventListener('submit', function (e) {
    var ok = true;
    Object.keys(rules).forEach(function (id) { if (!check(id)) ok = false; });
    if (!ok) e.preventDefault();
  });
})();