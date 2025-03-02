function initMap() {

  var kazakhstan = { lat: 48.0196, lng: 66.9237 };

  var map = new google.maps.Map(document.getElementById("map"), {
    zoom: 6,
    center: kazakhstan,
    mapTypeId: 'roadmap',
    styles: [
      {
        "elementType": "geometry",
        "stylers": [{ "color": "#212121" }]
      },
      {
        "elementType": "labels.text.fill",
        "stylers": [{ "color": "#ffffff" }]
      },
      {
        "elementType": "labels.text.stroke",
        "stylers": [{ "color": "#000000" }]
      },
      {
        "featureType": "water",
        "stylers": [{ "color": "#0e1626" }]
      },
      {
        "featureType": "road",
        "elementType": "geometry",
        "stylers": [{ "color": "#383838" }]
      },
      {
        "featureType": "poi",
        "stylers": [{ "visibility": "off" }]
      }
    ]
  });

  // Добавление границ Казахстана
  map.data.loadGeoJson('https://raw.githubusercontent.com/zhukovgreen/kz-geojson/master/kz-regions.json');

  map.data.setStyle({
    fillColor: '#FFD700',
    fillOpacity: 0.4,
    strokeColor: '#000',
    strokeWeight: 2
  });




  // Добавляем маркеры агропромышленных объектов
  var agroLocations = [
    // 🔹 Карагандинская область
    { name: "ТОО «Агрофирма Қарқаралы»", lat: 49.4183, lng: 75.4119 },
    { name: "ТОО «Шахтинская Агроферма»", lat: 49.7153, lng: 72.8654 },
    { name: "Фермерское хозяйство «Сарыарка»", lat: 49.9551, lng: 73.4662 },
    { name: "Элеватор «Темиртау Агро»", lat: 50.0545, lng: 72.9497 },
    { name: "Кооператив «Жанаарка Агро»", lat: 48.8595, lng: 71.6382 },

    // 🔹 Астана (Нур-Султан) и Акмолинская область
    { name: "Элеватор Астана", lat: 51.1801, lng: 71.446 },
    { name: "ТОО «АгроПром Астана»", lat: 51.1457, lng: 71.5012 },
    { name: "Фермерское хозяйство «Ақмола»", lat: 51.2069, lng: 70.9642 },
    { name: "Склад удобрений «АгроСнаб»", lat: 51.2309, lng: 71.4328 },
    { name: "ТОО «АгроЖайнақ»", lat: 51.2829, lng: 70.8957 },

    // 🔹 Другие регионы
    { name: "Ферма Актобе", lat: 50.28333, lng: 57.16667 },
    { name: "Агроцентр Шымкент", lat: 42.31773, lng: 69.59012 },
    { name: "Теплица Костанай", lat: 53.21402, lng: 63.62462 },
    { name: "Склад удобрений Алматы", lat: 43.25667, lng: 76.92861 },
    { name: "АгроПарк Павлодар", lat: 52.2833, lng: 76.9509 }
  ];

  // Добавляем маркеры на карту
  agroLocations.forEach(function (location) {
    var marker = new google.maps.Marker({
      position: { lat: location.lat, lng: location.lng },
      map: map,
      title: location.name
    });

    // Всплывающее окно с информацией
    var infoWindow = new google.maps.InfoWindow({
      content: `<h3>${location.name}</h3><p>Агропромышленный объект</p>`
    });

    // Открытие окна при клике на маркер
    marker.addListener("click", function () {
      infoWindow.open(map, marker);
    });
  });
}
initMap()