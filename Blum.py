import requests
from datetime import datetime, timedelta
import json
import time
import random
import sys
import os
from colorama import Fore, Style, init

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def art():
    print("\033[1;91m" + r"""
                           _   
                          | |  
  ___ _ __ ___   __ _ _ __| |_ 
 / __| '_ ` _ \ / _` | '__| __|
 \__ | | | | | | (_| | |  | |_ 
 |___|_| |_| |_|\__,_|_|   \__|
                               
                               

 """ + "\033[0m" + "\033[1;92m" + r"""""" + "\033[0m" + "\033[1;92m" + r"""
  _______          _ 
 |__   __|        | |
    | | ___   ___ | |
    | |/ _ \ / _ \| |
    | | (_) | (_) | |
    |_|\___/ \___/|_|
                     
                     
                     """ + "\033[0m\n\033[1;96m---------------------------------------\033[0m\n\033[1;93mScript created by: smArt tOol hAniF\033[0m\n\033[1;92mJoin Telegram: \nhttps://t.me/smartoolhanif \033[0m\n\033[1;91mVisit my GitHub: \nhttps://github.com/smartoolhanif\033[0m\n\033[1;96m---------------------------------------\033[0m\n\033[1;38;2;139;69;19;48;2;173;216;230m--------------[Blum Bot]--------------\033[0m\n\033[1;96m---------------------------------------\033[0m")

def get_query_ids_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            query_ids = [line.strip() for line in file.readlines()]
            return query_ids
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def save_token(token, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(token)
    except Exception as e:
        print(f"Error saving token: {e}")

def get_token_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            token = file.readline().strip()
            return token
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_new_token(query_id):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://telegram.blum.codes",
        "priority": "u=1, i",
        "referer": "https://telegram.blum.codes/"
    }

    data = json.dumps({"query": query_id})
    url = "https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"

    animation = ["|", "/", "-", "\\"]

    while True:  # Loop indefinitely
        try:
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 200:
                try:
                    response_json = response.json()
                    token = response_json.get('token', {}).get('refresh', None)
                    if token:
                        return token
                    else:
                        print("Token key not found in response.")
                except json.JSONDecodeError as e:
                    print(f"JSON Decode Error: {e}")
                    print(f"Response content: {response.text}")
            elif response.status_code == 520:
                for i in range(len(animation)):  # Loop through animation frames
                    sys.stdout.write(f"\rWait Token Fetched {animation[i]}")
                    sys.stdout.flush()
                    time.sleep(0.5)
                sys.stdout.write("\r" + " " * 20 + "\r")  # Clear line
            else:
                print(f"Unexpected status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            clear_terminal()
            art()
            print(f"{Fore.RED + Style.BRIGHT}Network Problem")

        time.sleep(5)
        clear_terminal()
        art()

def get_headers(token):
    return {
      "accept": "application/json, text/plain, */*",
      "accept-language": "en-US,en;q=0.9",
      "authorization": f"Bearer {token}",
      "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
      "sec-ch-ua-mobile": "?1",
      "sec-ch-ua-platform": "\"Android\"",
      "sec-fetch-dest": "empty",
      "sec-fetch-mode": "cors",
      "sec-fetch-site": "same-site"
      
    }

def fetch_data(url, headers, retry=3):
    for attempt in range(retry):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt < retry - 1:
                time.sleep(2 ** attempt)
            else:
                raise


def get_balance(token, account_no):
    url = "https://game-domain.blum.codes/api/v1/user/balance"
    headers = get_headers(token)
    
    try:
        data_balance = fetch_data(url, headers)
        available_balance = data_balance.get("availableBalance", "N/A")
        play_passes = data_balance.get("playPasses", "N/A")
        is_fast_farming_enabled = data_balance.get("isFastFarmingEnabled", False)

        print(f"{Fore.CYAN + Style.BRIGHT}------Account No.{account_no}------")
        print(f"{Fore.GREEN + Style.BRIGHT}Balance: {available_balance}")
        print(f"{Fore.YELLOW + Style.BRIGHT}Total Play Pass: {play_passes}")

        if not is_fast_farming_enabled:
            print(f"{Fore.RED + Style.BRIGHT}Farming not started")

        return data_balance

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def claim_farming(token):
    url = "https://game-domain.blum.codes/api/v1/farming/claim"
    headers = get_headers(token)    
    try:
        sys.stdout.write("Claiming farming balance...")
        sys.stdout.flush()
        response = requests.post(url, headers=headers)
        sys.stdout.write('\r' + ' ' * len("Claiming farming balance..."))
        sys.stdout.write('\r')
        data = response.json()
       
        if response.status_code == 425 and data.get("message") == "It's too early to claim":
            print(f"{Fore.RED+ Style.BRIGHT}Farming Already Claimed")
        elif response.status_code == 200:
            print(f"{Fore.GREEN+ Style.BRIGHT}Farming Claimed Successfully")
        else:
            print(f"{Fore.RED+ Style.BRIGHT}Unexpected status code: {response.status_code}")
            print(f"{Fore.RED+ Style.BRIGHT}Response text: {response.text}")
            
    except requests.exceptions.RequestException as req_err:
        print(f"{Fore.RED+ Style.BRIGHT}Request error occurred: {req_err}")

def start_farming(token):
    url_farming = "https://game-domain.blum.codes/api/v1/farming/start"
    url_balance = "https://game-domain.blum.codes/api/v1/user/balance"
    headers = get_headers(token)
    
    while True:
        try:
            sys.stdout.write("Starting farming...")
            sys.stdout.flush()
            sys.stdout.write('\r' + ' ' * len("Starting farming..."))
            sys.stdout.write('\r')

            response1 = requests.post(url_farming, headers=headers)
            response1.raise_for_status()
            
            if response1.status_code == 200:
                data1 = response1.json()
                farming_balance = data1.get("balance", "N/A")
                end_time = data1.get("endTime", None)

                end_time_dt = datetime.fromtimestamp(end_time / 1000.0)
                now = datetime.now()
                remaining_time = end_time_dt - now
                hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                time_str = f"{int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"
                
                if farming_balance == "0":
                    print("Farming Started Successfully")
                    while True:
                        try:
                            response2 = requests.get(url_balance, headers=headers)
                            response2.raise_for_status()
                            
                            if response2.status_code == 200:
                                data2 = response2.json()
                                new_balance = data2.get("availableBalance", "N/A")
                                print(f"{Fore.GREEN + Style.BRIGHT}New Balance: {new_balance}")
                                return end_time
                            else:
                                print(f"{Fore.RED + Style.BRIGHT}Unexpected status code from balance request: {response2.status_code}")
                                print(f"{Fore.RED + Style.BRIGHT}Response text: {response2.text}")
                                time.sleep(5)
                        except requests.exceptions.RequestException as e:
                            time.sleep(5)
                else:
                    print(f"{Fore.MAGENTA + Style.BRIGHT}Farming Balance: {farming_balance}")
                    print(f"{Fore.CYAN + Style.BRIGHT}Time Until End: {time_str}")
                    return end_time
            
            else:
                print(f"{Fore.RED + Style.BRIGHT}Unexpected status code: {response1.status_code}")
                print(f"{Fore.RED + Style.BRIGHT}Response text: {response1.text}")
                time.sleep(5)

        except requests.exceptions.RequestException as e:
            time.sleep(5)

def get_daily_reward(token):
    url = "https://game-domain.blum.codes/api/v1/daily-reward"
    headers = get_headers(token)
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        
        if response.status_code == 200:
            print(f"{Fore.GREEN + Style.BRIGHT}Daily Reward Claimed Successfully{Style.RESET_ALL}")
            return  # Exit the function on success
        
        elif response.status_code == 400:
            print(f"{Fore.RED + Style.BRIGHT}Daily Reward Already Claimed{Style.RESET_ALL}")
            return  # Exit the function if the reward has already been claimed
        
        else:
            print(f"{Fore.RED + Style.BRIGHT}Response Status Code: {response.status_code}{Style.RESET_ALL}")
    
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED + Style.BRIGHT}Daily Reward Already Claimed{Style.RESET_ALL}")

def claim_ref(token):
    url = "https://user-domain.blum.codes/api/v1/friends/claim"
    headers = get_headers(token)
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        
        if response.status_code == 200:
            data = response.json()
            ref_balance = data.get("claimBalance", "N/A")  # Default to "N/A" if not found
            print(f"{Fore.GREEN + Style.BRIGHT}Referral Bonus Claimed Successfully{Style.RESET_ALL}")
            print(f"{Fore.GREEN + Style.BRIGHT}Referral Bonus: {ref_balance}{Style.RESET_ALL}")
            return  # Exit the function on success
        
        elif response.status_code == 400:
            print(f"{Fore.RED + Style.BRIGHT}Referral Bonus Already Claimed{Style.RESET_ALL}")
            return  # Exit the function if the bonus has already been claimed
        
        else:
            print(f"{Fore.RED + Style.BRIGHT}Response Status Code: {response.status_code}{Style.RESET_ALL}")
    
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED + Style.BRIGHT}Referral Bonus Already Claimed{Style.RESET_ALL}")

    # Uncomment if you want to retry after a failure
    # time.sleep(5)

def new_balance(token):
    url = "https://game-domain.blum.codes/api/v1/user/balance"
    headers = get_headers(token)
    
    while True:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Check for HTTP errors
            
            if response.status_code == 200:
                data_balance = response.json()
                new_balance = data_balance.get("availableBalance", "N/A")
                play_passes = data_balance.get("playPasses", 0)  # Default to 0 if not found
                return new_balance, play_passes
            
            else:
                print(f"{Fore.RED + Style.BRIGHT}Unexpected status code: {response.status_code}")
                print(f"{Fore.RED + Style.BRIGHT}Response text: {response.text}")
                
                time.sleep(5)

        except requests.exceptions.RequestException as e:
            time.sleep(5)

def play_game(token):
    url = "https://game-domain.blum.codes/api/v1/game/play"
    headers = get_headers(token)
    
    while True:
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()
            gameid = data.get("gameId")

            if gameid:
                print(f"{Fore.YELLOW + Style.BRIGHT}Game Started....")
                time.sleep(32)
                return gameid
            else:
                print("Game ID not found in the response.")
                return None
        except requests.exceptions.RequestException as e:
            time.sleep(5)  # Wait before retrying

def claim_game(token, gameId):
    url = "https://game-domain.blum.codes/api/v1/game/claim"
    headers = get_headers(token)
    points = random.randint(256, 278)
    body = {"gameId": gameId, "points": points}

    while True:
        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()  # Check for HTTP errors
            
            if response.status_code == 200:
                print(f"{Fore.GREEN + Style.BRIGHT}Game Reward Claimed Successfully")
                break  # Exit loop on successful claim
            else:
                print(f"{Fore.RED + Style.BRIGHT}Unexpected status code: {response.status_code}")
                print(f"{Fore.RED + Style.BRIGHT}Response text: {response.text}")
                # Optionally, add a delay before retrying
                time.sleep(5)  # Wait for 5 seconds before retrying

        except requests.exceptions.RequestException as e:
            time.sleep(5)  # Wait for 5 seconds before retrying

def tribe(token):
    tribe_check_url = "https://tribe-domain.blum.codes/api/v1/tribe/my"
    tribe_leave_url = "https://tribe-domain.blum.codes/api/v1/tribe/leave"
    tribe_join_url = "https://tribe-domain.blum.codes/api/v1/tribe/e0020ec3-f007-4116-8ff2-6b60913a44f7/join"
    headers = get_headers(token)    
    try:
        response_my = requests.get(tribe_check_url, headers=headers)

        while response_my.status_code == 424:
            response_my = requests.get(tribe_check_url, headers=headers)
        
        data_1 = response_my.json()
        tribe_id = data_1.get("id")
        name = data_1.get("title")
        member = data_1.get("countMembers")
        
        if tribe_id == "e0020ec3-f007-4116-8ff2-6b60913a44f7":
            print(f"{Fore.CYAN + Style.BRIGHT}Tribe: {name} | {Fore.MAGENTA + Style.BRIGHT}Tribe Member: {member}")
        elif tribe_id != "e0020ec3-f007-4116-8ff2-6b60913a44f7":
            response_leave = requests.post(tribe_leave_url, headers=headers, json={})
            response_join = requests.post(tribe_join_url, headers=headers)
            
            response_my = requests.get(tribe_check_url, headers=headers)
            while response_my.status_code == 424:
                response_my = requests.get(tribe_check_url, headers=headers)
            
            data_1 = response_my.json()
            name = data_1.get("title")
            member = data_1.get("countMembers")
            print(f"{Fore.CYAN + Style.BRIGHT}Tribe: {name} | {Fore.MAGENTA + Style.BRIGHT}Tribe Member: {member}")
  
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        response_join = requests.post(tribe_join_url, headers=headers)
        
        response_my = requests.get(tribe_check_url, headers=headers)
        while response_my.status_code == 424:
            response_my = requests.get(tribe_check_url, headers=headers)
        
        data_1 = response_my.json()
        name = data_1.get("title")
        member = data_1.get("countMembers")
        print(f"{Fore.CYAN + Style.BRIGHT}Tribe: {name} | {Fore.MAGENTA + Style.BRIGHT}Tribe Member: {member}")


def task(token):
    url_task_list = "https://earn-domain.blum.codes/api/v1/tasks"
    url_task_start = "https://earn-domain.blum.codes/api/v1/tasks/{ids}/start"
    url_task_claim = "https://earn-domain.blum.codes/api/v1/tasks/{ids}/claim"
    headers = get_headers(token)
    try:
        response = requests.get(url_task_list, headers=headers)
        response.raise_for_status()
        data = response.json()
        ids = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    for section in item.get('subSections', []):
                        if isinstance(section, dict):
                            for task in section.get('tasks', []):
                                if isinstance(task, dict):
                                    ids.append(task.get('id'))
        
        for task_id in ids:
            start_url = url_task_start.format(ids=task_id)
            claim_url = url_task_claim.format(ids=task_id)

            start_response = requests.post(start_url, headers=headers)
            data_start = start_response.json()
            title = data_start.get("title")
            if start_response.status_code == 200:
                print(f"{Fore.CYAN + Style.BRIGHT}Task Claiming: {title}")
                time.sleep(5)
                claim_response = requests.post(claim_url, headers=headers)
                data_claim = claim_response.json()
                reward = data_claim.get("reward")
                title_2 = data_start.get("title")
                if claim_response.status_code == 200:
                    print(f"{Fore.GREEN + Style.BRIGHT}Task Complete")
                    print(f"{Fore.CYAN + Style.BRIGHT}Task Reward: {Fore.WHITE + Style.BRIGHT}{reward}")
                elif claim_response.status_code == 400:
                    print(f"{Fore.YELLOW + Style.BRIGHT}Task Already Completed")
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Response: {claim_response.json()}")
            
            elif start_response.status_code == 400:
                print(f"{Fore.RED + Style.BRIGHT}Task Already Completed")
            else:
                print(f"{Fore.RED + Style.BRIGHT}Response: {start_response.json()}")
            
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED + Style.BRIGHT}Server Problem")

def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}:{minutes}:{seconds}"

def countdown_timer(seconds):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        print(f"{Fore.CYAN + Style.BRIGHT}Wait {hours:02}:{mins:02}:{secs:02}", end='\r')
        time.sleep(1)
        seconds -= 1
    print("Wait 00:00:00          ", end='\r')

def main():
    clear_terminal()
    art()
    remaining_times = []    
    user_input = input(f"{Fore.WHITE + Style.BRIGHT}Do you want to Complete Tasks? (y/n): ").strip().lower()   
    run_task = user_input == 'y'    
    if run_task or user_input == 'n':
    	
        while True:
            query_ids = get_query_ids_from_file('data.txt')
            clear_terminal()
            art()

            for index, query_id in enumerate(query_ids):
                if query_id:
                    if index > 0:
                        countdown_timer(5)
                        
                    token = get_new_token(query_id)
                    if token:
                        token_file = 'token.txt'
                        save_token(token, token_file)
                        get_balance(token, index + 1)
                        tribe(token)
                        claim_farming(token)
                        farming_end_time = start_farming(token)
                        if farming_end_time:
                        	remaining_time = farming_end_time
                        	remaining_times.append(remaining_time)
                        claim_ref(token)
                        
                        if run_task:
                            task(token)
                        
                        while True:
                            current_balance, play_passes = new_balance(token)
                            if current_balance is None or play_passes is None:
                                print(f"{Fore.RED + Style.BRIGHT}Failed to retrieve balance or play passes.")
                                break
                            
                            if play_passes > 0:
                                print(f"{Fore.CYAN + Style.BRIGHT}Play Passes Available: {play_passes}")
                                game_id = play_game(token)
                                if game_id:
                                    claim_game(token, game_id)
                            else:
                                print(f"{Fore.RED + Style.BRIGHT}Play Pass is 0")
                                break
                        
                        get_daily_reward(token)
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}Account No.{index + 1}: Token generation failed.")
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Account No.{index + 1}: Query ID not found.")
            
            if remaining_times:
                shortest_time = min(remaining_times)
                now = time.time() * 1000
                diffe = shortest_time - now
                seco = int(diffe / 1000)
                print(seco)
                countdown_timer(seco + 2)
                clear_terminal()
                art()
    
    elif user_input == 'n':
        print("Task function will not be run.")
    
    else:
        print("Invalid input. Please enter 'y' or 'n'.")

if __name__ == "__main__":
    main()
