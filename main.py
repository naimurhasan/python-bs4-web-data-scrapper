import requests
import io
from bs4 import BeautifulSoup
from openpyxl import Workbook


BASE_URL = 'https://smarttayari.com/sample/578'
FILE_NAME = 'page.html'

def downloadPage():
    r = requests.get(BASE_URL)
    if r.status_code == 200:
        with io.open(FILE_NAME, 'w',encoding='utf8') as f:
            f.write(r.content.decode())
        print('FILE SAVED')
    else:
        print('request failed with status code: '+str(r.status_code))

def getQuestions():
    with io.open(FILE_NAME, 'r',encoding='utf8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    quiz_elems = soup.find_all(class_='quiz-block')
    questions = []
    for elem in quiz_elems:
        question = {}
        question['q'] = elem.find('h3').text
        
        option_elems = elem.find('ol').find_all('li')
        question['option_1'] = option_elems[0].text
        question['option_2'] = option_elems[1].text
        question['option_3'] = option_elems[2].text
        question['option_4'] = option_elems[3].text
        question['answer'] = elem['data-correct']
        questions.append(question)
    return questions

def saveExcel():
    questions = getQuestions()
    wb = Workbook()
    ws = wb.active

    ws.append(['Question', 'Option1', 'Option2', 'Option3', 'Option4', 'Answer'])
    for q in questions:
        ws.append([q['q'], q['option_1'], q['option_2'], q['option_3'], q['option_4'], q['answer']])
    wb.save("questoins.xlsx")

def main():
    saveExcel()

if __name__ == '__main__':
    main()