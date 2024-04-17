from django.http import JsonResponse, HttpResponse
from .models import Books
import tempfile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import VideoSerializer
import ffmpeg
import os


def Book_Title(request):
    books=Books.objects.all()
    print(f'books:- {books} Books Value:- {books.values}')
    data={"books":"list(books.values)"}
    return JsonResponse(data)

@api_view(['POST'])
def video_extract_audio(request):
    serializer = VideoSerializer(data=request.data)
    if serializer.is_valid():
        input_video = serializer.validated_data['input_video']
        
        # Save the uploaded video to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_video_file:
            for chunk in input_video.chunks():
                temp_video_file.write(chunk)
        
        # Define output file path for audio
        audio_file_path = os.path.join('media', 'audio', f'{temp_video_file.name}.mp3')
        
        try:
            # Run FFmpeg command to extract audio
            ffmpeg.input(temp_video_file.name).output(audio_file_path).run()
            
            # Delete the temporary video file
            os.unlink(temp_video_file.name)

            #Read the extracted audio data
            with open(audio_file_path,'rb') as audio_file:
                audio_data=audio_file.read()
                response=HttpResponse(audio_data,content_type='audio/mpeg')
                response['Content-Disposition']='attachment; filename="extracted_audio.mp3"'
            
            return response
        except ffmpeg.Error as e:
            # Handle FFmpeg errors
            os.unlink(temp_video_file.name)  # Ensure temporary file is deleted
            return Response({'error': str(e)}, status=500)
    else:
        # Return serializer errors if data is invalid
        return Response(serializer.errors, status=400)


