<template>
  <div class="map-wrapper">
    <div id="map"></div>
    <div class="search-container">
      <input v-model="keyword" placeholder="검색어를 입력하세요">
      <button @click="searchPlaces">검색</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      map: null,
      keyword: '',
      markers: [],
      defaultPosition: {
        lat: 37.50625 , // 멀티캠퍼스 위치 (기본값)
        lng: 127.03169444444445
      }
    }
  },
  mounted() {
    if (window.kakao && window.kakao.maps) {
      this.initMap();
    } else {
      this.loadKakaoMap();
    }
  },
  methods: {
    loadKakaoMap() {
      const script = document.createElement('script');
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=c56c3d493aee00d132376b3af3029173&autoload=false&libraries=services`;
      script.onload = () => window.kakao.maps.load(this.initMap);
      document.head.appendChild(script);
    },
    initMap() {
      // 사용자의 위치 가져오기 시도
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const userLat = position.coords.latitude;
            const userLng = position.coords.longitude;
            console.log('사용자 위치:', { lat: userLat, lng: userLng });
            
            this.createMap(userLat, userLng);
          },
          (error) => {
            console.error('위치 정보 가져오기 실패:', error);
            // 기본 위치(멀티캠퍼스)로 지도 생성
            this.createMap(this.defaultPosition.lat, this.defaultPosition.lng);
          }
        );
      } else {
        console.log('Geolocation이 지원되지 않음');
        this.createMap(this.defaultPosition.lat, this.defaultPosition.lng);
      }
    },
    createMap(lat, lng) {
      const container = document.getElementById('map');
      const options = {
        center: new window.kakao.maps.LatLng(lat, lng),
        level: 3
      };
      this.map = new window.kakao.maps.Map(container, options);
    },
    searchPlaces() {
      if (!this.keyword.trim()) {
        alert('검색어를 입력해주세요');
        return;
      }

      const places = new window.kakao.maps.services.Places();
      const options = {
        location: this.map.getCenter()
      };

      places.keywordSearch(this.keyword, (result, status) => {
        if (status === window.kakao.maps.services.Status.OK) {
          console.log('검색 결과:', result);
          this.displayMarkers(result);
        } else {
          console.error('검색 실패:', status);
          alert('검색 결과가 없습니다.');
        }
      }, options);
    },
    displayMarkers(places) {
      // 기존 마커들 제거
      this.markers.forEach(marker => marker.setMap(null));
      this.markers = [];

      // 새로운 마커들 생성
      places.forEach(place => {
        const marker = new window.kakao.maps.Marker({
          map: this.map,
          position: new window.kakao.maps.LatLng(place.y, place.x)
        });

        // 인포윈도우 생성
        const infowindow = new window.kakao.maps.InfoWindow({
          content: `<div style="padding:5px;font-size:12px;">${place.place_name}</div>`
        });

        // 마커에 마우스오버 이벤트 추가
        window.kakao.maps.event.addListener(marker, 'mouseover', () => {
          infowindow.open(this.map, marker);
        });

        // 마커에 마우스아웃 이벤트 추가
        window.kakao.maps.event.addListener(marker, 'mouseout', () => {
          infowindow.close();
        });

        this.markers.push(marker);
      });
    }
  }
}
</script>

<style scoped>
.map-wrapper {
  width: 100%;
  height: 100%;
  padding: 20px;
}

#map {
  width: 100%;
  height: 600px;
  margin-bottom: 20px;
}

.search-container {
  margin-top: 20px;
}

input {
  padding: 8px;
  margin-right: 10px;
}

button {
  padding: 8px 16px;
}
</style>