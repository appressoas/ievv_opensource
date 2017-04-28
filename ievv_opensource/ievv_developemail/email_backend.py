from django.core.mail.backends.base import BaseEmailBackend

from ievv_opensource.ievv_developemail.models import DevelopEmail


class DevelopEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        developemails = []
        for message in email_messages:
            developemail = DevelopEmail(raw_content=str(message))
            print()
            print("*" * 70)
            print()
            print(dir(message))
            print()


            developemails.append(developemail)
        # DevelopEmail.objects.bulk_create(developemails)
        return len(list(email_messages))
