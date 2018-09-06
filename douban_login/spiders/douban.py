# -*- coding: utf-8 -*-
import scrapy
from urllib import request
from PIL import Image


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    start_urls = ["https://accounts.douban.com/login"]
    login_url = "https://accounts.douban.com/login"
    profile_url = 'https://www.douban.com/people/97956064/'
    editsignature_url = 'https://www.douban.com/people/97956064/edit_signature'

    def parse(self, response):
        formdata = {
            'source': 'None',
            'redir': 'https://www.douban.com',
            'form_email': 'xxxxxx@qq.com',
            'form_password': 'xxxxxxxx',
            'remember': 'on',
            'login': '登录',
        }
        captcha_url = response.css('img#captcha_image::attr(src)').get()
        # print(captcha_url)
        if captcha_url:
            captcha = self.regonize_captcha(captcha_url)
            formdata['captcha-solution'] = captcha
            captcha_id = response.xpath("//input[@name='captcha-id']/@value").get()
            formdata['captcha-id'] = captcha_id
        yield scrapy.FormRequest(url=self.login_url, formdata=formdata, callback=self.parse_after_login)

        # 是否登录成功
        def parse_after_login(self, response):
            if response.url == 'http://www.douban.com/':
                yield scrapy.Request(self.profile_url, callback=self.parse_projile)
                print('登录成功!')
            else:
                print('登录失败!')


# 进入到了个人中心!
def parse_projile(self, response):
    print(response.url)
    if response.url == self.profile_url:
        ck = response.xpath("//input[@name='ck']/@value").get()
        formdata = {
            'ck': ck,
            'signature': '我就是我,不一样的烟火!'
        }
        yield scrapy.FormRequest(self.editsignature_url, formdata=formdata)
    else:
        print('没有进入到个人中心!')


# 识别验证码
def regonize_captcha(self, image_url):
    request.urlretrieve(image_url, 'captcha.png')
    image = Image.open('captcha.png')
    image.show()
    captcha = input('请输入验证码:')
    return captcha
