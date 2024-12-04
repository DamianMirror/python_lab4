# your_project/middleware.py

from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    """
    Middleware, що перенаправляє неаутентифікованих користувачів на сторінку логіну.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = reverse('login')
        self.exempt_urls = [
            reverse('login'),
            reverse('register'),
            # Додайте інші URL, які не потребують захисту
        ]

    def __call__(self, request):
        if not request.user.is_authenticated:
            if request.path not in self.exempt_urls and not request.path.startswith('/api/'):
                return redirect(self.login_url)
        response = self.get_response(request)
        return response
