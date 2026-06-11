from django.shortcuts import redirect

class StaffRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Проверяем перед обработкой запроса
        if (request.path == '/' and 
            request.user.is_authenticated and 
            request.user.is_staff):
            return redirect('admin_dashboard')
        
        response = self.get_response(request)
        return response