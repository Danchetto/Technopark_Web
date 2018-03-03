from django.core.management.base import BaseCommand, CommandError
from questions.models import *

class Command(BaseCommand):


    def handle(self, *args, **options):
        for i in range(3):
            question = Question(title="test_data" + str(i),
            text="Creating by test", likes=0, dislikes=0)

            question.save()

            tags = ["tag1", "tag2", "tag3"]

            for tag in tags:
                try:
                    new_tag = Tag.objects.get(name=tag)
                except:
                    new_tag = Tag(name=tag)
                    new_tag.save()
                question.tags.add(new_tag)


            for k in range(3):
                answer = Answer(text="answer for test data" + str(k), question=question, correct=False)
                question.answer_count += 1
                answer.save()

            question.save()

        self.stdout.write('Successfully created test data')