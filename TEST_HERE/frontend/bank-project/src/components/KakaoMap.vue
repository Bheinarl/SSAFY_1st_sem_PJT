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
      markers: []
    }
  },
  mounted() {
    console.log('컴포넌트 마운트됨');
    if (window.kakao && window.kakao.maps) {
      console.log('카카오맵 SDK 이미 로드됨');
      this.initMap();
    } else {
      console.log('카카오맵 SDK 로드 시작');
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
      navigator.geolocation.getCurrentPosition((position) => {
        const container = document.getElementById('map');
        const options = {
          center: new window.kakao.maps.LatLng(
            position.coords.latitude,
            position.coords.longitude
          ),
          level: 3
        };
        this.map = new window.kakao.maps.Map(container, options);
      });
    },
    searchPlaces() {
      if (!this.keyword.trim()) {
        alert('검색어를 입력해주세요');
        return;
      }

      const places = new window.kakao.maps.services.Places();
      places.keywordSearch(this.keyword, (result, status) => {
        if (status === window.kakao.maps.services.Status.OK) {
          console.log('검색 결과:', result);
          this.displayMarkers(result);
        } else {
          console.error('검색 실패:', status);
          alert('검색 결과가 없습니다.');
        }
      });
    },
    displayMarkers(places) {
      this.markers.forEach(marker => marker.setMap(null));
      this.markers = places.map(place => {
        const marker = new window.kakao.maps.Marker({
          map: this.map,
          position: new window.kakao.maps.LatLng(place.y, place.x)
        });
        return marker;
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
  height: 600px;  /* 높이를 명시적으로 지정 */
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