from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


# create role based json token
def create_token(user):
	user_role = 'none'
	refresh = RefreshToken.for_user(user)

	if user.is_superuser:
		user_role = 'super_user'
	elif user.is_staff:
		user_role = 'staff'
	elif user.is_admin:
		user_role = 'admin'
	else:
		user_role = 'none'

	try:
		profile_pic = user.profile_pic.url
	except:
		profile_pic = ''

	return {
		'refresh_token': str(refresh),
		'access_token': str(refresh.access_token),
		'user_role': user_role,
        'user_id': user.id,
        'profile_pic': profile_pic,
        'name': user.name
	}