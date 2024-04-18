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
    request_type=request.data.get('type')
    print(f'request:- {request} requestData:- {request.data.get('type')}')
    serializer = VideoSerializer(data=request.data)
    if serializer.is_valid():
        input_video = serializer.validated_data['input_video']
        
        # Save the uploaded video to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_video_file:
            for chunk in input_video.chunks():
                temp_video_file.write(chunk)
        
        # Define output file path for audio
        if request_type=="video_to_audio":
            file_path = os.path.join('media', 'audio', f'{temp_video_file.name}.mp3')
        elif request_type=="compressor":
            file_path = os.path.join('media', 'video', f'{temp_video_file.name}.mp4')
        
        try:
            # Run FFmpeg command to extract audio
            if request_type=="video_to_audio":
                ffmpeg.input(temp_video_file.name).output(file_path).run()
            elif request_type=="compressor":
                ffmpeg.input(temp_video_file.name).output(file_path,    vcodec='libx264', b='1.5M',acodec='aac',ab='128k').run()
            # Delete the temporary video file
            os.unlink(temp_video_file.name)

            #Read the extracted audio data
            with open(file_path,'rb') as file_data:
                file_data_Read=file_data.read()
                if request_type=="video_to_audio": 
                    response=HttpResponse(file_data_Read,content_type='audio/mpeg')
                    response['Content-Disposition']=f'attachment; filename={temp_video_file.name}.mp3'
                elif request_type=="compressor":
                    response=HttpResponse(file_data_Read,content_type='video/mp4')
                    response['Content-Disposition']=f'attachment; filename={temp_video_file.name}.mp4'
                    # response['Content-Disposition']=f'attachment; filename={temp_video_file.name}.mp3'
            
            return response
        except ffmpeg.Error as e:
            # Handle FFmpeg errors
            os.unlink(temp_video_file.name)  # Ensure temporary file is deleted
            return Response({'error': str(e)}, status=500)
    else:
        # Return serializer errors if data is invalid
        return Response(serializer.errors, status=400)


