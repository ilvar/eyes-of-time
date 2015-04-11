angular.module('eot.controllers', [])

    .controller('MapCtrl', function ($scope, $ionicModal, $http, $interval) {
        $scope.resetEvent = function() {
            $scope.newEvent = {
                lat: null,
                lon: null,
                description: ''
            };
        };

        $scope.resetEvent();

        $scope.map = L.map("map", {
            center: [0, 0],
            doubleClickZoom: false,
            zoom: 3,
            maxZoom: 9
        });

        var layer = L.tileLayer('https://map1.vis.earthdata.nasa.gov/wmts-webmerc/MODIS_Terra_CorrectedReflectance_TrueColor/default/{time}/{tilematrixset}{maxZoom}/{z}/{y}/{x}.{format}', {
            attribution: 'Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.',
            bounds: [[-90, -180], [90, 180]],
            minZoom: 1,
            maxZoom: 9,
            format: 'jpg',
            time: '2015-04-08',
            tilematrixset: 'GoogleMapsCompatible_Level'
        });

        $scope.map.addLayer(layer);

        $scope.markers = [];

        $scope.$watch('events', function(events_list) {
            if (!events_list) {
                return
            }
            _.each(events_list, function(e) {
                var existing_markers = _.filter($scope.markers, function(m) {
                    return m.getLatLng().lat == e.coordinates[0] && m.getLatLng().lon == e.coordinates[1];
                });
                if (!existing_markers.length) {
                    var marker = L.marker(e.coordinates);
                    marker.bindPopup(e.description);
                    $scope.markers.push(marker);
                    marker.addTo($scope.map)
                }
            });
        });

        $scope.onMapClick = function(e) {
            $scope.newEvent.lat = e.latlng.lat;
            $scope.newEvent.lon = e.latlng.lng;
            $scope.openModal();
        };

        $scope.map.on('dblclick', $scope.onMapClick);

        $scope.openModal = function () {
            $scope.modal.show();
        };

        $scope.closeModal = function () {
            $scope.modal.hide();
        };

        $scope.url = 'http://eyes-of-time.herokuapp.com/events/';

        $scope.saveEvent = function() {
            $http.post($scope.url, $scope.newEvent, {withCredentials: true}).success(function(result) {
                if (!result.error) {
                    $scope.events = result;
                    $scope.resetEvent();
                    $scope.closeModal();
                } else {
                    alert(result.error);
                    alert(top.location);
                }
            });
        };

        $scope.loadEvents = function() {
            $http.get($scope.url, {withCredentials: true}).success(function(result) {
                $scope.events = result;
            });
        };

        $scope.loadEvents();
        $interval($scope.loadEvents, 60 * 1000); // 1 minute

        $ionicModal.fromTemplateUrl('add-modal.html', {
            scope: $scope,
            animation: 'slide-in-up'
        }).then(function (modal) {
            $scope.modal = modal;
        });

        top.map = $scope.map;

    })

    .controller('RatingCtrl', function ($scope, $http) {
        $scope.users = [];

        $http.get('http://eyes-of-time.herokuapp.com/rating/').success(function(result) {
            $scope.users = result;
        });
    })

    .controller('AccountCtrl', function ($scope, $http) {
        $scope.user = null;

        $http.get('http://eyes-of-time.herokuapp.com/profile/', {withCredentials: true}).success(function(result) {
            $scope.user = result;
        });
    });
