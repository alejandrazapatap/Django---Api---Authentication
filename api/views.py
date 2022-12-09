from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import *
from .serializers import EmployeeSerializers, EmployeeSubdivisionSerializer, EmployeeUpdateSerializers
from django.db.models import Q

# Create your views here.
class GetEmployeeInfoId(APIView):
    def get(self, request, pk):
        URL = "http://interns.syncronik.com/media/"
        employee= Employees.objects.get(id=pk)
        employee_sub= EmployeesSubdivision.objects.get(id_employee=employee)
        sub= Subdivisions.objects.get(pk=employee_sub.id_subdivision.id)
        div= Divisions.objects.get(id=sub.id_division.id)
        
        data= {"msg":"Accepted","id":employee.id,"first_name": employee.user.first_name,"last_name":employee.user.last_name,
        "email":employee.user.email,"id_role":employee.id_role.name_role, "biography":employee.biography, 
        "url_photo":URL + str(employee.url_photo),"division":div.name_division,"subdivision":sub.name_subdivision}
        return Response(data, status=status.HTTP_200_OK)

class GetAllEmployeesView(APIView):
    #permission_classes= (IsAdminUser,)
    def get(self, request):
        queryset= Employees.objects.all()
        print(queryset)
        serializer= EmployeeSerializers(queryset, many=True)
        serialized_data= serializer.data
        return Response(serialized_data, status.HTTP_200_OK)

class GetEmployeesDivisionsDetailsView(APIView):
    #permission_classes= (IsAdminUser,)
    def get(self,request):
        queryset = EmployeesSubdivision.objects.all()
        serializer = EmployeeSubdivisionSerializer(queryset, many=True)
        serializer_data = serializer.data
        return Response(serializer_data, status.HTTP_200_OK)

# class CreateNewEmployeeView(APIView):
#     permission_classes= (IsAdminUser,)
#     def post(self,request):
#         serializer= EmployeeSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         else:
#             print(serializer.errors)

#         return Response(serializer.data, status.HTTP_201_CREATED)

        
class DeleteEmployeeView(APIView):
    permission_classes= (IsAdminUser,)
    def delete(self, request, pk):
        try:
            employee= Employees.objects.get(id=pk)
            user=CustomUser.objects.get(id=employee.user.id)
            employee_sub= EmployeesSubdivision.objects.get(id_employee=employee)
            
            if employee:
                employee_sub.delete()
                employee.delete()
                user.delete()
                
                return Response({"msg":"Successfully deleted"}, status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response({"msg":"User was not found"}, status.HTTP_404_NOT_FOUND)

class UpdateEmployeeInfo(APIView):
    def put(self, request,pk):
        name = request.data["name"]
        last_name = request.data["last_name"]
        phone = request.data["phone"]
        biography= request.data["biography"]
        url_photo= request.data["url_photo"]
        division = request.data["division"]
        subdivision = request.data["subdivision"]

        employee= Employees.objects.get(pk=pk)
        user= CustomUser.objects.get(id=employee.user.id)
        print(employee)

        if employee:
            user.first_name= name
            user.save()
            user.last_name= last_name
            user.save()
            employee.phone= phone
            employee.save()
            employee.biography= biography
            employee.save()
            employee.url_photo= url_photo
            employee.save()

        sub= Subdivisions.objects.get(pk=subdivision)
        div= Divisions.objects.get(id=sub.id_division.id)
        employee_id = EmployeesSubdivision.objects.get(id_employee= employee)
        if employee_id:
            employee_id.id_subdivision= sub
            employee_id.save()
            employee_id.id_subdivision.id_division=div
            employee_id.save()

        mensaje = {"msg":"Employee actualizado", "id":employee.id, "first_name":user.first_name, "last_name":user.last_name,
            "email":user.email, "phone":employee.phone, "biography":employee.biography,"url_photo":str(employee.url_photo),"id_division":employee_id.id_subdivision.id_division.name_division,"id_subdivision":employee_id.id_subdivision.name_subdivision}    
        return Response(mensaje, status=status.HTTP_200_OK)

        # employee_name = 
        # user= CustomUser.objects.get(id=pk)
        # if user:
        #     user.first_name = name
        #     user.save()
        #     user.last_name = last_name
        #     user.save()
        
        # employee = Employees.objects.get(user=user)
        # if employee:
        #     employee.phone = phone
        #     employee.save()
        #     employee.biography= biography
        #     employee.save()
        #     employee.url_photo= url_photo
        #     employee.save()


        # sub= Subdivisions.objects.get(pk=subdivision)
        # employee_id = EmployeesSubdivision.objects.get(id_employee= employee)
        # if employee_id:
        #     employee_id.id_subdivision= sub
        #     employee_id.save()

        #     print(employee_id)
        # return Response({"msg":"ok"}, status.HTTP_200_OK)