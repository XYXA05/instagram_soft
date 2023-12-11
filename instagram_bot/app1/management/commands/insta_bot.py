import random
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from django.core.management.base import BaseCommand
from app1.models import Instagram_acaunts, acaunts_for_get, Potoci
from app1.choice_answer import model_map
from asgiref.sync import sync_to_async
from selenium.webdriver.chrome.options import Options


class Command(BaseCommand):
    help = 'bot'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_locks = {}

    @sync_to_async
    def update_user_message_in__acaunts_for_get(self, mail):
        user_instance = Instagram_acaunts.objects.get(mail=mail)
        user_instance.enter_count += 1  # Increment the message count
        user_instance.save()  # Save the updated instance


    @sync_to_async
    def update_user(self, acaunts_href):
        try:
            user_instance = acaunts_for_get.objects.get(acaunts_href=acaunts_href)
            user_instance.used = 'use'  # Update the 'used' field to 'use'
            user_instance.save()  # Save the updated instance
        except acaunts_for_get.DoesNotExist:
            print(f"User with acaunts_href {acaunts_href} does not exist.")
        except Exception as e:
            print(f"Error updating user: {e}")

    @sync_to_async
    def update_user_massage(self, acaunts_href):
        try:
            user_instance = acaunts_for_get.objects.get(acaunts_href=acaunts_href)
            user_instance.send_massage_point = 'send_massage'  # Update the 'used' field to 'use'
            user_instance.save()  # Save the updated instance
        except acaunts_for_get.DoesNotExist:
            print(f"User with acaunts_href {acaunts_href} does not exist.")
        except Exception as e:
            print(f"Error updating user: {e}")

    async def create_link_acaunt(self, **kwargs):
        try:
            await sync_to_async(acaunts_for_get.objects.get_or_create)(**kwargs)
        except Exception as e:
            print(f"Error creating user: {e}")

    def is_user_being_messaged(self, users):
        return users in self.user_locks

    @sync_to_async
    def get_message_count(self, mail):
        user_instance = Instagram_acaunts.objects.get(mail=mail)
        return user_instance.enter_count
    
    async def send_message(self, browser, users, step_choice, text, mail):
        try:
            # Check if the user is already being messaged by another account
            if not self.is_user_being_messaged(users):
                self.user_locks[users] = True  # Lock the user to prevent other accounts from messaging simultaneously
                await asyncio.sleep(15)
                browser.get(f'https://www.instagram.com/{users}/')
                await asyncio.sleep(15)

                button_message = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div')
                button_message.click()
                
                message_count = await self.get_message_count(mail)
                if int(message_count) < 5:
                    await asyncio.sleep(15)
                    message_input = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/p')
                    message_input.clear()
                    await asyncio.sleep(25)
                    model_class = model_map[step_choice]
                    if step_choice == "text_with_gpt" or step_choice == "text":
                        messages = model_class(text)
                        await asyncio.sleep(10)
                        message = messages.get_response()
                        await asyncio.sleep(15)
                        message_input.send_keys(message)
                        await asyncio.sleep(25)
                        
                        message_input.send_keys(Keys.ENTER)
                        await self.update_user_message_in__acaunts_for_get(mail)
                        await self.update_user_massage(users)
                        await self.update_user(users)
                        await asyncio.sleep(20)

                    del self.user_locks[users]  # Unlock the user after sending the message
                else:
                    print('send 6 maasage for accaunt')
                    browser.quit()
            else:
                print(f"User {users} is already being messaged by another account.")

        except NoSuchElementException:
            await self.update_user(users)
            print(f"Element not found for profile: {users}")


    async def logon(self, gamail, password, acaunts_for_gets, users_list, step_choice, text, mail):
        #chrome_options = Options()
        #chrome_options.add_argument("--headless") 
        #browser = webdriver.Chrome(options=chrome_options)
        browser = webdriver.Chrome()

        try:
            browser.get('https://www.instagram.com/')
            await asyncio.sleep(random.randrange(3, 6))

            username_input = browser.find_element(By.NAME, 'username')
            username_input.clear()
            username_input.send_keys(gamail)

            await asyncio.sleep(3)

            password_input = browser.find_element(By.NAME, 'password')
            password_input.clear()
            password_input.send_keys(password)

            password_input.send_keys(Keys.ENTER)

            await asyncio.sleep(10)

            browser.get(f'{acaunts_for_gets}')
            await asyncio.sleep(10)

            followers_list = browser.find_element(By.XPATH, "//html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]")

            for _ in range(1):  # You can adjust the number of times you want to scroll
                browser.execute_script("arguments[0].scrollBy(0, 1000);", followers_list)
                await asyncio.sleep(2)

            hrefs = list(set(map(lambda x: x.text, browser.find_elements(By.CLASS_NAME, 'xt0psk2'))))

            for link in hrefs:
                await self.create_link_acaunt(acaunts_href=link)

            for users in users_list:
                await self.send_message(browser, users, step_choice, text, mail)

        finally:
            browser.quit()

    def handle(self, *args, **options):
        acaunt = Instagram_acaunts.objects.all()
        loop = asyncio.get_event_loop()
        tasks = []

        for acaunts in acaunt:
            gamail = acaunts.mail
            password = acaunts.password
            mail = acaunts.mail
            acaunts_for_gets = acaunts.instagram_acaunts_for_get
            potoci = Potoci.objects.filter(acaunts__id=acaunts.id)
            userss = acaunts_for_get.objects.filter(used='not use')
            user_list = [users.acaunts_href for users in userss]

            for potoc in potoci:
                step_choice = potoc.chice_answer
                text = potoc.promt
                task = loop.create_task(self.logon(gamail, password, acaunts_for_gets, user_list, step_choice, text, mail))
                tasks.append(task)

        loop.run_until_complete(asyncio.wait(tasks))


                        