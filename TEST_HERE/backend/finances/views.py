from django.http import JsonResponse
import requests

def fetch_products(request, category):
    api_url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
    if category == 'deposits':
      api_url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
    elif category == 'savings':
      api_url = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
    
    page_no = int(request.GET.get('pageNo', 1))  # 클라이언트에서 전달된 페이지 번호 (기본값 1)
    params = {
        'auth': '00b0b3083665dc1958ea2974b49690e1',
        'topFinGrpNo': '030300',
        'pageNo': page_no
    }
    try:
        print("fetch_products 호출됨")
        response = requests.get(api_url, params=params)
        if response.status_code != 200:
            return JsonResponse({"error": f"Failed to fetch data: {response.status_code}"}, status=500)
        
        data = response.json()
        result = data.get('result', {})
        product_list = result.get('baseList', [])
        
        if not result:
            return JsonResponse({"error": "No products found or invalid response structure"}, status=500)

        # result의 메타 데이터와 product_list를 함께 반환
        response_data = {
            "products": product_list,
            "pagination": {
                "total_count": result.get("total_count", 0),
                "max_page_no": result.get("max_page_no", 1),
                "now_page_no": result.get("now_page_no", 1),
            }
        }
        print('response데이터는 이거입니다 : ',response_data['pagination'])
        return JsonResponse(response_data, safe=False)
    except Exception as e:
        print(f"Error fetching products: {e}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)
