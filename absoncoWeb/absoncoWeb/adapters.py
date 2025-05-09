from allauth.socialaccount.adapter import DefaultSocialAccountAdapter # type: ignore
from allauth.account.utils import user_email, user_username, user_field # type: ignore

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        
        # Get profile info from social account
        if sociallogin.account.provider == 'google':
            user_data = sociallogin.account.extra_data
            # Example: set first_name and last_name from Google data
            if 'given_name' in user_data:
                user_field(user, 'first_name', user_data.get('given_name', ''))
            if 'family_name' in user_data:
                user_field(user, 'last_name', user_data.get('family_name', ''))
                
        elif sociallogin.account.provider == 'github':
            user_data = sociallogin.account.extra_data
            # GitHub doesn't provide first/last name directly
            if 'name' in user_data and user_data['name']:
                name_parts = user_data['name'].split(' ', 1)
                user_field(user, 'first_name', name_parts[0])
                if len(name_parts) > 1:
                    user_field(user, 'last_name', name_parts[1])
                    
        # Add other providers as needed
        return user