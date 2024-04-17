from django.http import JsonResponse


def custom_404_handler(request, exception):
    response_data = {'error': 'Resource not found'}
    return JsonResponse(response_data, status=404)
