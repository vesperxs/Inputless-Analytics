from zipfile import BadZipFile
from textract import exceptions
from textract import process
import docx2txt
import mailbox
import bs4

from .normalize_text import normalize_raw_text
from .offsets import Paragraph


# from .entity_extractor import build_dataframe

def get_html_text(html):
    try:
        return bs4.BeautifulSoup(html, 'lxml').body.get_text(' ', strip=True)
    except AttributeError: # message contents empty
        return None

def create_txt(mbox_obj):
    for idx, email_obj in enumerate(mbox_obj):
        email_data = GmailMboxMessage(email_obj)
        sub, text = email_data.parse_email()
        with open(sub.replace('/','-') + '.txt', 'w') as f:
            f.write(text[1][2])

class GmailMboxMessage():
    def __init__(self, email_data):
        if not isinstance(email_data, mailbox.mboxMessage):
            raise TypeError('Variable must be type mailbox.mboxMessage')
        self.email_data = email_data

    def parse_email(self):
        email_labels = self.email_data['X-Gmail-Labels']
        email_date = self.email_data['Date']
        email_from = self.email_data['From']
        email_to = self.email_data['To']
        email_subject = self.email_data['Subject']
        email_text = self.read_email_payload()
        return (email_subject, email_text)

    def read_email_payload(self):
        email_payload = self.email_data.get_payload()
        if self.email_data.is_multipart():
            email_messages = list(self._get_email_messages(email_payload))
        else:
            email_messages = [email_payload]
        return [self._read_email_text(msg) for msg in email_messages]

    def _get_email_messages(self, email_payload):
        for msg in email_payload:
            if isinstance(msg, (list,tuple)):
                for submsg in self._get_email_messages(msg):
                    yield submsg
            elif msg.is_multipart():
                for submsg in self._get_email_messages(msg.get_payload()):
                    yield submsg
            else:
                yield msg

    def _read_email_text(self, msg):
        content_type = 'NA' if isinstance(msg, str) else msg.get_content_type()
        encoding = 'NA' if isinstance(msg, str) else msg.get('Content-Transfer-Encoding', 'NA')
        if 'text/plain' in content_type and 'base64' not in encoding:
            msg_text = msg.get_payload()
        elif 'text/html' in content_type and 'base64' not in encoding:
            msg_text = get_html_text(msg.get_payload())
        elif content_type == 'NA':
            msg_text = get_html_text(msg)
        else:
            msg_text = None
        return (content_type, encoding, msg_text)


class ParseData:
    def __init__(self, index):
        self._index = index

    @staticmethod
    def parse(index, f_type):
        try:
            if f_type == '.docx':
                raw_text = docx2txt.process(index)
            #elif f_type == '.mbox':
            #    mboxobj = mailbox.mbox(index)
            #    create_txt(mboxobj)
            else:
                raw_text = process(index, extension= f_type, encoding='utf-8').decode()

            cleaned_text = normalize_raw_text(raw_text)
            case: Paragraph = Paragraph(index, cleaned_text)
            return case

        except exceptions.ShellError:
            pass
        except UnicodeDecodeError:
            pass
        except TypeError:
            pass
        except ValueError:
            pass
        except BadZipFile:
            pass
    
    def filter_by_types(self):

        filename = self._index.split("/")[-1]
        if filename.lower().endswith('.docx'):
            return self.parse(self._index, '.docx')
        elif filename.lower().endswith('.doc'):
            return self.parse(self._index, '.doc')
        elif filename.lower().endswith('.pdf'):
            return self.parse(self._index, '.pdf')
        elif filename.lower().endswith('.odt'):
            return self.parse(self._index,'.odt')
        elif filename.lower().endswith('.csv'):
            return self.parse(self._index,'.csv')
        elif filename.lower().endswith('.xls'):
            return self.parse(self._index,'.xls')
        elif filename.lower().endswith('.xlsx'):
            return self.parse(self._index,'.xlsx')
        elif filename.lower().endswith('.pptx'):
            return self.parse(self._index,'.pptx')
        elif filename.lower().endswith('.txt'):
            return self.parse(self._index,'.txt')



        else:
            pass
