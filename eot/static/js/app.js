/**
 * Created by codeadict on 4/11/15.
 */

//var api_endpoint = "http://eyes-of-time.herokuapp.com";
var api_endpoint = "http://localhost:8000";


var eyesoftimeApp = angular.module('eyesoftimeApp', [])
  .config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
  });
eyesoftimeApp.controller('FindingListController', function ($scope, $http, $interval) {
  $scope.resetEvent = function () {
    $scope.newEvent = {
      lat: null,
      lon: null,
      description: ''
    };
  };

  $scope.resetEvent();

  $scope.map = L.map("map", {
    center: [0, 0],
    attributionControl: false,
    doubleClickZoom: false,
    zoomControl: true,
    fullscreenControl: true,
    zoom: 3,
    maxZoom: 9
  });

  /* GPS enabled geolocation control set to follow the user's location */
  var locateControl = L.control.locate({
    position: "topright",
    drawCircle: true,
    follow: true,
    setView: true,
    keepCurrentZoomLevel: true,
    markerStyle: {
      weight: 1,
      opacity: 0.8,
      fillOpacity: 0.8
    },
    circleStyle: {
      weight: 1,
      clickable: false
    },
    icon: "icon-direction",
    metric: false,
    strings: {
      title: "My location",
      popup: "You are within {distance} {unit} from this point",
      outsideMapBoundsMsg: "You seem located outside the boundaries of the map"
    },
    locateOptions: {
      maxZoom: 5,
      watch: true,
      enableHighAccuracy: true,
      maximumAge: 10000,
      timeout: 10000
    }
  }).addTo($scope.map);

  var layer = L.tileLayer('https://map1.vis.earthdata.nasa.gov/wmts-webmerc/MODIS_Terra_CorrectedReflectance_TrueColor/default/{time}/{tilematrixset}{maxZoom}/{z}/{y}/{x}.{format}', {
    attribution: 'Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.',
    bounds: [
      [-90, -180],
      [90, 180]
    ],
    minZoom: 1,
    maxZoom: 9,
    format: 'jpg',
    time: '2015-04-08',
    tilematrixset: 'GoogleMapsCompatible_Level'
  });

  $scope.map.addLayer(layer);

  $scope.markers = [];

  $scope.$watch('events', function (events_list) {
    if (!events_list) {
      return
    }
    _.each(events_list, function (e) {
      var existing_markers = _.filter($scope.markers, function (m) {
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

  $scope.toggleSidebar = function () {
    $("#sidebar").toggle();
    $scope.map.invalidateSize();
    return false;
  }

  $scope.showModal = false;

  $scope.onMapClick = function (event) {
    $scope.newEvent.lat = event.latlng.lat;
    $scope.newEvent.lon = event.latlng.lng;
    $scope.toggleModal();
  };


  $scope.map.on('dblclick', $scope.onMapClick);

  $scope.toggleModal = function () {
    $scope.showModal = !$scope.showModal;
  };

  $scope.registerEvent = function () {
    $http.post(api_endpoint + '/events/', $scope.newEvent, {withCredentials: true}).success(function (result) {
      if (!result.error) {
        $scope.events = result;
        $scope.resetEvent();
        $scope.toggleModal();
      } else {
        alert(result.error);
      }
    });
  };

  $scope.loadEvents = function () {
    $http.get(api_endpoint + '/events/', {withCredentials: true}).success(function (result) {
      $scope.events = result;
    });
  };

  $scope.loadEvents();
  $interval($scope.loadEvents, 60 * 1000); // 1 minute

});

eyesoftimeApp.directive('modal', function () {
  return {
    template: '<div class="modal fade" tabindex="-1" role="dialog">' +
      '<div class="modal-dialog">' +
      '<div class="modal-content">' +
      '<div class="modal-header">' +
      '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>' +
      '<h4 class="modal-title">{{ title }}</h4>' +
      '</div>' +
      '<div class="modal-body" ng-transclude></div>' +
      '</div>' +
      '</div>' +
      '</div>',
    restrict: 'E',
    transclude: true,
    replace: true,
    scope: true,
    link: function postLink(scope, element, attrs) {
      scope.title = attrs.title;

      scope.$watch(attrs.visible, function (value) {
        if (value == true)
          $(element).modal('show');
        else
          $(element).modal('hide');
      });

      $(element).on('shown.bs.modal', function () {
        scope.$apply(function () {
          scope.$parent[attrs.visible] = true;
        });
      });

      $(element).on('hidden.bs.modal', function () {
        scope.$apply(function () {
          scope.$parent[attrs.visible] = false;
        });
      });
    }
  };
});

