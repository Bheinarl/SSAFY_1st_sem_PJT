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

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import markerCurrent from '@/assets/markers/marker-current.png';
import markerDefault from '@/assets/markers/marker-default.png';
import markerSelected from '@/assets/markers/marker-selected.png';

const map = ref(null);  // 카카오맵 인스턴스
const keyword = ref('');  // 검색 키워드
const markers = ref([]);  // 검색 결과 마커 배열
const searchResults = ref([]);  // 검색 결과 저장용 배열
const currentMarker = ref(null);  // 현재 위치 마커
const defaultPosition = {  // 기본 위치(멀티캠퍼스)
  lat: 37.50625, 
  lng: 127.03169444444445
};

// 키워드를 Router Query에서 가져오기
const route = useRoute();
keyword.value = route.query.keyword || ''; // URL에서 전달된 쿼리 값 읽기

onMounted(() => {
  // 카카오맵이 로드되어 있다면 초기화, 그렇지 않다면 로드 후 초기화
  if (window.kakao && window.kakao.maps) {
    initMap();
  } else {
    loadKakaoMap();
  }

  // 키워드 검색 실행
  if (keyword.value) {
    setTimeout(() => {
      searchPlaces();
    }, 1000); // 맵 로딩 완료 후 검색
  }
});

// 현재 위치로 이동하는 메소드
const moveToCurrentLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        const moveLatLng = new window.kakao.maps.LatLng(lat, lng);
        map.value.setCenter(moveLatLng);
        map.value.setLevel(2);

        const currentMarkerImage = new window.kakao.maps.MarkerImage(
          markerCurrent,
          new window.kakao.maps.Size(24, 35)
        );

        if (currentMarker.value) { // 기존 마커 제거
          currentMarker.value.setMap(null);
        }

        currentMarker.value = new window.kakao.maps.Marker({
          position: moveLatLng,
          map: map.value,
          image: currentMarkerImage
        });

        console.log('현재 위치:', { lat, lng }); // 디버깅용
      },
      (error) => {
        console.error('위치 정보 가져오기 실패:', error);
        alert('위치 정보를 가져올 수 없습니다.');
      },
      {
        enableHighAccuracy: true,
        maximumAge: 0,
        timeout: 5000
      }
    );
  } else {
    alert('이 브라우저에서는 위치 정보를 사용할 수 없습니다.');
  }
};

// 카카오맵 스크립트를 동적으로 로드
const loadKakaoMap = () => {
  const script = document.createElement('script');
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=c56c3d493aee00d132376b3af3029173&autoload=false&libraries=services`;
  script.onload = () => window.kakao.maps.load(initMap);
  document.head.appendChild(script);
};

// 맵 초기화 함수
const initMap = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const userLat = position.coords.latitude;
        const userLng = position.coords.longitude;
        console.log('사용자 위치:', { lat: userLat, lng: userLng });
        createMap(userLat, userLng);
        moveToCurrentLocation();
      },
      (error) => {
        console.error('위치 정보 가져오기 실패:', error);
        createMap(defaultPosition.lat, defaultPosition.lng);
      }
    );
  } else {
    console.log('Geolocation이 지원되지 않음');
    createMap(defaultPosition.lat, defaultPosition.lng);
  }
};

// 지도를 생성하는 함수
const createMap = (lat, lng) => {
  const container = document.getElementById('map');
  const options = {
    center: new window.kakao.maps.LatLng(lat, lng),
    level: 3
  };
  map.value = new window.kakao.maps.Map(container, options);
};

// 두 좌표 간 거리 계산 함수
const calculateDistance = (lat1, lng1, lat2, lng2) => {
  const R = 6371; // 지구의 반지름 (km)
  const dLat = toRad(lat2 - lat1);
  const dLng = toRad(lng2 - lng1);
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * 
            Math.sin(dLng/2) * Math.sin(dLng/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
};

// 라디안 값으로 변환
const toRad = (value) => {
  return value * Math.PI / 180;
};

// 검색어로 장소 검색
const searchPlaces = () => {
  if (!keyword.value.trim()) {
    alert('검색어를 입력해주세요');
    return;
  }

  const places = new window.kakao.maps.services.Places();
  const options = {
    location: map.value.getCenter()
  };

  places.keywordSearch(keyword.value, (result, status) => {
    if (status === window.kakao.maps.services.Status.OK) {
      const currentLat = currentMarker.value ? currentMarker.value.getPosition().getLat() : map.value.getCenter().getLat();
      const currentLng = currentMarker.value ? currentMarker.value.getPosition().getLng() : map.value.getCenter().getLng();

      result.forEach(place => {
        place.distance = calculateDistance(
          currentLat, 
          currentLng,
          parseFloat(place.y), 
          parseFloat(place.x)
        );
      });
      const sortedResult = result.sort((a, b) => a.distance - b.distance);
      console.log('정렬된 검색 결과:', sortedResult);

      searchResults.value = sortedResult;
      displayMarkers(sortedResult);
    } else {
      console.error('검색 실패:', status);
      searchResults.value = [];
      alert('검색 결과가 없습니다.');
    }
  }, options);
};

// 검색 결과 마커 표시
const displayMarkers = (places) => {
  markers.value.forEach(marker => marker.setMap(null)); // 기존 마커 해제
  markers.value = [];
  map.value.setLevel(5);

  const defaultMarkerImage = new window.kakao.maps.MarkerImage(
    markerDefault,
    new window.kakao.maps.Size(24, 35)
  );

  places.forEach(place => {
    const marker = new window.kakao.maps.Marker({
      map: map.value,
      position: new window.kakao.maps.LatLng(place.y, place.x),
      image: defaultMarkerImage
    });

    const infowindow = new window.kakao.maps.InfoWindow({
      content: `<div style="padding:5px;font-size:12px;">${place.place_name}</div>`
    });

    window.kakao.maps.event.addListener(marker, 'mouseover', () => {
      infowindow.open(map.value, marker);
    });
    window.kakao.maps.event.addListener(marker, 'mouseout', () => {
      infowindow.close();
    });

    markers.value.push(marker);
  });
};

// 선택한 장소로 이동
const moveToPlace = (place) => {
  const moveLatLng = new window.kakao.maps.LatLng(place.y, place.x);
  map.value.setLevel(3);
  map.value.setCenter(moveLatLng);

  const defaultMarkerImage = new window.kakao.maps.MarkerImage(
    markerDefault,
    new window.kakao.maps.Size(24, 35)
  );
  
  const selectedMarkerImage = new window.kakao.maps.MarkerImage(
    markerSelected,
    new window.kakao.maps.Size(24, 35)
  );

  searchResults.value.forEach((searchPlace, index) => {
    if (searchPlace.id === place.id) {
      markers.value[index].setImage(selectedMarkerImage);
    } else {
      markers.value[index].setImage(defaultMarkerImage);
    }
  });
};
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