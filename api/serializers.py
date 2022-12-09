from rest_framework import serializers
from .models import *

class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = '__all__'

class EmployeeUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ('phone','url_photo','biography')

class EmployeeSubdivisionSerializer(serializers.ModelSerializer):
    employee_details = serializers.SerializerMethodField('get_employee_details')
    

    class Meta:
        model = EmployeesSubdivision
        fields = ['employee_details']

    def get_employee_details(self, EmployeesSubdivision):
        # try:
            data = {
                    "employee": {
                        "id_employee": EmployeesSubdivision.id_employee.pk,
                        "employee_name": EmployeesSubdivision.id_employee.user.first_name,
                        "employee_last_name": EmployeesSubdivision.id_employee.user.last_name,
                        "division" : {
                            "id_division": EmployeesSubdivision.id_subdivision.id_division.pk,
                            "division_name": EmployeesSubdivision.id_subdivision.id_division.name_division
                        },
                        "subdivision" : {
                            "id_subdivision": EmployeesSubdivision.id_subdivision.pk,
                            "subdivision_name": EmployeesSubdivision.id_subdivision.name_subdivision
                        }   
                    
                    }     
            }
        # except:
        #     data = None
            
            return data


class SubdivsionsSerializer(serializers.ModelSerializer):
    employee_items= serializers.SerializerMethodField()

    class Meta:
        model = Subdivisions
        fields = ('id_division','name_subdivision', 'employee_items')

    def get_employee_items(self,obj):
        divisions_query= EmployeesSubdivision.objects.filter(id_subdivision=obj.id)
        serializer= EmployeeSubdivisionSerializer(divisions_query, many=True)

        return serializer.data
