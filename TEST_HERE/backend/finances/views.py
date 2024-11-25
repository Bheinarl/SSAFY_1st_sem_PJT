from django.http import JsonResponse
import requests
from .models import DepositProduct, SavingProduct, FundProduct

def fetch_and_save_funds_products(request): 
    print('fetch_and_save_funds_products')

    categories = ['채권형', '단기금융', '혼합채권형', '혼합자산', '변액보험', '혼합주식형', '주식형', '파생상품', '부동산', '특별자산', '재간접']

    # 기존 데이터 확인
    existing_data_count = FundProduct.objects.count()
    if existing_data_count > 0:
        return JsonResponse({
            "message": "Data already exists. Fetching skipped.",
            "existing_count": existing_data_count
        }, status=200)

    # API 호출 및 데이터 저장
    for category in categories:
        base_api_url = 'https://apis.data.go.kr/1160100/service/GetFundProductInfoService/getStandardCodeInfo?serviceKey=Z0etJ6Sv%2BIOfdba2SlwmsGsJfrut7XaOO50AMFe%2BMwH2ksB8ID5EZMniJwBYBTzUPpEJw87qpDY%2B54CHiw7R%2Fw%3D%3D&resultType=json&pageNo=1&numOfRows=50&fndTp='
        base_api_url += category
        try:
            response = requests.get(base_api_url)
            response.raise_for_status()  # 요청 실패 시 예외 발생

            if response.text.strip() == "":
                raise ValueError("Empty response")
            
            data = response.json()
            
            # API 응답에서 데이터 추출
            items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
            
            for item in items:
                # FundProduct 모델에 데이터 저장
                FundProduct.objects.create(
                    fndTp=item.get('fndTp', ''),  # 펀드 유형
                    asoStdCd=item.get('asoStdCd', ''),  # 상품 분류 코드
                    fndNm=item.get('fndNm', '')  # 펀드 명
                )

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for category {category}: {e}")
            return JsonResponse({
                "message": "Error fetching data.",
                "error": str(e)
            }, status=500)
        except ValueError as e:
            print(f"Error fetching data for category {category}: {e}")
            return JsonResponse({
                "message": "Error fetching data.",
                "error": str(e)
            }, status=500)

    return JsonResponse({
        "message": "Data fetched and saved successfully.",
        "fetched_categories": len(categories),
    }, status=201)

def get_filtered_funds_products(request, subcategory):
    try:
        if subcategory == '전체':
            products = FundProduct.objects.all()
        else:
            products = FundProduct.objects.filter(fndTp=subcategory)

        response_data = {
            "products": list(products.values('fndNm', 'fndTp', 'asoStdCd')),
        }
        return JsonResponse(response_data, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def fetch_and_save_deposit_savings_products(request, category):
    print('fetch_and_save_deposit_savings_products')
    # 기본 API URL 설정
    api_url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
    if category == 'deposits':
        api_url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
    elif category == 'savings':
        api_url = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
    else:
        return JsonResponse({"error": "Invalid category"}, status=400)
    
    # 모델 선택
    model = DepositProduct if category == 'deposits' else SavingProduct

    # 데이터가 이미 존재하는지 확인
    existing_data_count = model.objects.count()
    if existing_data_count > 0:
        return JsonResponse({
            "message": "Data already exists. Fetching skipped.",
            "existing_count": existing_data_count
        }, status=200)

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


def get_filtered_deposit_savings_products(request, category):

    # 해당 category에 맞는 데이터 가져오기
    if category == 'deposits':
        products = DepositProduct.objects.all()
    elif category == 'savings':
        products = SavingProduct.objects.all()
    else:
        return JsonResponse({"error": "Invalid category"}, status=400)

    # 반환할 데이터 구성
    response_data = {
        "products": list(products.values('fin_prdt_nm', 'kor_co_nm', 'join_member', 'mtrt_int', 'join_way')),
    }
    return JsonResponse(response_data)

