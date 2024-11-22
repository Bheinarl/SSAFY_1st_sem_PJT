<template>
  <div class="map-wrapper">
    <div id="map"></div>
    <div class="control-container">
      <button class="location-btn" @click="moveToCurrentLocation">
        현재 위치
      </button>
      <div class="search-container">
        <input v-model="keyword" placeholder="검색어를 입력하세요">
        <button @click="searchPlaces">검색</button>
      </div>
    </div>
    <!-- 검색 결과 목록 추가 -->
    <div class="search-results" v-if="searchResults.length">
      <div class="result-item" v-for="(place, index) in searchResults" :key="index" @click="moveToPlace(place)">
        <h3>{{ place.place_name }}</h3>
        <p class="address">{{ place.address_name }}</p>
        <p class="category">{{ place.category_name }}</p>
        <p class="phone">{{ place.phone || '전화번호 없음' }}</p>
      </div>
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
      searchResults: [], // 검색 결과 저장용 배열 추가
      currentMarker: null, // 현재 위치 마커
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
    // 현재 위치로 이동하는 메소드 추가
    moveToCurrentLocation() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            
            // 현재 위치로 지도 이동
            const moveLatLng = new window.kakao.maps.LatLng(lat, lng);
            this.map.setCenter(moveLatLng);
            this.map.setLevel(5);  // 기본 확대 레벨로 설정 (1~14, 숫자가 작을수록 확대)
            
            // 기존 현재 위치 마커 제거
            if (this.currentMarker) {
              this.currentMarker.setMap(null);
            }
            
            // 현재 위치 마커 생성
            this.currentMarker = new window.kakao.maps.Marker({
              position: moveLatLng,
              map: this.map
            });
            
            console.log('현재 위치:', { lat, lng });
          },
          (error) => {
            console.error('위치 정보 가져오기 실패:', error);
            alert('위치 정보를 가져올 수 없습니다.');
          },
          {
            enableHighAccuracy: true,  // 높은 정확도 사용
            maximumAge: 0,  // 캐시된 위치정보를 사용하지 않음
            timeout: 5000  // 5초 이내에 응답이 없으면 에러
          }



        );
      } else {
        alert('이 브라우저에서는 위치 정보를 사용할 수 없습니다.');
      }
    },


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

    // searchPlaces 메소드 수정
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
          console.log('****검색 결과:', result);
          this.searchResults = result; // 검색 결과 저장
          this.displayMarkers(result);
        } else {
          console.error('검색 실패:', status);
          this.searchResults = []; // 검색 결과 초기화
          alert('검색 결과가 없습니다.');
        }
      }, options);
    },

    // 장소로 이동하는 메소드 추가
    moveToPlace(place) {
      const moveLatLng = new window.kakao.maps.LatLng(place.y, place.x);
      this.map.setCenter(moveLatLng);
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
  position: relative;
}

#map {
  width: 100%;
  height: 600px;
  margin-bottom: 20px;
}

.control-container {
  position: absolute;
  top: 30px;
  left: 30px;
  z-index: 1;
  background: white;
  padding: 10px;
  border-radius: 4px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.location-btn {
  padding: 8px 16px;
  margin-bottom: 10px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
}

.location-btn:hover {
  background-color: #357abd;
}

.search-container {
  display: flex;
  gap: 8px;
}

input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  flex-grow: 1;
}

button {
  padding: 8px 16px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #357abd;
}

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
  margin-bottom: 20px;
}

input {
  padding: 8px;
  margin-right: 10px;
  width: 300px;
}

button {
  padding: 8px 16px;
}

.search-results {
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #0026ff;
  border-radius: 4px;
}

.result-item {
  padding: 15px;
  border-bottom: 1px solid #5683ff;
  cursor: pointer;
  transition: background-color 0.2s;
}

.result-item:hover {
  background-color: #a1bfff;
}

.result-item h3 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #333;
}

.result-item p {
  margin: 4px 0;
  font-size: 14px;
  color: #666;
}

.result-item .address {
  color: #2c5282;
}

.result-item .category {
  color: #718096;
}

.result-item .phone {
  color: #4a5568;
}

</style>