# tweet-cleaner

ツイ消しスクリプト  
でしたが、いろいろ増えてきました  
いろいろ入ってます。  
apiのバージョンはv1です。  

# usage

```bash
mkdir config

cp config.ini.sample config/config.ini

# CONSUMER_TOKEN, CONSUMER_TOKEN_SECRETを設定
vim config.ini

# PINコードを入力してアクセストークンを取る
# config.screen_name.iniが生成される
python src/auth.py --config config/config.ini

# ツイート消す
python src/delete-tweet.py --config config/config.screen_name.ini

```
