import requests,re
import random

def send(cc, last, username, time_taken):
    cc = cc.strip()
    numbers = re.findall(r"\d+", cc)
    n = mm = yy = cvc = ""
    if len(numbers) >= 4:
        n = numbers[0]
        mm = numbers[1]
        yy = numbers[2]
        cvc = numbers[3]
        #mm = str(int(mm))
        if len(yy) == 4:
            yy = yy[-2:]
        cc_formatted = f"{n}|{mm}|{yy}|{cvc}"
        ii = n[:6]
    else:
        cc_formatted = cc
        ii = cc[:6]

    random_amount1 = random.randint(1, 4)
    random_amount2 = random.randint(1, 99)

    try:
        response = requests.get(f'https://bins.antipublic.cc/bins/{ii}')
        data = response.json()

        if response.status_code == 200:
            bank = data.get("bank", "Unknown")
            emj = data.get("country_flag", "🏳️")
            do = data.get("country", "Unknown")
            dicr = data.get("brand", "Unknown")
            typ = data.get("type", "Unknown")
        else:
            print(f"API Error: {data.get('error', 'Unknown error')}")
            bank = emj = do = dicr = typ = 'Unknown'
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        bank = emj = do = dicr = typ = 'Unknown'

    msg1 = f"""
𝗚𝗔𝗧𝗘𝗪𝗔𝗬 ➜ Light Yagami 🍎

<b>RESPONSE ➜</b> {last} 
𝗖𝗖 ➜ <code>{cc_formatted}</code>       
𝗕𝗜𝗡 ➜ {ii}                   
𝗖𝗢𝗨𝗡𝗧𝗥𝗬 ➜ {do}               
𝗕𝗔𝗡𝗞 ➜ {bank}                
𝗙𝗟𝗔𝗚 ➜ {emj}                 

Check by @{username}
𝗕𝗼𝘁 𝗯𝘆: @strawhatchannel69
"""
    return msg1
