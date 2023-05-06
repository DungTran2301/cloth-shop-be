
from django.conf import settings
import jwt

def user_id(request):
  auth_header = request.headers.get('Authorization')
  token = auth_header.split(' ')[1]
  decoded_token = jwt.decode(
      token, settings.SECRET_KEY, algorithms=['HS256'])
  user_id = decoded_token['user_id']
  return user_id