from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="home"),
    path("reset_data_base", views.reset_data_base, name="reset_data_base"),
    path("send_database_restart", views.send_database_restart, name="send_database_restart"),
    path("student_data", views.student_data, name="student_data"),
    path("documentation", views.documentation, name="documentation"),
    path("load_file_configuration", views.load_file_configuration, name="load_file_configuration"),
    path("load_files_transactions", views.load_file_transactions, name="load_files_transactions"),
    path("process_file_config", views.process_file_config, name="process_file_config"),
    path("process_file_transactions", views.process_file_transactions, name="process_file_transactions"),
    path("consult_account_statement", views.consult_account_statement, name="consult_account_statement"),
]
