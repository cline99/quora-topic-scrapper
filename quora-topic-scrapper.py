####Cline Colaco
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re
from bs4 import BeautifulSoup
import csv

qna = []
def extract_ques_ans(html):
    qa_dict = {}
    soup = BeautifulSoup(html, 'html.parser')
    question_element = soup.find('div', class_='QuestionTitle___StyledText-exj38m-0 chNUqN puppeteer_test_question_title')
    question = question_element.get_text(strip=True) if question_element else None
    answer_element = soup.find('div', class_='q-box spacing_log_answer_content puppeteer_test_answer_content')
    answer = answer_element.get_text(strip=True) if answer_element else None
    qa_dict[question] = answer
    qna.append(qa_dict)

def topic_scrpper(topic):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.quora.com/topic/" + topic)

    while True:
        current_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        wait = WebDriverWait(driver, 10)
        try:
            wait.until(lambda driver: driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );") > current_height)
        except:
            break
    elements = driver.execute_script('return document.getElementsByClassName("q-text qu-truncateLines--3 qu-wordBreak--break-word");')
    for element in elements:
        driver.execute_script("arguments[0].click();", element)

    full_page_html = driver.page_source
    driver.quit()
    pattern = r'(?s)<div class="QuestionTitle___StyledText-exj38m-0 chNUqN puppeteer_test_question_title"[^>]*>.*?<div class="q-box spacing_log_answer_content puppeteer_test_answer_content"[^>]*>.*?<\/div>.*?<\/div>'
    matches = re.findall(pattern, full_page_html)
    for html in matches:
        extract_ques_ans(html)

    for d in qna:
        print('\nQuestion:', list(d.keys())[0], '\nAnswer:', list(d.values())[0])

    print(len(qna))

topic_scrpper('India')
# As this CSV writer uses UTF-8, some of the characters are showing up as gibberish in CSV, if someone knows the fix, please do
# csv_file_path = '{}.csv'.format(topic)

# all_keys = set().union(*(qna_dict.keys() for qna_dict in qna))

# with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
#     fieldnames = ['Question', 'Answer']

#     csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

#     csv_writer.writeheader()

#     for d in qna:
#         csv_writer.writerow({'Question': list(d.keys())[0], 'Answer': list(d.values())[0]})

# print(f'CSV file created at: {csv_file_path}')

