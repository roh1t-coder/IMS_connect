from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import User, Employee, Idea, Vote, Collaboration, Reward
from .serializers import EmployeeSerializer, IdeaSerializer, VoteSerializer, CollaborationSerializer, RewardSerializer

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role')
    if not all([username, email, password, role]):
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, email=email, password=password, role=role)
    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def employee_list(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        user_id = request.data.get('user')
        if not User.objects.filter(pk=user_id).exists():
            return Response({'user': 'Invalid pk "{}" - object does not exist.'.format(user_id)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)  # Add logging for validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def employee_detail(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)  # Add logging for validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def idea_list(request):
    if request.method == 'GET':
        ideas = Idea.objects.all()
        serializer = IdeaSerializer(ideas, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        employee_id = request.data.get('employee')
        if not Employee.objects.filter(pk=employee_id).exists():
            return Response({'employee': 'Invalid pk "{}" - object does not exist.'.format(employee_id)}, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data.copy()
        data['submission_date'] = timezone.now()  # Ensure submission_date is set
        
        serializer = IdeaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)  # Add logging for validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def idea_detail(request, pk):
    try:
        idea = Idea.objects.get(pk=pk)
    except Idea.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = IdeaSerializer(idea)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = IdeaSerializer(idea, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)  # Add logging for validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        idea.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def vote(request):
    idea_id = request.data.get('idea')
    user_id = request.data.get('user')
    vote_type = request.data.get('vote_type')
    
    if not all([idea_id, user_id, vote_type]):
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not Idea.objects.filter(pk=idea_id).exists():
        return Response({'error': 'Invalid idea ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not User.objects.filter(pk=user_id).exists():
        return Response({'error': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    vote = Vote.objects.create(idea_id=idea_id, user_id=user_id, vote_type=vote_type)
    return Response({'message': 'Vote recorded successfully'}, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def vote_list(request):
    if request.method == 'GET':
        votes = Vote.objects.all()
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)  # Add logging for validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def vote_detail(request, pk):
    try:
        vote = Vote.objects.get(pk=pk)
    except Vote.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VoteSerializer(vote)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = VoteSerializer(vote, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)  # Add logging for validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def collaboration_list(request):
    if request.method == 'GET':
        collaborations = Collaboration.objects.all()
        serializer = CollaborationSerializer(collaborations, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollaborationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)  # Add logging for validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def collaboration_detail(request, pk):
    try:
        collaboration = Collaboration.objects.get(pk=pk)
    except Collaboration.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CollaborationSerializer(collaboration)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollaborationSerializer(collaboration, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)  # Add logging for validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        collaboration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def reward_list(request):
    if request.method == 'GET':
        rewards = Reward.objects.all()
        serializer = RewardSerializer(rewards, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RewardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)  # Add logging for validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def reward_detail(request, pk):
    try:
        reward = Reward.objects.get(pk=pk)
    except Reward.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RewardSerializer(reward)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = RewardSerializer(reward, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)  # Add logging for validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        reward.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)