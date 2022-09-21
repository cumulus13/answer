from django.db import models

class Categories(models.Model):

	name = models.CharField(max_length = 200)
	url = models.CharField(max_length = 500)
	iconImageUrl = models.CharField(max_length = 500, null = True, blank = True, db_column = 'iconimageurl')
	isCrawlable = models.IntegerField(db_column = 'iscrawlable')
	typename = models.CharField(max_length = 50, db_column = '__typename')

	class Meta:
		managed = False
		db_table = 'categories'


class SubCategories(models.Model):
	class Meta:
		managed = False
		db_table = 'sub_categories'

	name = models.CharField(max_length = 200)
	url = models.CharField(max_length = 500)
	iconImageUrl = models.CharField(max_length = 500, null = True, blank = True, db_column = 'iconimageurl')
	isCrawlable = models.IntegerField(db_column = 'iscrawlable')
	typename = models.CharField(max_length = 50, db_column = '__typename')
	parent_id = models.IntegerField()


class SubSubCategories(models.Model):
	class Meta:
		managed = False
		db_table = 'sub_sub_categories'

	name = models.CharField(max_length = 200)
	url = models.CharField(max_length = 500)
	iconImageUrl = models.CharField(max_length = 500, null = True, blank = True, db_column = 'iconimageurl')
	isCrawlable = models.IntegerField(db_column = 'iscrawlable')
	typename = models.CharField(max_length = 50, db_column = '__typename')
	parent_id = models.IntegerField()


class SubSubSubCategories(models.Model):
	class Meta:
		managed = False
		db_table = 'sub_sub_sub_categories'

	name = models.CharField(max_length = 200)
	url = models.CharField(max_length = 500)
	iconImageUrl = models.CharField(max_length = 500, null = True, blank = True, db_column = 'iconimageurl')
	isCrawlable = models.IntegerField(db_column = 'iscrawlable')
	typename = models.CharField(max_length = 50, db_column = '__typename')
	parent_id = models.IntegerField()
