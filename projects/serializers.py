from django.shortcuts import get_object_or_404
from projects.models import Project, CompanyProjectComparison,ProjectImage,ProjectImageSet
from datetime import datetime
from companies.models import Company
from companies.serializers import GeneralRemarkJsonSerializer, SetChargingStagesSerializer,SetQuotationGeneralRemarkSerializer,SetInvoiceGeneralRemarkSerializer,SetReceiptGeneralRemarkSerializer
from customers.models import Customer
from customers.serializers import CustomerJsonSerializer
from rooms.serializers import RoomItemJsonSerializer,ProjectItemByRoomJsonSerializer
from project_expenses.serializers import ProjectExpenseJsonSerializer
from project_timetable.models import ProjectMilestone
from rest_framework import serializers
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist, ValidationError
from common.fields import Base64ImageField

class CreateProjectSerializer(serializers.ModelSerializer):

	class Meta:
		model=Project
		fields=("project_title","district","work_location","status","start_date","due_date")

	def create(self, validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise ValidationError("You must create a company first.")
		if not company.company_charging_stages:
			raise ValidationError("You must create company's charging stages first.")
		if not company.company_doc_format:
			raise ValidationError("You must create company's document format first.")
		if not company.company_doc_header:
			raise ValidationError("You must create company's document header first.")
		ccss=company.company_charging_stages
		cs=[]
		for i in range(ccss.quantity):
			r={}
			r["value"]=ccss.values[i]
			if ccss.descriptions[i]!=None and ccss.descriptions[i]!="":
				r["description"]=ccss.descriptions[i]
			cs.append(r)
		cdf=company.company_doc_format
		df={
			"project_upper_format":cdf.project_upper_format,
			"project_lower_format":cdf.project_lower_format,
			"quot_upper_format":cdf.quot_upper_format,
			"quot_middle_format":cdf.quot_middle_format,
			"quot_lower_format":cdf.quot_lower_format,
			"invoice_upper_format":cdf.invoice_upper_format,
			"invoice_middle_format":cdf.invoice_middle_format,
			"invoice_lower_format":cdf.invoice_lower_format,
			"receipt_upper_format":cdf.receipt_upper_format,
			"receipt_middle_format":cdf.receipt_middle_format,
			"receipt_lower_format":cdf.receipt_lower_format
		}

		project=Project.objects.create(project_title=validated_data["project_title"],
			district=validated_data["district"],
			company=company,
			charging_stages=cs,
			document_format=df,
			created_by=user,
			job_no=company.job_no+int(cdf.project_based_number),
			quotation_remarks=company.get_quotation_general_remarks_json(),
			invoice_remarks=company.get_invoice_general_remarks_json(),
			receipt_remarks=company.get_receipt_general_remarks_json()
		)
		company.job_no+=1
		company.save()
		if validated_data.get("work_location"):
			project.work_location=validated_data["work_location"]
		if validated_data.get("status"):
			project.status=validated_data["status"]
		if validated_data.get("start_date"):
			project.start_date=validated_data["start_date"]
		if validated_data.get("due_date"):
			project.due_date=validated_data["due_date"]
		project.save()
		return project

class UpdateProjectSerializer(serializers.ModelSerializer):
	project_id=serializers.IntegerField()
	class Meta:
		model=Project
		fields=("project_id","project_title","district","work_location","status","start_date","due_date")

	def update(self, instance,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise ValidationError("You must create a company first.")

		project=get_object_or_404(Project,id=instance)

		if user==project.company.owner:

			if validated_data.get("project_title"):
				project.project_title=validated_data["project_title"]
			if validated_data.get("district"):
				project.district=validated_data["district"]
			if validated_data.get("work_location"):
				project.work_location=validated_data["work_location"]
			if validated_data.get("status"):
				project.status=validated_data["status"]
			if validated_data.get("start_date"):
				project.start_date=validated_data["start_date"]
			if validated_data.get("due_date"):
				project.due_date=validated_data["due_date"]
			project.updated_on=datetime.now()
			project.save()
			return project
		else:
			raise PermissionDenied

class GetProjectRequestSerializer(serializers.Serializer):
	project_id=serializers.IntegerField()

class SetCompanyProjectComparisonSerializer(serializers.ModelSerializer):
	
	class Meta:
		model=CompanyProjectComparison
		fields=('projects',)

	def create(self,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise ValidationError("You must create a company first.")

		if user==company.owner:
			comparison, craeted=CompanyProjectComparison.objects.get_or_create(company=company)
			comparison.projects.set(validated_data["projects"])
			comparison.save()
			return comparison

class GetProjectWithChargingStageRequestSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	charging_stage=serializers.IntegerField()

class SetProjectChargingStagesSerializer(serializers.Serializer):
	project_id=serializers.IntegerField()
	#charging_stages=SetChargingStagesSerializer()

	def create(self,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise ValidationError("You must create a company first.")

		project=get_object_or_404(Project,id=validated_data["project_id"])
		if user==project.company.owner:
			'''if project.quotation_generated_on:
				raise ValidationError("The quotation is not allowed to update")'''
			
			ccss=company.company_charging_stages
			cs=[]
			for i in range(ccss.quantity):
				r={}
				r["value"]=ccss.values[i]
				if ccss.descriptions[i]!=None and ccss.descriptions[i]!="":
					r["description"]=ccss.descriptions[i]
				cs.append(r)
			project.charging_stages=cs
			project.save()
			return project
			'''ccss=validated_data["charging_stages"]
			cs=[]
			for i in range(ccss["quantity"]):
				r={}
				r["value"]=ccss["values"][i]
				if ccss["descriptions"][i]!=None and ccss["descriptions"][i]!="":
					r["description"]=ccss["descriptions"][i]
				cs.append(r)
			project.charging_stages=cs
			project.save()
			return project'''

class SetProjectQuotationRemarksSerializer(serializers.Serializer):
	project_id=serializers.IntegerField()
	quotation_remarks=SetQuotationGeneralRemarkSerializer()

	def create(self,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise ValidationError("You must create a company first.")

		project=get_object_or_404(Project,id=validated_data["project_id"])
		if user==project.company.owner:
			
			project.quotation_remarks=validated_data["quotation_remarks"]
			project.save()
			return project

class SetProjectInvoiceRemarksSerializer(serializers.Serializer):
	project_id=serializers.IntegerField()
	invoice_remarks=SetInvoiceGeneralRemarkSerializer()

	def create(self,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise ValidationError("You must create a company first.")

		project=get_object_or_404(Project,id=validated_data["project_id"])
		if user==project.company.owner:
			
			project.invoice_remarks=validated_data["invoice_remarks"]
			project.save()
			return project

class SetProjectReceiptRemarksSerializer(serializers.Serializer):
	project_id=serializers.IntegerField()
	receipt_remarks=SetReceiptGeneralRemarkSerializer()

	def create(self,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise ValidationError("You must create a company first.")

		project=get_object_or_404(Project,id=validated_data["project_id"])
		if user==project.company.owner:
			
			project.receipt_remarks=validated_data["receipt_remarks"]
			project.save()
			return project

class CreateProjectImageSetRequestSerializer(serializers.Serializer):
	related_project=serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
	project_milestone=serializers.PrimaryKeyRelatedField(queryset=ProjectMilestone.objects.all())
	imgs=serializers.ListField(child=Base64ImageField(max_length=None, use_url=True,required=False,allow_null=True))

class GetProjectImageSetRequestSerializer(serializers.Serializer):
	id=serializers.IntegerField()

class GetProjectImageRequestSerializer(serializers.Serializer):
	id=serializers.IntegerField()

class ProjectImageSerializer(serializers.ModelSerializer):
	class Meta:
		model=ProjectImage
		fields=("img")

class ImageSetControlSerializer(serializers.Serializer):
	remove=serializers.ListField(child=serializers.IntegerField())
	add=serializers.ListField(child=Base64ImageField(max_length=None, use_url=True,required=False,allow_null=True))


class ProjectImageSetSerializer(serializers.ModelSerializer):
	img_control=ImageSetControlSerializer(required=False)
	imgs=serializers.ListField(required=False,child=Base64ImageField(max_length=None, use_url=True,required=False,allow_null=True))
	class Meta:
		model=ProjectImageSet
		fields=("imgs","related_project","project_milestone","img_control")

	def create(self,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise ValidationError("You must create a company first.")

		if validated_data.get("related_project"):
			project=validated_data["related_project"]

		elif validated_data.get("project_milestone"):
			project=validated_data["project_milestone"].project

		else:
			raise ValidationError("You must assign a related object to the image set.")

		#project=get_object_or_404(Project,id=project_id)
		_imgs=[]
		if project.company.owner==user:
			
			if len(validated_data["imgs"])>5:
				raise ValidationError("You can't assign more than 5 images")
			for img in validated_data["imgs"]:
				_img=ProjectImage.objects.create(related_project=project,img=img)
				_imgs.append(_img)

			if validated_data.get("related_project"):
				ret=ProjectImageSet.objects.create(related_project=validated_data["related_project"])
				ret.imgs.set(_imgs)

			elif validated_data.get("project_milestone"):
				ret=ProjectImageSet.objects.create(project_milestone=validated_data["project_milestone"])
				ret.imgs.set(_imgs)
			return ret

		raise PermissionDenied

	def update(self,instance,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise ValidationError("You must create a company first.")
		project=instance.related_project if instance.related_project!=None else instance.project_milestone.project
		_imgs=[]
		if project.company.owner==user:
			
			if instance.imgs.count()-len(validated_data["img_control"]["remove"])+len(validated_data["img_control"]["add"])>5:
				raise ValidationError("You can't assign more than 5 images")
			ProjectImage.objects.filter(pk__in=validated_data["img_control"]["remove"]).delete()
			if instance.imgs.count()+len(validated_data["img_control"]["add"])>5:
				raise ValidationError("You can't assign more than 5 images")
			for img in validated_data["img_control"]["add"]:
				_img=ProjectImage.objects.create(related_project=project,img=img)
				_imgs.append(_img)
			instance.imgs.add(*_imgs)
		return instance



class ProjectJsonSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	project_title=serializers.CharField()
	status=serializers.CharField()
	details=serializers.CharField()
	work_location=serializers.CharField()
	start_date=serializers.DateField()
	due_date=serializers.DateField()
	customer=CustomerJsonSerializer()


class GetProjectResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	project=ProjectJsonSerializer()

class ListProjectResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	projects=ProjectJsonSerializer(many=True)

class CompanyProjectComparisoJsonSerializer(serializers.Serializer):
	total_income=serializers.FloatField()
	total_outcome=serializers.FloatField()
	gross_profit_margin=serializers.FloatField()

class ListCompanyProjectComparisonSelectionsResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	selections=CompanyProjectComparisoJsonSerializer(many=True)

class GetCompanyProjectComparisonResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	comparisons=CompanyProjectComparisoJsonSerializer(many=True)

class QuotationFormatJsonSerializer(serializers.Serializer):
	quot_upper_format=serializers.CharField()
	quot_middle_format=serializers.CharField()
	quot_lower_format=serializers.CharField()

class InvoiceFormatJsonSerializer(serializers.Serializer):
	invoice_upper_format=serializers.CharField()
	invoice_middle_format=serializers.CharField()
	invoice_lower_format=serializers.CharField()

class ReceiptFormatJsonSerializer(serializers.Serializer):
	receipt_upper_format=serializers.CharField()
	receipt_middle_format=serializers.CharField()
	receipt_lower_format=serializers.CharField()

class ProjectAllItemJsonSerializer(serializers.Serializer):
	items=RoomItemJsonSerializer(many=True)

class ProjectChargingStageSerializer(serializers.Serializer):
	value=serializers.IntegerField()
	content=serializers.CharField()

class ProjectChargingStagesSeriailizer(serializers.Serializer):
	charging_stages=ProjectChargingStageSerializer(many=True)

class ProjectQuotationPreviewJsonSerializer(serializers.Serializer):
	job_no=serializers.CharField()
	quot_format=QuotationFormatJsonSerializer()
	items=serializers.DictField(child=ProjectAllItemJsonSerializer())
	charging_stages=ProjectChargingStagesSeriailizer()
	general_remarks=serializers.ListField(child=GeneralRemarkJsonSerializer())
	quotation_no=serializers.CharField()
	customer_contact=CustomerJsonSerializer()
	#can_update_charging_stage=serializers.BooleanField()

class ProjectQutationPreviewResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	quot_preview=ProjectQuotationPreviewJsonSerializer()

class ProjectInvoicePreviewJsonSerializer(serializers.Serializer):
	job_no=serializers.CharField()
	invoice_format=InvoiceFormatJsonSerializer()
	amount=serializers.FloatField()
	total_amount=serializers.FloatField()
	charging_stage=ProjectChargingStageSerializer()
	general_remarks=serializers.ListField(child=GeneralRemarkJsonSerializer())
	invoice_no=serializers.CharField()
	customer_contact=CustomerJsonSerializer()

class ListChargingStageAmountJsonSerializer(serializers.Serializer):
	value=serializers.IntegerField()
	price=serializers.FloatField()

class ListProjectInvoiceResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	charging_stages=ListChargingStageAmountJsonSerializer(many=True)

class ProjectInvoicePreviewResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	invoice_preview=ProjectInvoicePreviewJsonSerializer()

class ProjectReceiptPreviewJsonSerializer(serializers.Serializer):
	job_no=serializers.CharField()
	receipt_format=ReceiptFormatJsonSerializer()
	amount=serializers.FloatField()
	total_amount=serializers.FloatField()
	charging_stage=ProjectChargingStageSerializer()
	general_remarks=serializers.ListField(child=GeneralRemarkJsonSerializer())
	receipt_no=serializers.CharField()
	customer_contact=CustomerJsonSerializer()

class ListProjectReceiptResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	charging_stages=ListChargingStageAmountJsonSerializer(many=True)

class ProjectReceiptPreviewResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	receipt_preview=ProjectReceiptPreviewJsonSerializer()

class ProjectItemByTypeJsonSerializer(serializers.Serializer):
	items=RoomItemJsonSerializer(many=True)
	sum_price=serializers.FloatField()

class GetProjectAllItemResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	items=serializers.DictField(child=ProjectItemByTypeJsonSerializer())

class GetProjectAllRoomItemResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	items=serializers.DictField(child=ProjectItemByRoomJsonSerializer())

class ProjectExpenseByTypeJsonSerializer(serializers.Serializer):
	items=ProjectExpenseJsonSerializer(many=True)
	sum_price=serializers.FloatField()

class ProjectChargingStageJsonSerializer(serializers.Serializer):
	value=serializers.IntegerField()
	description=serializers.CharField()
	sum_price=serializers.FloatField()
	date=serializers.DateField()

class GetProjectProfitAnalysisJsonSerializer(serializers.Serializer):
	income_items=ProjectChargingStageJsonSerializer(many=True)
	outcome_items=serializers.DictField(child=ProjectExpenseByTypeJsonSerializer())
	total_income=serializers.FloatField()
	total_outcome=serializers.FloatField()
	gross_profit_margin=serializers.FloatField()


class GetProjectProfitAnalysisResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	project_profit_analysis=GetProjectProfitAnalysisJsonSerializer()

class ProjectStatusJsonSerializer(serializers.Serializer):
	project_status=serializers.ListField(child=serializers.CharField(),max_length=2,min_length=2)

class ListProjectStatusResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	project_status_list=ProjectStatusJsonSerializer()