from django.shortcuts import render
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView
from onlineschoolapp.forms import StudentSignUpForm, TeacherSignUpForm, MentorSignUpForm
from onlineschoolapp.models import calc_online_school_stats
from onlineschoolapp.models import User, Course, Teacher, Student, Mentor, Lesson, Grade
from onlineschoolapp.filters import CourseFilter, TeacherFilter, StudentFilter, MentorFilter, LessonFilter
from onlineschoolapp.decorators import teacher_required, student_required, mentor_required


class CourseListView(generic.ListView):

    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CourseFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CourseDetailView(generic.DetailView):
    model = Course


class TeacherListView(generic.ListView):
    model = Teacher

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TeacherFilter(self.request.GET, queryset=self.get_queryset())
        return context


class TeacherDetailView(generic.DetailView):
    model = Teacher


class StudentListView(LoginRequiredMixin, generic.ListView):

    model = Student
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = StudentFilter(self.request.GET, queryset=self.get_queryset())
        return context


class StudentDetailView(generic.DetailView):
    model = Student


class MentorListView(LoginRequiredMixin, generic.ListView):

    model = Mentor
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = MentorFilter(self.request.GET, queryset=self.get_queryset())
        return context


class MentorDetailView(generic.DetailView):
    model = Mentor


class LessonListView(LoginRequiredMixin, generic.ListView):

    model = Lesson
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = LessonFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        if self.request.user.is_student:
            return Lesson.objects.filter(course_id__student__user=self.request.user)
        else:
            return Lesson.objects.all()


class LessonDetailView(generic.DetailView):
    model = Lesson


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


class StudentSignUpView(CreateView):

    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return index(self.request)


class TeacherSignUpView(CreateView):

    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return index(self.request)


class MentorSignUpView(CreateView):

    model = User
    form_class = MentorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'mentor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return index(self.request)


@method_decorator([login_required, student_required], name='dispatch')
class StudentGradesListView(LoginRequiredMixin, generic.ListView):

    model = Student
    template_name ='onlineschoolapp/student_grades_list.html'

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)


@method_decorator([login_required, teacher_required], name='dispatch')
class LessonCreate(CreateView):

    model = Lesson
    fields = ['title', 'course_id', 'teacher_id', 'link']
    success_url = reverse_lazy('lessons')


@method_decorator([login_required, teacher_required], name='dispatch')
class LessonDelete(DeleteView):

    model = Lesson
    success_url = reverse_lazy('lessons')


@method_decorator([login_required, teacher_required], name='dispatch')
class GradeUpdate(UpdateView):

    model = Grade
    fields = ['course', 'student', 'homework1', 'homework2', 'project', 'final_mark']
    success_url = reverse_lazy('students')


def index(request):

    num_courses, num_teachers, num_students = calc_online_school_stats()
    return render(request, 'index.html',
                  context={'num_courses': num_courses,
                           'num_teachers': num_teachers,
                           'num_students': num_students})