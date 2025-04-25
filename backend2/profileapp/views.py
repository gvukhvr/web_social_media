# profileapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
        profile.delete()
        return Response({"detail": "Profile deleted."}, status=status.HTTP_204_NO_CONTENT)
    except Profile.DoesNotExist:
        return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def list_users(request):
    users = User.objects.all()
    users_data = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return Response(users_data, status=status.HTTP_200_OK)