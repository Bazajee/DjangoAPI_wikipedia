from django.core.mail import send_mail

import re
from bs4 import BeautifulSoup
import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR as HTTP_500



@api_view(['GET'])
def wikipedia_based (request, title):
    """
    The title argument must correspond to an existing Wikipedia page (Note: only English Wikipedia is supported).
    The function retrieves a summary from a Wikipedia page. 
    If over 20% of the words in the summary are long, the backend sends an email.
    The function returns a JSON object containing the following fields:
        title: The title of the Wikipedia page.
        percent_long_words: The percentage of long words in the summary.
        summary: The summary of the Wikipedia page.
        long_words: A list of long words found in the summary.
    """
    try:
        try: 
            url = f'https://en.wikipedia.org/w/api.php?action=parse&page={title}&format=json&prop=text&section=0'
            response = requests.get(url)
        except Exception:
            return Response("Error from wikipedia API:", status=HTTP_500)
            
        # Parse data
        json_data = response.json()
        summary_raw_text = json_data['parse']['text']['*']
        soup = BeautifulSoup(summary_raw_text, "html.parser")
        summary_text = "".join(tag.text.strip() for tag in soup.find_all(['p']))
        word_list = list(
            filter(bool, re.sub(r"[^a-zA-Z]", " ", summary_text).split(' '))
        )
        
        # Calculate long word count
        long_word_count = sum(len(word) > 5 for word in word_list)

        # send mail
        mail_send = False
        if ((long_word_count / len(word_list)) * 100) > 20.00:
            send_mail(
                f'Long word detected',
                f'{title} wikipedia page summary contains more than 20% of long word.',
                f'from@example.com',
                ['to@example.com'],
                fail_silently=False,
            )
            mail_send = True
        
        
            
        # Return response
        return Response({
            'title': title,
            'long word': round((long_word_count / len(word_list)) * 100),
            'mail sent': mail_send,
            'text': summary_text,
            'words list': word_list
        })
        
    except Exception :
        return Response("Error form views:", status=HTTP_500)
    
    
