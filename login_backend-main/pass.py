#ハッシュ化のためのユーティリティ（登録時用） の内容
import bcrypt

# 入力するパスワード（任意）
plain_password = "X4BW6Hb2"
#ここに仮のパスワードを入力して、実行してください。ターミナルにハッシュ化パスワードが出てきます
#コピーしてＤＢに入れてください。

# ハッシュ化（12ラウンドで十分安全）
hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt(12))

# 表示
print("元のパスワード:", plain_password)
print("ハッシュ化パスワード:", hashed.decode('utf-8'))