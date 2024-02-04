####Cline Colaco
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re
from bs4 import BeautifulSoup
import csv

qna = []
threshold_views = 10
threshold_shares = 5
def extract_ques_ans(html):
    qa_dict = {}
    soup = BeautifulSoup(html, 'html.parser')
    views_element = soup.find('div', class_='q-flex qu-justifyContent--space-between AnswerFooter___StyledFlex-sc-2xbo88-0 kcDxwV')
    views = views_element.get_text(strip=True)[0:views_element.get_text(strip=True).index('view') - 1] if views_element else None
    shares_element = soup.find_all('div', class_='q-click-wrapper qu-display--inline-block qu-tapHighlight--white qu-cursor--pointer qu-hover--textDecoration--underline ClickWrapper___StyledClickWrapperBox-zoqi4f-0 iyYUZT')
    shares = shares_element[1].get_text(strip=True) if shares_element else None
    s_pattern = r"View (\d+([KMkMm])?) shares"
    match = re.match(s_pattern, shares)
    if match:
        raw_number_with_suffix = match.group(1)
        suffix = match.group(2).upper() if match.group(2) else ''
        match_numeric = re.match(r"(\d+)", raw_number_with_suffix)
        raw_number = match_numeric.group(1) if match_numeric else ''
        if raw_number:
            if suffix == 'K':
                number_of_shares = int(raw_number) * 1000
            elif suffix == 'M':
                number_of_shares = int(raw_number) * 1000000
            else:
                number_of_shares = int(raw_number)
    else:
        number_of_shares = 0

    t_views = views
    t_views = float(views[0:len(views) - 1]) * 1000 if views[-1].upper() in ('K') else t_views
    t_views = float(views[0:len(views) - 1]) * 100000 if views[-1].upper() in ('M') else t_views
    t_views = float(views[0:len(views) - 1]) * 100000000 if views[-1].upper() in ('B') else t_views

    if not(int(t_views) >= threshold_views and int(number_of_shares) >= threshold_shares):
        pass
    else:
        question_element = soup.find('div', class_='QuestionTitle___StyledText-exj38m-0 chNUqN puppeteer_test_question_title')
        question = question_element.get_text(strip=True) if question_element else None
        answer_element = soup.find('div', class_='q-box spacing_log_answer_content puppeteer_test_answer_content')
        answer = answer_element.get_text(strip=True) if answer_element else None
        qa_dict[question] = '-->' + answer
        qna.append(qa_dict)
        print(number_of_shares, int(t_views), question)


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
    pattern = r'(?s)<div class="QuestionTitle___StyledText-exj38m-0 chNUqN puppeteer_test_question_title"[^>]*>.*?<div class="q-flex qu-mb--small qu-alignItems--center qu-justifyContent--space-between qu-zIndex--base styles___StyledFlex-c0eo4-0 gNbQFP"[^>]*>.*?<\/div>.*?<\/div>'
    matches = re.findall(pattern, full_page_html)

#--------------Driver Code
    for html in matches:
        extract_ques_ans(html)

    for d in qna:
        print('\nQuestion:', list(d.keys())[0], '\nAnswer:', list(d.values())[0])

    print(len(qna))

topic_scrpper('Autism')




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

