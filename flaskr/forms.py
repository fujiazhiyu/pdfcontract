# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, Email, InputRequired, NumberRange, Length, optional, ValidationError


class ContractForm(FlaskForm):
    submit = SubmitField('提交')
    email = StringField('Email', validators=[InputRequired(), Email()])
    student = StringField('学生姓名', validators=[InputRequired(), Length(min=1, max=30)])
    district = StringField('申请地区', validators=[InputRequired()])
    subject = StringField('申请专业', validators=[InputRequired()], default='建筑学')
    degree = SelectField('就读学位', coerce=str, choices=[('本科', '本科'), ('硕士', '硕士'), ('博士', '博士')], default='硕士')


class ApplicationForm(ContractForm):
    # 留学申请
    applyyear = IntegerField('申请年份', validators=[InputRequired()], default=2020)
    univalent = IntegerField('单价', validators=[InputRequired()], default=2000)
    school = IntegerField('申请学校数量', validators=[InputRequired()], default=6)
    total = IntegerField('总金额', validators=[InputRequired()], default=18000)


class CommissionForm(ContractForm):
    # 作品集委托辅导
    univalent = IntegerField('单价（老师每课时基本薪酬）', validators=[InputRequired()], default=200)
    lesson = IntegerField('课时数', validators=[InputRequired()], default=40)
    level = StringField('教师级别', validators=[InputRequired()], default="辅导老师I级")
    award = FloatField('奖金', validators=[InputRequired()], default=20)
    teacher = StringField('老师姓名', validators=[optional()])
    works = IntegerField('作品数量', validators=[InputRequired()], default=4)

    # def validate_previous(form, field):
    #     if form.lesson.data < field.data:
    #         raise ValidationError("前期课时数超额!")


class InstructionForm(ContractForm):
    # 作品集辅导
    univalent = IntegerField('单价（学生每课时学费）', validators=[InputRequired()], default=1000)
    lesson = IntegerField('课时数', validators=[InputRequired()], default=40)
    works = IntegerField('作品数量', validators=[InputRequired()], default=4)
    total = IntegerField('总金额', validators=[InputRequired()], default=40000)

    def validate_total(form, field):
        if field.data != form.univalent.data * form.lesson.data:
            raise ValidationError("总价与课时数不匹配！")


class CommissionApplicationForm(ContractForm):
    # 留学申请委托
    applyyear = IntegerField('申请年份', validators=[InputRequired()], default=2020)
    school = IntegerField('申请学校数量', validators=[InputRequired()], default=6)
    total = IntegerField('总金额', validators=[InputRequired()], default=2000)
    univalent = IntegerField('每所学校申请费用', validators=[InputRequired()], default=200)
    teacher = StringField('老师姓名', validators=[optional()])
