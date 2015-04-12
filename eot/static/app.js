/**
 * Created by codeadict on 4/11/15.
 */

/* create Basemap Layers */

var template = "//map1{s}.vis.earthdata.nasa.gov/wmts-geo/{layer}/default/{time}/{tileMatrixSet}/{z}/{y}/{x}.jpg";

var api_endpoint = "http://eyes-of-time.herokuapp.com";

var nasaLayer = L.tileLayer(template, {
    layer: "MODIS_Terra_CorrectedReflectance_TrueColor",
    tileMatrixSet: "EPSG4326_250m",
    time: "2013-11-04",
    tileSize: 512,
    subdomains: "abc",
    noWrap: true,
    continuousWorld: true,
    // Prevent Leaflet from retrieving non-existent tiles on the
    // borders.
    bounds: [
        [-89.9999, -179.9999],
        [89.9999, 179.9999]
    ]
});


var EPSG4326 = new L.Proj.CRS(
    "EPSG:4326",
    "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs", {
        origin: [-180, 90],
        resolutions: [
            0.5625,
            0.28125,
            0.140625,
            0.0703125,
            0.03515625,
            0.017578125,
            0.0087890625,
            0.00439453125,
            0.002197265625
        ],
        // Values are x and y here instead of lat and long elsewhere.
        bounds: [
            [-180, -90],
            [180, 90]
        ]
    }
);

/* Overlay Layers *//*
 var highlight = L.geoJson(null);
 var highlightStyle = {
 stroke: false,
 fillColor: "#00FFFF",
 fillOpacity: 0.7,
 radius: 10
 };

 map = L.map("map", {
 zoom: 2,
 maxZoom: 8,
 center: [0, 0],
 zoomControl: false,
 attributionControl: false,
 crs: EPSG4326,
 maxBounds: [
 [-120, -220],
 [120, 220]
 ]
 });

 map.addLayer(nasaLayer);*/

/* add points */
L.layerJSON({
    url: "/static/js/test-data.json",
    propertyLoc: ['lat', 'lon'],
    propertyTitle: 'description',
    minShift: Infinity,
    caching: true,
    buildPopup: function (data) {
        return L.Util.template("<p>{description}</p>", {
            description: data.description
        });
    },
    optsPopup: {'closeButton': false, focus: true}
})
    .on('dataloaded', function (e) {
        setTimeout(function () {
            map.fitBounds(e.target.getBounds()); //zoom to all data
        }, 100);
    })
//.addTo(map);

//map.addLayer(highlight);


var eyesoftimeApp = angular.module('eyesoftimeApp', ["leaflet-directive"])
eyesoftimeApp.controller('FindingListController', function ($scope, $http) {
    var findingList = this;
    $http.get(api_endpoint + "/events/")
        .then(function (res) {
            findingList.events = res.data;
        });

    findingList.highlight = function () {
        highlight.clearLayers().addLayer(L.circleMarker([$(this).attr("lat"), $(this).attr("lon")], highlightStyle));
    };

    $scope.Lat = false;
    $scope.Lon = false;
    $scope.showModal = false;
    $scope.toggleModal = function () {
        $scope.showModal = !$scope.showModal;
    };

    $scope.$on('leafletDirectiveMap.click', function (event, args) {
        var latlng = args.leafletEvent.latlng;
        $scope.Lat = latlng.lat;
        $scope.Lon = latlng.lng;
        $scope.toggleModal();
    });

    $scope.registerEvent = function () {
        $http({
            url: api_endpoint + '/events/',
            method: "POST",
            data: {
                'description': message,
                'lat': $scope.Lat,
                'lon': $scope.Lon
            }
        });
    };

    angular.extend($scope, {
        events: {
            map: {
                enable: ['click', 'drag', 'blur', 'touchstart'],
                logic: 'emit'
            }
        },
        maxBounds: [
            [-120, -220],
            [120, 220]
        ],
        attributionControl: false,
        crs: EPSG4326,
        center: {
            lat: 0,
            lng: 0,
            zoom: 2
        },
        maxBounds: [
            [-120, -220],
            [120, 220]
        ],
        layers: {
            baselayers: {
                nasa_terra_true_color: {
                    name: 'MODIS_Terra_CorrectedReflectance_TrueColor',
                    type: 'xyz',
                    url: template,
                    layerOptions: {
                        layer: "MODIS_Terra_CorrectedReflectance_TrueColor",
                        tileMatrixSet: "EPSG4326_250m",
                        time: "2013-11-04",
                        tileSize: 512,
                        subdomains: "abc",
                        noWrap: true,
                        continuousWorld: true,
                        // Prevent Leaflet from retrieving non-existent tiles on the
                        // borders.
                        bounds: [
                            [-89.9999, -179.9999],
                            [89.9999, 179.9999]
                        ]
                    }
                }
            }
        },
        defaults: {
            doubleClickZoom: false,
            maxBounds: [
                [-120, -220],
                [120, 220]
            ],
            attributionControl: false,
            crs: EPSG4326,
            maxZoom: 8,
            minZoom: 1,
            zoom: 2,
            scrollWheelZoom: true
        }
    });
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

