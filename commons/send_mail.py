import yagmail
from commons.logger_util import info_log, error_log
from commons.yaml_util import read_config_yaml


def send_mail(attachments):
    """
    把测试报告作为附件发送到指定的QQ邮箱。
    """
    # user：发件人邮箱，password：发件人qq邮箱授权码，host：qq的服务器域名。
    mail_config = {"host": read_config_yaml("MAIL", "host"),
                   "user": read_config_yaml("MAIL", "send_user"),
                   "password": str(read_config_yaml("MAIL", "password"))}
    yag = yagmail.SMTP(**mail_config)
    # 邮件标题。
    subject = "自动化测试报告"
    # 邮件内容。
    contents = "自动化测试结果推送，请查看附件内容。"
    # 收件人qq邮箱，设置to参数为list类型，可以给多个人发邮件。
    to = read_config_yaml("MAIL", "receive_user")
    cc = read_config_yaml("MAIL", "cc_user")
    bcc = read_config_yaml("MAIL", "bcc_user")
    try:
        # 收件人邮箱和收件信息，设置send方法中的cc(抄送)和bcc(秘密抄送)参数，可添加抄送。当需要抄送或秘密抄送多个人时，cc/bcc参数设置为list。
        yag.send(to, subject, contents, attachments, cc, bcc)
        info_log("邮件发送成功！")
        # 关闭服务。
        yag.close()
    except Exception as e:
        error_log("邮件发送失败：{}".format(e))
