#coding=utf-8
from Tools.scripts.treesync import raw_input
import os
import re

import django
import rsa




os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_sso.settings")
django.setup()
from sso_server.models import Consumer

def key_generate():
    #生成
    try:
        public_key,private_key = rsa.newkeys(512)
        public_key = public_key.save_pkcs1().decode()
        private_key = private_key.save_pkcs1().decode()
        
        name = raw_input("请输入应用的名字：")
        Consumer.objects.create(
            name = name,
            public_key = re.sub("\s","",public_key),
            private_key = re.sub("\s","",private_key)
        )
        print("成功生成！")
    except Exception as e:
        print("出错！")
        print(e)
        
if __name__ == "__main__":
    key_generate()
    
    
    
       