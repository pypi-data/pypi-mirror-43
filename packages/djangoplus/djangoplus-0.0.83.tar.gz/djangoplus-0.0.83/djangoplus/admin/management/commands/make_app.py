# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from djangoplus.tools.browser import Browser


class Command(BaseCommand):

    def handle(self, *args, **options):
        #browser = Browser('http://localhost:8000')
        #browser.open('/')
        #browser.wait(2)
        #browser.save_screenshot('base.png')

        def resize(w, h):
            from PIL import Image
            im = Image.open('base.png')
            width, height = im.size
            print(width, height)
            if width > height:
                percent = 100 * h / height / 100
                print('h', percent)
            else:
                percent = 100 * w / width / 100
                print('w', percent)
            width = int(width * percent)
            height = int(height * percent)
            print(width, height, 9999)
            im = im.resize((width, height), Image.ANTIALIAS)
            x, y = width / 2 - w / 2, height / 2 - h / 2
            new_img = im.crop((x, y, x + w, y + h))
            print(new_img.size)
            new_img.save('output.png')

        #browser.wait(2)
        resize(1024, 500)
        #browser.close()
