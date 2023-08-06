import requests

# mail_to收件人，subject主题，msg_txt邮件内容
class MyEmail:
    def send_mail(self, mail_to, subject, msg_txt):
        print("send email to %s, subject is %s, body is %s" % (mail_to, subject, msg_txt))
        data = dict(
            tos=mail_to,
            content=msg_txt,
            subject=subject,
            format="html"
        )
        url = "http://proxy.zuoyebang.com:1925/api/mail"
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        resp = requests.post(url, data, headers=headers)
        try:
            resp.raise_for_status()
        #python3 的捕获异常的方式
        except Exception as e:
            #python2 的捕获异常的方式
            #except Exception , e:
            print("send mail failed: %s" % e.message)
            return False
        return resp.json()["status"] == 0

#how to use :
# if __name__ == "__main__":
#     my = MyEmail()
#     receivers = "wangjianming@zuoyebang.com"
#     messageSubject = "Test mail"
#     messageText = "Test Mail Content"
#     my.send_mail(receivers,messageSubject,messageText)