(function () {
  var doctors = JSON.parse(document.getElementById('doctors-data').textContent);
  var listEl = document.getElementById('list');
  var layout = document.getElementById('layout');
  var markers = [], userPos = null;

  var map = L.map('map').setView([22.3, 72.6], 7);
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  function esc(s) {
    var d = document.createElement('div');
    d.textContent = s == null ? '' : s;
    return d.innerHTML;
  }

  doctors.forEach(function (d) {
    var m = L.marker([d.lat, d.lng]).addTo(map);
    m.bindPopup('<b>' + esc(d.name) + '</b><br>' + esc(d.specialty) + '<br>' + esc(d.phone) +
      '<br><a href="/doctors/' + d.id + '/">View Profile</a>');
    markers.push(m);
  });

  function km(a, b, c, d) {
    var R = 6371, p = Math.PI / 180, dLat = (c - a) * p, dLng = (d - b) * p;
    var x = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(a * p) * Math.cos(c * p) * Math.sin(dLng / 2) * Math.sin(dLng / 2);
    return R * 2 * Math.atan2(Math.sqrt(x), Math.sqrt(1 - x));
  }

  function showMap() {
    layout.className = 'map-layout show-map';
    document.getElementById('t-map').className = 'on';
    document.getElementById('t-list').className = '';
    setTimeout(function () { map.invalidateSize(); }, 100);
  }

  function focusDoctor(i) {
    map.setView([doctors[i].lat, doctors[i].lng], 13);
    markers[i].openPopup();
    showMap();
  }

  function render(filter) {
    listEl.innerHTML = '';
    doctors.forEach(function (d, i) {
      if (filter && d.city.toLowerCase().indexOf(filter.toLowerCase()) === -1) return;
      var dist = userPos ? ' · ' + km(userPos.lat, userPos.lng, d.lat, d.lng).toFixed(1) + ' km' : '';
      var div = document.createElement('div');
      div.className = 'map-item';
      div.innerHTML = '<h4>' + esc(d.name) + '</h4><small>' + esc(d.specialty) + '</small>' +
        '<p>' + esc(d.city) + dist + '<br>' + esc(d.phone) + '</p>' +
        '<a target="_blank" rel="noopener" href="https://www.openstreetmap.org/directions?to=' +
        d.lat + ',' + d.lng + '">Get Directions</a>';
      div.addEventListener('click', function (e) {
        if (e.target.tagName !== 'A') focusDoctor(i);
      });
      listEl.appendChild(div);
    });
    if (!listEl.children.length) listEl.innerHTML = '<p style="padding:14px;color:#777">Koi doctor nahi mila.</p>';
  }

  document.getElementById('city').addEventListener('input', function () { render(this.value); });

  document.getElementById('near').addEventListener('click', function () {
    if (!navigator.geolocation) { alert('Browser location support nahi karta.'); return; }
    navigator.geolocation.getCurrentPosition(function (p) {
      userPos = { lat: p.coords.latitude, lng: p.coords.longitude };
      render(document.getElementById('city').value);
      map.setView([userPos.lat, userPos.lng], 10);
      L.circleMarker([userPos.lat, userPos.lng], { radius: 8, color: '#0b3b5c' })
        .addTo(map).bindPopup('Aap yahan ho');
    }, function () { alert('Location allow nahi hui.'); });
  });

  document.getElementById('t-list').onclick = function () {
    layout.className = 'map-layout show-list';
    this.className = 'on';
    document.getElementById('t-map').className = '';
  };
  document.getElementById('t-map').onclick = showMap;

  render('');
})();