from googletrans import Translator
if __name__ == '__main__':
    translator = Translator()
    f_en = open(r'C:\Users\osnat\botzi\file_for_translate.txt', 'r')
    data = f_en.read()
    result = translator.translate(data, src='en', dest='he').text
    f_eb = open(r'C:\Users\osnat\botzi\file_translate_to_hebrew.txt', 'w')
    f_eb.write(result)
   #print(result)