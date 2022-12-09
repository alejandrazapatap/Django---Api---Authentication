from django.shortcuts import render
from django.contrib.auth import  login, logout
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password,check_password
from rest_framework.authtoken.models import Token
from api.models import Employees,Roles,EmployeesSubdivision,Subdivisions,Divisions
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes




from authentication.models import CustomUser
from api.models import Employees


# Create your views here.
@parser_classes((MultiPartParser, ))
class RegisterView(APIView):
    permission_classes= (IsAdminUser,)
    '''Registrar usuario'''
    def post(self,request):
        email = request.data['email']
        password = make_password(request.data['password'])
        first_name = request.data['first_name']  
        last_name = request.data['last_name']
        phone= request.data['phone']
        biography= request.data['biography']
        try:
            url_photo= request.FILES['url_photo']
        except:
            url_photo=""
        id_division= request.data['id_division']
        id_subdivision=request.data['id_subdivision']
        
        try:
            user = CustomUser.objects.create(email=email,password=password,first_name=first_name,last_name=last_name)
            Token.objects.create(user=user)
            id_role= Roles.objects.get(id=2)
            employee= Employees.objects.create(user=user, phone= phone, biography=biography, url_photo=url_photo,id_role=id_role)
            division= Divisions.objects.get(id=id_division)
            subdivision= Subdivisions.objects.get(id=id_subdivision)
            E_subdivision=EmployeesSubdivision.objects.create(id_employee=employee,id_subdivision=subdivision)
            
            
            
            mensaje = {"msg":"Employee registrado", "id":employee.id, "first_name":user.first_name, "last_name":user.last_name,
            "email":user.email, "phone":employee.phone, "biography":employee.biography,"url_photo":str(employee.url_photo), "id_role":id_role.name_role,"division":division.name_division,"subdivision":subdivision.name_subdivision}
            estado = status.HTTP_201_CREATED
        except Exception as err:
            print(err)
            mensaje = {"msg":"No se pudo registrar el usuario"}
            estado = status.HTTP_400_BAD_REQUEST
        return Response(mensaje,estado)
           


class LoginView(APIView):
    '''Logear usuario'''
    def post(self,request):
        '''Ask data'''
        email = request.data['email']
        password = request.data['password']
        email = email.replace(" ", "")
              
        try:
            '''Get the user data, compared the password given by the user with the hash password'''
            user = CustomUser.objects.get(email=email)
            pass_user = user.password
            check_pass = check_password(password,pass_user)
            employee = Employees.objects.get(user=user)
                    
        except:
            '''If check password is False'''
            check_pass = False
        
        if check_pass:
            '''Get user token, if it doesn't exist, create token'''
            try:
                token= Token.objects.get(user=user)


            except Token.DoesNotExist:
                token= Token.objects.create(user=user)
            '''Send the user data with the status code if it was accepted'''
            data= {"msg":"Accepted","id":user.id,"first_name": user.first_name,"last_name":user.last_name,"email":user.email,"id_role":employee.id_role.name_role,"token":str(token.key)}
            estado= status.HTTP_202_ACCEPTED
        else:
            '''Send status unauthorized if the credentials are incorrect or invalid'''
            data= {"msg": "Invalid credentials"}
            estado= status.HTTP_401_UNAUTHORIZED
            '''Send the response based on the case'''
        return Response(data,estado)
        
         
        # if user is not None:
        #     login(request, user)
        # Redirect to a success page.
        
        
        
class LogoutView(APIView):
    '''Logout usuario'''
    def post(self,request):
        email = request.data['email']
        try:
            user= CustomUser.objects.get(email=email)
            token= Token.objects.get(user=user)
            token.delete()
            mensaje= {"msg":"Successfully logged out"}
            estado= status.HTTP_200_OK

        except:
            mensaje= {"msg":"Invalid credentials"}
            estado= status.HTTP_401_UNAUTHORIZED
        return Response(mensaje,estado)


# Redirect to a success page.       