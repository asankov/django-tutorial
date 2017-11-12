import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question

INDEX_URL = reverse('polls:index')


class QuestionModelsTest(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is in the future.
        """
        date_in_future = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=date_in_future)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is older than 1 day.
        """
        date_in_past = timezone.now() - datetime.timedelta(days=1)
        past_question = Question(pub_date=date_in_past)
        self.assertIs(past_question.was_published_recently(), False)

    def test_was_published_recently_with_new_question(self):
        """
        was_publised_recently() returns True for questions whose pub_date is within the last day.
        """
        recent_date = timezone.now() - datetime.timedelta(hours=23, minutes=59,seconds=59)
        recent_question = Question(pub_date=recent_date)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    Creates a question with the given 'question_text' and published the given number of 'days' offset to now
    """
    time = timezone.now() + timezone.timedelta(days = days)
    return Question.objects.create(question_text=question_text, pub_date = time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exists, an appropriate message is displayed.
        """
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the index page.
        """
        create_question(question_text="Past question", days=-1)
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future are not displayed on the index page.
        """
        create_question(question_text="Future question", days=1)
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            []
        )

    def test_future_questions_and_past_questions(self):
        """
        Even if both future and past questions exists, only past questions are displayed.
        """
        create_question(question_text="Past question", days=-1)
        create_question(question_text="Future question", days=1)
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )

    def test_two_past_questions(self):
        """
        The question index page must display multiple questions
        """
        create_question(question_text="First past question", days=-1)
        create_question(question_text="Second past question", days=-1)
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Second past question>','<Question: First past question>']
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The details view of a question whose pub_date is in the future returns 404.
        """
        future_question = create_question("Future question", days=1)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The details view of a question whose pub_date is in the past shows the question's text.
        """
        past_question = create_question("Past question", days=-1)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)




