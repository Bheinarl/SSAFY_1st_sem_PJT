from django.http import JsonResponse
import requests
from .models import DepositProduct, SavingProduct

def fetch_products(request, category):
    # 기본 API URL 설정
    api_url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
    if category == 'deposits':
        api_url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
    elif category == 'savings':
        api_url = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
    else:
        return JsonResponse({"error": "Invalid category"}, status=400)
    
    # 페이지 번호와 기본 파라미터 처리
    params = {
        'auth': '00b0b3083665dc1958ea2974b49690e1',
        'pageNo': 1,  # 첫 페이지부터 시작
    }

    topFinGrpNo_list = ['020000', '030200', '030300', '050000', '060000']
    all_product_list = []  # 전체 상품 리스트를 저장할 리스트

    try:
        # 각 topFinGrpNo에 대해 반복적으로 데이터 처리
        for topFinGrpNo in topFinGrpNo_list:
            params['topFinGrpNo'] = topFinGrpNo
            print(f"Processing topFinGrpNo: {topFinGrpNo}")

            # 첫 페이지 데이터 처리
            response = requests.get(api_url, params=params)
            if response.status_code != 200:
                return JsonResponse({"error": f"Failed to fetch data: {response.status_code}"}, status=500)
            
            data = response.json()
            result = data.get('result', {})
            product_list = result.get('baseList', [])
            
            if not result:
                return JsonResponse({"error": "No products found or invalid response structure"}, status=500)

            # 전체 페이지 순회하여 모든 데이터를 저장
            total_count = result.get("total_count", 0)
            max_page_no = result.get("max_page_no", 1)

            # 각 페이지를 순차적으로 처리
            for page_no in range(1, max_page_no + 1):
                params['pageNo'] = page_no
                response = requests.get(api_url, params=params)

                if response.status_code != 200:
                    return JsonResponse({"error": f"Failed to fetch data on page {page_no}: {response.status_code}"}, status=500)

                data = response.json()
                result = data.get('result', {})
                product_list = result.get('baseList', [])

                # 상품 데이터 저장
                for product in product_list:
                    if category == 'deposits':
                        DepositProduct.objects.update_or_create(
                            fin_prdt_cd=product.get('fin_prdt_cd'),
                            defaults={
                                'fin_prdt_nm': product.get('fin_prdt_nm'),
                                'kor_co_nm': product.get('kor_co_nm'),
                                'fin_co_no': product.get('fin_co_no'),
                                'join_way': product.get('join_way'),
                                'max_limit': product.get('max_limit', 0.00),
                                'mtrt_int': product.get('mtrt_int'),
                                'join_member': product.get('join_member', ''),
                                'etc_note': product.get('etc_note', '')
                            }
                        )
                    elif category == 'savings':
                        SavingProduct.objects.update_or_create(
                            fin_prdt_cd=product.get('fin_prdt_cd'),
                            defaults={
                                'fin_prdt_nm': product.get('fin_prdt_nm'),
                                'kor_co_nm': product.get('kor_co_nm'),
                                'fin_co_no': product.get('fin_co_no'),
                                'join_way': product.get('join_way'),
                                'max_limit': product.get('max_limit', 0.00),
                                'mtrt_int': product.get('mtrt_int'),
                                'join_member': product.get('join_member', ''),
                                'etc_note': product.get('etc_note', '')
                            }
                        )
                
                # 누적된 product_list를 전체 리스트에 추가
                all_product_list.extend(product_list)
        
        # 반환 데이터 구성
        response_data = {
            "products": all_product_list,  # 모든 상품 리스트 반환
            "pagination": {
                "total_count": total_count,
                "max_page_no": max_page_no,
                "now_page_no": 1,  # 첫 페이지로 설정
            }
        }
        print('response 데이터:', response_data['pagination'])
        return JsonResponse(response_data, safe=False)
    
    except Exception as e:
        print(f"Error fetching products: {e}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)
