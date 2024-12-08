from django.contrib import admin
import app

# Register your models here.
admin.site.register(app.models.Profile)
admin.site.register(app.models.Tag)
admin.site.register(app.models.Question)
admin.site.register(app.models.QuestionLike)
admin.site.register(app.models.Answer)
admin.site.register(app.models.AnswerLike)