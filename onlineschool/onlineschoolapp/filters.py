import django_filters
from onlineschoolapp.models import Course, Teacher, Student, Lesson, Mentor


class CourseFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(field_name='name', lookup_expr='contains', label='Название курса')

    class Meta:
        model = Course
        fields = ['name', 'price', 'duration']


class TeacherFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(field_name='name', lookup_expr='contains', label='Имя и фамилия преподавателя')
    course = django_filters.CharFilter(field_name='course__name', lookup_expr='contains', label='Курс')

    class Meta:
        model = Teacher
        fields = ['name', 'company', 'course']


class StudentFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(field_name='name', lookup_expr='contains', label='Имя и фамилия студента')
    course = django_filters.CharFilter(field_name='course__name', lookup_expr='contains', label='Курс')
    homework1 = django_filters.NumberFilter(field_name='grade__homework1', label='Оценка за 1 ДЗ')
    homework2 = django_filters.NumberFilter(field_name='grade__homework2', label='Оценка за 2 ДЗ')
    project = django_filters.NumberFilter(field_name='grade__project', label='Оценка за проект')
    final_mark = django_filters.NumberFilter(field_name='grade__final_mark', label='Итоговая оценка за курс')

    class Meta:
        model = Student
        fields = ['name', 'course', 'homework1', 'homework2', 'project', 'final_mark']


class MentorFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(field_name='name', lookup_expr='contains', label='Имя и фамилия ментора')
    course = django_filters.CharFilter(field_name='course__name', lookup_expr='contains', label='Курс')
    education = django_filters.CharFilter(field_name='education', lookup_expr='contains')

    class Meta:
        model = Mentor
        fields = ['name', 'course', 'education']


class LessonFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(field_name='title', lookup_expr='contains', label='Тема занятия')
    course = django_filters.CharFilter(field_name='course_id__name', lookup_expr='contains', label='Курс')
    teacher = django_filters.CharFilter(field_name='teacher_id__name', lookup_expr='contains',
                                        label='Имя и фамилия преподавателя')

    class Meta:
        model = Lesson
        fields = ['title', 'teacher']