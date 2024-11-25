<template>
  <div class="map-wrapper">
    <!-- 카카오맵이 표시될 div -->
    <div id="map"></div>

    <!-- 컨트롤 영역 (현재 위치 버튼, 검색창+검색버튼) -->
    <div class="control-container"> 
      <button class="location-btn" @click="moveToCurrentLocation">
        현재 위치
      </button>
      <div class="search-container">
        <input v-model="keyword" placeholder="검색어를 입력하세요">
        <button @click="searchPlaces">검색</button>
      </div>
    </div>
    
     <!-- 검색 결과 목록 (검색 결과가 있을 때만 표시) -->
    <div class="search-results" v-if="searchResults.length">
      <div class="result-item" v-for="(place, index) in searchResults" :key="index" @click="moveToPlace(place)">
        <h3>{{ place.place_name }}</h3>
        <p class="address">{{ place.address_name }}</p>
        <p class="category">{{ place.category_name }}</p>
        <p class="distance">{{ place.distance.toFixed(2) }} km</p>
        <p class="phone">{{ place.phone ? place.phone : '전화번호 없음' }}</p>
      </div>
    </div>
  </div>
  
</template>

<script>
import markerCurrent from '@/assets/markers/marker-current.png'
import markerDefault from '@/assets/markers/marker-default.png'
import markerSelected from '@/assets/markers/marker-selected.png'
import { useRoute } from 'vue-router';

export default {
  data() {
    return {
      map: null,            // 카카오맵 인스턴스
      keyword: '',          // 검색 키워드
      markers: [],          // 검색 결과 마커 배열
      searchResults: [],    // 검색 결과 저장용 배열 추가
      currentMarker: null,  // 현재 위치 마커
      defaultPosition: {    // 기본 위치(멀티캠퍼스)
        lat: 37.50625 , 
        lng: 127.03169444444445
      }
    }
  },

  mounted() {
    // 키워드를 Router Query에서 가져오기
    const route = useRoute();
    this.keyword = route.query.keyword || ''; // URL에서 전달된 쿼리 값 읽기

    // 카카오맵이 로드되어 있다면 초기화, 그렇지 않다면 로드 후 초기화
    if (window.kakao && window.kakao.maps) {
      this.initMap();
    } else {
      this.loadKakaoMap();
    }

    // 키워드 검색 실행
    if (this.keyword) {
      setTimeout(() => {
        this.searchPlaces();
      }, 1000); // 맵 로딩 완료 후 검색
    }
  },

  methods: {
    
    // 현재 위치로 이동하는 메소드
    moveToCurrentLocation() {
      if (navigator.geolocation) {
        // 현재 위치 가져오기
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            
            // 현재 위치로 지도 중심 이동 및 확대 레벨 설정(1~14, 숫자가 작을수록 확대)
            const moveLatLng = new window.kakao.maps.LatLng(lat, lng);
            this.map.setCenter(moveLatLng);
            this.map.setLevel(2);


            // 현재 위치 마커 생성
            const currentMarkerImage = new window.kakao.maps.MarkerImage(
              markerCurrent,
              new window.kakao.maps.Size(24, 35)
            );

            if (this.currentMarker) { // 기존 마커 제거
              this.currentMarker.setMap(null);
            }

            this.currentMarker = new window.kakao.maps.Marker({ // 현재 위치용 마커 이미지 설정(빨간색🔴)
              position: moveLatLng,
              map: this.map,
              image: currentMarkerImage
            });
            
            console.log('현재 위치:', { lat, lng }); // 디버깅용
          },

          (error) => {
            console.error('위치 정보 가져오기 실패:', error);
            alert('위치 정보를 가져올 수 없습니다.');
          },
          {
            enableHighAccuracy: true,  // 현재 위치 값 <-> 검색한 위치 값 사이 정밀한 비교를 위해 높은 정확도 사용
            maximumAge: 0,  // 캐시된 위치정보를 사용하지 않음
            timeout: 5000  // 5초 이내에 응답이 없으면 에러
          }
        );
      } else {
        alert('이 브라우저에서는 위치 정보를 사용할 수 없습니다.');
      }
    },

    // 카카오맵 스크립트를 동적으로 로드
    loadKakaoMap() {
      const script = document.createElement('script');
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=c56c3d493aee00d132376b3af3029173&autoload=false&libraries=services`;
      script.onload = () => window.kakao.maps.load(this.initMap);
      document.head.appendChild(script);
    },

    // 맵 초기화 함수
    initMap() {
      // 사용자의 위치 가져오기 시도
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const userLat = position.coords.latitude;
            const userLng = position.coords.longitude;
            console.log('사용자 위치:', { lat: userLat, lng: userLng }); // 디버깅용
            this.createMap(userLat, userLng); // 사용자의 현재 위치 중심으로 지도 생성
            this.moveToCurrentLocation(); // 초기 위치 이동
          },
          (error) => {
            console.error('위치 정보 가져오기 실패:', error);
            this.createMap(this.defaultPosition.lat, this.defaultPosition.lng); // 기본 위치(멀티캠퍼스)로 지도 생성
          }
        );
      } else {
        console.log('Geolocation이 지원되지 않음');
        this.createMap(this.defaultPosition.lat, this.defaultPosition.lng);
      }
    },

    // 지도를 생성하는 함수
    createMap(lat, lng) {
      const container = document.getElementById('map');
      const options = {
        center: new window.kakao.maps.LatLng(lat, lng), // 지도 중심 좌표 설정
        level: 3 // 기본적으로 지도 확대 레벨 3으로 설정
      };
      this.map = new window.kakao.maps.Map(container, options);
    },

    // 두 좌표 간 거리 계산 함수
    calculateDistance(lat1, lng1, lat2, lng2) {
      const R = 6371; // 지구의 반지름 (km)
      const dLat = this.toRad(lat2 - lat1);
      const dLng = this.toRad(lng2 - lng1);
      const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                Math.cos(this.toRad(lat1)) * Math.cos(this.toRad(lat2)) * 
                Math.sin(dLng/2) * Math.sin(dLng/2);
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
      return R * c;
    },

    // 라디안 값으로 변환
    toRad(value) {
      return value * Math.PI / 180;
    },


    // 검색어로 장소 검색
    searchPlaces() {
      if (!this.keyword.trim()) {
        alert('검색어를 입력해주세요');
        return;
      }

      const places = new window.kakao.maps.services.Places();
      const options = {
        location: this.map.getCenter() // 현재 지도 중심으로 검색
      };

      places.keywordSearch(this.keyword, (result, status) => {
        if (status === window.kakao.maps.services.Status.OK) {
          // 거리 계산을 위해 현 위치 가져오기
          const currentLat = this.currentMarker ? this.currentMarker.getPosition().getLat() : this.map.getCenter().getLat();
          const currentLng = this.currentMarker ? this.currentMarker.getPosition().getLng() : this.map.getCenter().getLng();

          // 거리 계산 및 사용자의 현 위치에서 가까운 순으로 정렬
          result.forEach(place => {
            place.distance = this.calculateDistance(
              currentLat, 
              currentLng,
              parseFloat(place.y), 
              parseFloat(place.x)
            );
          });
          const sortedResult = result.sort((a, b) => a.distance - b.distance);
          console.log('정렬된 검색 결과:', sortedResult);

          this.searchResults = sortedResult; // 정렬된 결과 저장
          this.displayMarkers(sortedResult); // 검색 결과 마커 표시
        } else {
          console.error('검색 실패:', status);
          this.searchResults = [];
          alert('검색 결과가 없습니다.');
        }
      }, options);
    },

    // 검색 결과 마커 표시
    displayMarkers(places) {
      this.markers.forEach(marker => marker.setMap(null)); // 기존 마커 해제
      this.markers = []; // 검색 결과 마커 여러개 담을 빈 배열
      this.map.setLevel(5);  // 확대 레벨 설정 (1~14, 숫자가 작을수록 확대)

      const defaultMarkerImage = new window.kakao.maps.MarkerImage( // 검색 결과용 기본 마커 이미지 설정(파란색🔵)
        markerDefault,
        new window.kakao.maps.Size(24, 35)
      );

      places.forEach(place => {
        const marker = new window.kakao.maps.Marker({
          map: this.map,
          position: new window.kakao.maps.LatLng(place.y, place.x),
          image: defaultMarkerImage
        });

        const infowindow = new window.kakao.maps.InfoWindow({
          content: `<div style="padding:5px;font-size:12px;">${place.place_name}</div>`
        });

        // 마커 이벤트 - 마우스 위로 올리면 정보 보임
        window.kakao.maps.event.addListener(marker, 'mouseover', () => {
          infowindow.open(this.map, marker);
        });
        window.kakao.maps.event.addListener(marker, 'mouseout', () => {
          infowindow.close();
        });

        this.markers.push(marker);
      });
    },

    // 선택한 장소로 이동
    moveToPlace(place) {
      const moveLatLng = new window.kakao.maps.LatLng(place.y, place.x);
      this.map.setLevel(3);
      this.map.setCenter(moveLatLng);

      const defaultMarkerImage = new window.kakao.maps.MarkerImage(
        markerDefault,
        new window.kakao.maps.Size(24, 35)
      );
      
      const selectedMarkerImage = new window.kakao.maps.MarkerImage( // 선택된 장소용 마커 이미지(초록색🟢)
        markerSelected,
        new window.kakao.maps.Size(24, 35)
      );


      // 검색 결과의 인덱스를 이용하여 마커 찾기 - 선택된 마커 이미지 업데이트
      this.searchResults.forEach((searchPlace, index) => {
        if (searchPlace.id === place.id) {  // 장소 ID로 비교
          this.markers[index].setImage(selectedMarkerImage);
        } else {
          this.markers[index].setImage(defaultMarkerImage);
        }
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
.result-item .distance {
  color: #2b6cb0;
  font-weight: bold;
}
</style>