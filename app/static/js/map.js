let selfLon;
let selfLat;

function initialize() {
    this.map = new BMap.Map('mapContainer');
    map.centerAndZoom(new BMap.Point(121.491, 31.233), 11);
    map.enableScrollWheelZoom(true);     //开启鼠标滚轮缩放
    // 创建定位控件
    var locationControl = new BMap.GeolocationControl({
        // 控件的停靠位置（可选，默认左上角）
        anchor: BMAP_ANCHOR_TOP_RIGHT,
        // 控件基于停靠位置的偏移量（可选）
        offset: new BMap.Size(20, 20)
    });
    // 将控件添加到地图上
    map.addControl(locationControl);
    // 添加定位事件
    locationControl.addEventListener("locationSuccess", function (e) {
        var address = '';
        address += e.addressComponent.province;
        address += e.addressComponent.city;
        address += e.addressComponent.district;
        address += e.addressComponent.street;
        address += e.addressComponent.streetNumber;
        alert("当前定位地址为：" + address);
    });
    locationControl.addEventListener("locationError", function (e) {
        alert(e.message);
    });
    getLocation();

}

// 点击展示模态框
function mapShow() {
    $('#mapModal').modal('show');
}

function getLocation() {
    // 创建百度地理位置实例，代替 navigator.geolocation
    var geolocation = new BMap.Geolocation();
    geolocation.getCurrentPosition(function(e) {
        if(this.getStatus() == BMAP_STATUS_SUCCESS){
            // 百度 geolocation 的经纬度属性不同，此处是 point.lat 而不是 coords.latitude
            window.selfLon = e.point.lng;
            window.selfLat = e.point.lat;
            console.log('纬度：' + window.selfLon + '经度：' + window.selfLat);
        } else {
            console.log('failed' + this.getStatus());
        }
    });
}

function drivingRoute(lon,lat) {
    var driving = new BMap.DrivingRoute(this.map, {
        renderOptions: {
            map: this.map,
            autoViewport: true
        }
    });
    console.log(window.selfLon)
    var start = new BMap.Point(window.selfLon, window.selfLat);
    var end = new BMap.Point(lon, lat);
    console.log(start,end)
    driving.search(start, end);
}
