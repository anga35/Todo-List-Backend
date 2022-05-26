from typing import OrderedDict
from django.forms import ValidationError
from rest_framework import serializers

from .models import Task

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model=Task
        fields=['id','name','create_date','deadline','is_done']

    '''

    Override default serializer create to allow list of task json data

    '''

#Override run_validation to return the raw data as validated data
    def run_validation(self, data=...):

       if(type(data) is list):
           return data

       else:
            return super().run_validation(data)


    def is_valid(self, raise_exception=False):


        print("ISVALID")
        return super().is_valid(raise_exception)
    

    def save(self, **kwargs):
        print(self.validated_data)
        print("save")
        
        

#If Validated data is list validate and manually save the data in the list
        if(type(self._validated_data) is list):
            print("ISLIST")
            if not self.validated_data:
                raise serializers.ValidationError("Empty List Provided")

            for data in self.validated_data:
                super().validate(self.to_internal_value(data))

            for data in self.validated_data:
                
                name=data['name']
                request=self.context['request']
                task=Task(name=name,user=request.user)
                if 'deadline' in data.keys():
                    print("INSERTING DEADLINE")
                    task.deadline=data['deadline']


                
                
                task.save()
                
                self.instance=task
            return task

        return super().save(**kwargs)