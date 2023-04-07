import jwt

admin_token = jwt.encode({'username': 'admin'}, '53cr3T_ke3e3e3eY', algorithm='HS256')

print(admin_token)