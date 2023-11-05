from tortoise import fields
class UserQuery(models.Model):
    id = fields.IntField(pk=True)
    username =fields.CharField(max_length=255,default='')
    queryname = fields.CharField(max_length=255)
    parameters: fields.ReverseRelation["Parameters"]
class Parameters(models.Model):
    id = fields.IntField(pk=True)
    userquery: fields.ForeignKeyRelation[UserQuery] = fields.ForeignKeyField(
        "models.UserQuery", related_name="queryname"
    )    
    parameter_name = fields.CharField(max_length=500,default='')
    parameter_value = fields.CharField(max_length=500,default='')

