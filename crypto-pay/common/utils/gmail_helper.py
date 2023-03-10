from cdc.qa.integrations.email import Gmail
from bs4 import BeautifulSoup


class GmailHelper(Gmail):
    def get_email_link_by_text(self, email: str, subject: str, text: str) -> str:
        message = self.read_latest(to_addr=email, subject=subject)
        soup = BeautifulSoup(message["content"], "html.parser")
        email_link = ""
        all_links = soup.find_all("a")
        for i in all_links:
            try:
                if text.lower() in i.text.lower():
                    email_link = i.attrs["href"]
                    break
            except Exception:
                # Not every link has text, just skip to verify the next
                pass
        return email_link

    def get_email_text(self, email: str, subject: str = ""):
        message = self.read_latest(to_addr=email, subject=subject)
        soup = BeautifulSoup(message["content"], "html.parser")
        tag = soup.body
        email_text = ""
        for string in tag.strings:
            email_text += string
        email_text = email_text.replace("\n", " ").replace("\r", " ")
        email_text = " ".join(email_text.split())
        return email_text

    def check_receive_or_not(self, email: str, subject: str):
        e = None
        try:
            message = self.read_latest(to_addr=email, subject=subject)
            if message is not None:
                return True, e
        except Exception as e1:
            return False, e1

    def get_register_link(self, email: str) -> str:
        register_link = self.get_email_link_by_text(
            email, subject="Crypto.com Pay for Business - Please Verify Your Email", text="Verify"
        )
        return register_link
