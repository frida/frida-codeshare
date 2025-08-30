import logging
logger = logging.getLogger(__name__)

def associate_existing_user(strategy, details, response, user=None, *args, **kwargs):
    """Associate with existing user based on GitHub ID from Auth0"""
    from fridasnippits.apps.frontend.models import User
    
    if user:  # Already found a user, skip
        return {'user': user}
    
    # Log the Auth0 data for debugging
    logger.error(f"Auth0 Response: {response}")
    logger.error(f"Auth0 Details: {details}")
    
    # Extract GitHub user ID from Auth0 response
    # Auth0 format is usually like "github|1072598"
    user_id = details.get('user_id') or response.get('sub') or response.get('user_id')
    if user_id and 'github|' in user_id:
        github_id = user_id.split('github|')[1]
        expected_username = f'github-{github_id}'
        
        try:
            existing_user = User.objects.get(username=expected_username)
            logger.error(f"Found existing user: {existing_user.username}")
            return {'user': existing_user, 'is_new': False}
        except User.DoesNotExist:
            logger.error(f"No user found with username: {expected_username}")
    
    return {}

def save_auth0_profile(strategy, details, response, user=None, *args, **kwargs):
    """Custom pipeline function to save Auth0 profile data to User model"""
    # Log the Auth0 data for debugging
    logger.error(f"Auth0 Response: {response}")
    logger.error(f"Auth0 Details: {details}")
    logger.error(f"Current user: {user}")
    
    if user:
        # Get nickname from Auth0 profile
        nickname = response.get('nickname') or details.get('username')
        
        # Update user with Auth0 profile data
        if nickname and not user.nickname:
            user.nickname = nickname
            user.save()
    
    return {'user': user}